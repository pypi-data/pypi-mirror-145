"""Workers for handling task running on pods."""
from __future__ import annotations

import logging
from typing import Any, List, Optional, Type

from marshmallow import Schema as MarshmallowSchema
import sqlvalidator  # type: ignore[import] # reason: typing issues with this import

from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.exceptions import DataStructureError
from bitfount.data.utils import DatabaseConnection
from bitfount.federated.algorithms.base import _BaseAlgorithmSchema
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithm,
    _BaseModelAlgorithmSchema,
)
from bitfount.federated.algorithms.sql_query import SqlQuery
from bitfount.federated.authorisation_checkers import _AuthorisationChecker
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.model_reference import BitfountModelReference
from bitfount.federated.pod_vitals import _PodVitals
from bitfount.federated.privacy.differential import DPPodConfig
from bitfount.federated.protocols.base import _BaseProtocolFactory
from bitfount.federated.transport.message_service import _BitfountMessageType
from bitfount.federated.transport.worker_transport import _WorkerMailbox
from bitfount.federated.utils import (
    _AGGREGATORS,
    _ALGORITHMS,
    _DISTRIBUTED_MODELS,
    _MODELS,
    _PROTOCOLS,
)
from bitfount.hub.api import BitfountHub

logger = _get_federated_logger(__name__)


class _Worker:
    """Client worker which runs a protocol locally.

    Args:
        datasource: DataSource object.
        mailbox: Relevant mailbox.
        bitfounthub: BitfountHub object.
        authorisation: AuthorisationChecker object.
        pod_identifier: Identifier of the pod the Worker is running in.
        pod_vitals: PodVitals object.
        pod_dp: DPPodConfig object.
    """

    def __init__(
        self,
        datasource: DataSource,
        mailbox: _WorkerMailbox,
        bitfounthub: BitfountHub,
        authorisation: _AuthorisationChecker,
        pod_identifier: str,
        pod_vitals: Optional[_PodVitals] = None,
        pod_dp: Optional[DPPodConfig] = None,
        **_kwargs: Any,
    ):
        self.datasource = datasource
        self.mailbox = mailbox
        self.hub = bitfounthub
        self.authorisation: _AuthorisationChecker = authorisation
        self.pod_identifier = pod_identifier
        self.pod_vitals = pod_vitals
        self._pod_dp = pod_dp

    def _deserialize_protocol(self, serialized_protocol: dict) -> _BaseProtocolFactory:
        """Takes a marshmallow serialized protocol, instantiates and returns it."""
        model_schema: Optional[Type[MarshmallowSchema]] = None
        aggregator_schema: Optional[Type[MarshmallowSchema]] = None

        if "model" in serialized_protocol["algorithm"]:
            model = None
            model_name = serialized_protocol["algorithm"]["model"].pop("name")
            # Currently, if there is an aggregator, it means there is necessarily also
            # a distributed model
            if model_name == "BitfountModelReference":
                schema = BitfountModelReference._Schema()
                model = schema.load(serialized_protocol["algorithm"]["model"])
                model.hub = self.hub

            if "aggregator" in serialized_protocol:
                if model is None:
                    try:
                        model = _DISTRIBUTED_MODELS[model_name]
                    except KeyError:
                        logging.error(
                            "Modeller has sent a model that is incompatible"
                            + " with their chosen algorithm/protocol.",
                        )
                        raise ValueError

                aggregator_cls = _AGGREGATORS[serialized_protocol["aggregator"]["name"]]
                aggregator_schema = aggregator_cls.get_schema(
                    tensor_shim_factory=model.backend_tensor_shim
                )
                model_schema = model.get_schema()
            else:
                if model is None:
                    model = _MODELS[model_name]
                model_schema = model.get_schema()
        algorithm_cls = _ALGORITHMS[serialized_protocol["algorithm"]["name"]]

        if issubclass(algorithm_cls, _BaseAlgorithmSchema):
            algorithm_schema = algorithm_cls.get_schema()
        elif issubclass(algorithm_cls, _BaseModelAlgorithmSchema):
            if model_schema is None:
                raise TypeError(
                    f"Chosen algorithm ({algorithm_cls}) is a model algorithm, "
                    f"but no model schema was specified"
                )
            algorithm_schema = algorithm_cls.get_schema(model_schema=model_schema)
        else:
            raise AttributeError(
                f"Algorithm class {algorithm_cls} does not implement get_schema()"
            )

        return _PROTOCOLS[serialized_protocol["name"]].load(
            serialized_protocol=serialized_protocol,
            algorithm_schema=algorithm_schema,
            aggregator_schema=aggregator_schema,
        )

    async def _get_protocol(self) -> _BaseProtocolFactory:
        """Retrieves the protocol."""
        serialized_protocol = await self.mailbox.get_task_details()
        return self._deserialize_protocol(serialized_protocol)

    async def run(self) -> None:
        """Calls relevant training procedure and sends back weights/results."""
        authorisation_errors = await self.authorisation.check_authorisation()

        if authorisation_errors.messages:
            # Reject task, as there were errors
            await self.mailbox.reject_task(
                authorisation_errors.messages,
            )
            return

        # Accept task and inform modeller
        logger.info("Task accepted, informing modeller.")
        await self.mailbox.accept_task()

        protocol = await self._get_protocol()
        verified = self.authorisation.verify_protocol(protocol)

        if not verified:
            logger.federated_error(
                "The protocol that has been received does not match "
                "the original protocol that was authorised and accepted. "
                "Aborting task."
            )
            self.mailbox.delete_handler(_BitfountMessageType.LOG_MESSAGE)
            return

        # Load data for training here
        datastructure: Optional[DataStructure] = None

        if hasattr(protocol.algorithm, "model"):
            datastructure = protocol.algorithm.model.datastructure  # type: ignore[attr-defined] # Reason: hasattr check # noqa: B950

        if not isinstance(protocol.algorithm, SqlQuery):
            # We execute the query directly on the db connection,
            # or load the data at runtime for a csv.
            # TODO: [NO_TICKET: Reason] No ticket created yet. Add the private sql query algorithm here as well. # noqa: B950
            self._load_data_for_worker(datastructure=datastructure)

        # Calling the `worker` method on the protocol also calls the `worker` method on
        # underlying objects such as the algorithm and aggregator. The algorithm
        # `worker` method will also download the model from the Hub if it is a
        # `BitfountModelReference`
        worker_protocol = protocol.worker(mailbox=self.mailbox, hub=self.hub)

        # If the algorithm is a model algorithm, then we need to pass the pod identifier
        # to the model so that it can extract the relevant information from the
        # datastructure the Modeller has sent.
        if isinstance(worker_protocol.algorithm, _BaseModelAlgorithm):
            worker_protocol.algorithm.model.set_pod_identifier(self.pod_identifier)

        await worker_protocol.run(
            datasource=self.datasource,
            pod_dp=self._pod_dp,
            pod_vitals=self.pod_vitals,
            pod_identifier=self.mailbox.pod_identifier,
        )
        logger.info("Task complete")
        self.mailbox.delete_handler(_BitfountMessageType.LOG_MESSAGE)

    def _load_data_for_worker(
        self,
        datastructure: Optional[DataStructure] = None,
    ) -> None:
        """Load the data for the worker."""
        selected_cols: List[str] = []
        sql_query: Optional[str] = None
        table: Optional[str] = None

        if datastructure:
            if datastructure.table:
                if isinstance(datastructure.table, dict):
                    if not (table := datastructure.table.get(self.pod_identifier)):
                        raise DataStructureError(
                            f"Table definition not found for {self.pod_identifier}. "
                            f"Table definitions provided in this DataStructure: "
                            f"{str(datastructure.table)}"
                        )
                elif isinstance(datastructure.table, str):
                    table = datastructure.table
            elif datastructure.query:
                if isinstance(datastructure.query, dict):
                    if not (sql_query := datastructure.query.get(self.pod_identifier)):
                        raise DataStructureError(
                            f"Query definition not found for {self.pod_identifier}. "
                            f"Query definitions provided in this DataStructure: "
                            f"{str(datastructure.query)}"
                        )
                elif isinstance(datastructure.query, str):
                    sql_query = datastructure.query
                if sqlvalidator.parse(sql_query).is_valid():
                    if not isinstance(self.datasource.data_ref, DatabaseConnection):
                        raise ValueError(
                            "Incompatible DataStructure, DataSource pair."
                            "DataStructure is expecting the DataSource to "
                            "be a DatabaseConnection."
                        )
        self.datasource.load_data(table_name=table, sql_query=sql_query)
        datasource_cols = self.datasource.get_features()

        if datastructure:
            if datastructure.ignore_cols:
                selected_cols = [
                    i for i in datasource_cols if i not in datastructure.ignore_cols
                ]
            elif datastructure.selected_cols:
                selected_cols = datastructure.selected_cols
                diff = list(set(selected_cols) - set(datasource_cols))
                if diff:
                    logger.warning(
                        f"Selected columns `{','.join(diff)}` "
                        f"were not found in the data, continuing without them."
                    )
                    selected_cols = [i for i in selected_cols if i not in diff]
            else:
                selected_cols = datasource_cols

            self.datasource.data = self.datasource.data[selected_cols]
