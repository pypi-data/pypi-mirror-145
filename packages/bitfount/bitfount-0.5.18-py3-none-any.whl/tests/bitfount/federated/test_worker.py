"""Tests worker.py."""
import re
from typing import Any, Mapping, Optional, cast
from unittest.mock import AsyncMock, Mock, create_autospec

from _pytest.logging import LogCaptureFixture
from _pytest.monkeypatch import MonkeyPatch
import pandas as pd
import pytest
from pytest import fixture
from pytest_mock import MockerFixture
import sqlalchemy

from bitfount import BitfountSchema, ColumnAverage, DataSource, DataStructure
from bitfount.data.exceptions import DataStructureError
from bitfount.data.types import SchemaOverrideMapping
from bitfount.data.utils import DatabaseConnection
from bitfount.federated.aggregators.base import _BaseAggregatorFactory
from bitfount.federated.aggregators.base import _registry as aggregator_registry
from bitfount.federated.algorithms.base import (
    _BaseAlgorithmFactory,
    _BaseAlgorithmSchema,
)
from bitfount.federated.algorithms.base import _registry as algorithm_registry
from bitfount.federated.algorithms.model_algorithms.base import (
    _BaseModelAlgorithmSchema,
)
from bitfount.federated.authorisation_checkers import (
    _AuthorisationChecker,
    _LocalAuthorisation,
)
from bitfount.federated.protocols.base import _BaseProtocolFactory
from bitfount.federated.protocols.base import _registry as protocol_registry
from bitfount.federated.protocols.fed_avg import FederatedAveraging
from bitfount.federated.task_requests import _ProtocolDetails
from bitfount.federated.utils import _DISTRIBUTED_MODELS
from bitfount.federated.worker import _Worker
from bitfount.types import DistributedModelProtocol, _JSONDict
from tests.utils.helper import TABLE_NAME, create_dataset, create_datasource, unit_test


@unit_test
class TestWorker:
    """Tests Worker class."""

    @fixture
    def dummy_protocol(self) -> FederatedAveraging:
        """Returns a FederatedAveraging instance."""
        protocol = Mock(algorithm=Mock(), aggregator=Mock())
        protocol.name = "FederatedAveraging"
        protocol.algorithm.name = "FederatedModelTraining"
        protocol.aggregator.name = "Aggregator"
        protocol.algorithm.model = Mock()
        protocol.algorithm.model.datastructure = create_autospec(DataStructure)
        protocol.algorithm.model.schema = create_autospec(BitfountSchema)
        return protocol

    @fixture
    def authoriser(self) -> _AuthorisationChecker:
        """An AuthorisationChecker object.

        An instance of LocalAuthorisation is returned because AuthorisationChecker
        cannot itself be instantiated.
        """
        return _LocalAuthorisation(
            Mock(),
            _ProtocolDetails(
                "bitfount.FederatedAveraging",
                "bitfount.FederatedModelTraining",
                aggregator="bitfount.SecureAggregator",
            ),
        )

    async def test_unverified_protocol_aborts_task(
        self,
        authoriser: _AuthorisationChecker,
        caplog: LogCaptureFixture,
        dummy_protocol: FederatedAveraging,
        mocker: MockerFixture,
    ) -> None:
        """Tests that an unverified protocol from the Modeller aborts the task.

        The authoriser expects the aggregator to be Secure but the protocol that is
        received actually uses the insecure aggregator. Thus we expect the task to
        be aborted.
        """
        caplog.set_level("INFO")
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        worker = _Worker(
            Mock(), AsyncMock(), Mock(), authoriser, pod_identifier="dummy_id"
        )
        mocker.patch.object(worker, "_get_protocol", return_value=dummy_protocol)

        await worker.run()

        assert len(caplog.records) == 3

        for i, record in enumerate(caplog.records):

            if i == 0:
                assert record.levelname == "INFO"
                assert record.msg == "Task accepted, informing modeller."

            elif i == 1:
                assert record.levelname == "ERROR"
                assert (
                    record.msg == "Aggregator Aggregator does not match "
                    "bitfount.SecureAggregator"
                )
            elif i == 2:
                assert record.levelname == "ERROR"
                assert (
                    record.msg == "The protocol that has been received does not match "
                    "the original protocol that was authorised and accepted. "
                    "Aborting task."
                )
            else:
                pytest.fail("Unexpected log level.")

    @fixture
    def mock_aggregator_cls_name(self) -> str:
        """Registry name for mock aggregator class."""
        return "mock_aggregator_cls"

    @fixture
    def mock_aggregator_cls_in_registry(
        self, mock_aggregator_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock aggregator class in relevant registry."""
        mock_aggregator_cls: Mock = create_autospec(_BaseAggregatorFactory)
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            aggregator_registry,
            mock_aggregator_cls_name,
            cast(Any, mock_aggregator_cls),
        )
        return mock_aggregator_cls

    @fixture
    def mock_algorithm_cls_name(self) -> str:
        """Registry name for mock algorithm class."""
        return "mock_algorithm_cls"

    @fixture
    def mock_algorithm_cls_in_registry(
        self, mock_algorithm_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock algorithm class in relevant registry."""
        mock_algorithm_cls: Mock = create_autospec(_BaseAlgorithmFactory)
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            algorithm_registry, mock_algorithm_cls_name, cast(Any, mock_algorithm_cls)
        )
        return mock_algorithm_cls

    @fixture
    def mock_model_cls_name(self) -> str:
        """Registry name for mock model class."""
        return "mock_model_cls"

    @fixture
    def mock_model_cls_in_registry(
        self, mock_model_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock model class in relevant registry."""
        mock_model_cls: Mock = create_autospec(DistributedModelProtocol)
        mock_model_cls.Schema = Mock()
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            _DISTRIBUTED_MODELS, mock_model_cls_name, cast(Any, mock_model_cls)
        )
        return mock_model_cls

    @fixture
    def mock_protocol_cls_name(self) -> str:
        """Registry name for mock protocol class."""
        return "mock_protocol_cls"

    @fixture
    def mock_protocol_cls_in_registry(
        self, mock_protocol_cls_name: str, monkeypatch: MonkeyPatch
    ) -> Mock:
        """Places mock protocol class in relevant registry."""
        mock_protocol_cls: Mock = create_autospec(_BaseProtocolFactory)
        # cast() needed as mypy cannot infer type correctly for MonkeyPatch.setitem()
        monkeypatch.setitem(
            protocol_registry, mock_protocol_cls_name, cast(Any, mock_protocol_cls)
        )
        return mock_protocol_cls

    @fixture
    def serialized_protocol_modelless(
        self, mock_algorithm_cls_name: str, mock_protocol_cls_name: str
    ) -> _JSONDict:
        """Serialized protocol dict without model."""
        return {
            "algorithm": {
                "name": mock_algorithm_cls_name,
            },
            "name": mock_protocol_cls_name,
        }

    @fixture
    def serialized_protocol_with_model(
        self,
        mock_aggregator_cls_name: str,
        mock_algorithm_cls_name: str,
        mock_model_cls_name: str,
        mock_protocol_cls_name: str,
    ) -> _JSONDict:
        """Serialized protocol dict with model (and aggregator)."""
        return {
            "algorithm": {
                "name": mock_algorithm_cls_name,
                "model": {"name": mock_model_cls_name},
            },
            "aggregator": {"name": mock_aggregator_cls_name},
            "name": mock_protocol_cls_name,
        }

    @fixture
    def mock_worker(self) -> Mock:
        """Mock Worker instance to use in `self` arg."""
        mock_worker = Mock(spec=_Worker, hub=Mock())
        return mock_worker

    def test__deserialize_protocol_with_modelless_algo(
        self,
        mock_algorithm_cls_in_registry: Mock,
        mock_protocol_cls_in_registry: Mock,
        mock_worker: Mock,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        serialized_protocol_modelless: _JSONDict,
    ) -> None:
        """Test _deserialize_protocol works with modelless algorithm."""
        # Patch with BaseAlgorithmSchema style get_schema
        mock_algorithm_cls_in_registry.get_schema = create_autospec(
            _BaseAlgorithmSchema.get_schema
        )

        # Difficult to handle issubclass checks with mocks; easiest way is to just
        # patch the builtin directly
        mocker.patch("bitfount.federated.worker.issubclass", return_value=True)

        _Worker._deserialize_protocol(
            self=mock_worker, serialized_protocol=serialized_protocol_modelless
        )

        # Check protocol/schema calls as expected
        mock_algorithm_cls_in_registry.get_schema.assert_called_once_with()
        mock_protocol_cls_in_registry.load.assert_called_once_with(
            serialized_protocol=serialized_protocol_modelless,
            algorithm_schema=mock_algorithm_cls_in_registry.get_schema.return_value,
            aggregator_schema=None,
        )

    def test__deserialize_protocol_with_model_algo(
        self,
        mock_aggregator_cls_in_registry: Mock,
        mock_algorithm_cls_in_registry: Mock,
        mock_model_cls_in_registry: Mock,
        mock_protocol_cls_in_registry: Mock,
        mock_worker: Mock,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        serialized_protocol_with_model: _JSONDict,
    ) -> None:
        """Test _deserialize_protocol works with model algorithm."""
        # Patch with BaseModelAlgorithmSchema style get_schema
        mock_algorithm_cls_in_registry.get_schema = create_autospec(
            _BaseModelAlgorithmSchema.get_schema
        )

        # Difficult to handle issubclass checks with mocks; easiest way is to just
        # patch the builtin directly. Need to fail first check, pass second.
        mocker.patch("bitfount.federated.worker.issubclass", side_effect=[False, True])

        _Worker._deserialize_protocol(
            self=mock_worker, serialized_protocol=serialized_protocol_with_model
        )

        # Check protocol/schema calls as expected
        mock_algorithm_cls_in_registry.get_schema.assert_called_once_with(
            model_schema=mock_model_cls_in_registry.get_schema()
        )
        mock_protocol_cls_in_registry.load.assert_called_once_with(
            serialized_protocol=serialized_protocol_with_model,
            algorithm_schema=mock_algorithm_cls_in_registry.get_schema.return_value,
            aggregator_schema=mock_aggregator_cls_in_registry.get_schema.return_value,
        )

    def test__deserialize_protocol_fails_with_model_algo_but_no_model(
        self,
        mock_algorithm_cls_in_registry: Mock,
        mock_protocol_cls_in_registry: Mock,
        mock_worker: Mock,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        serialized_protocol_modelless: _JSONDict,
    ) -> None:
        """Test _deserialize_protocol fails with model algorithm but no model."""
        # Patch with BaseModelAlgorithmSchema style get_schema
        mock_algorithm_cls_in_registry.get_schema = create_autospec(
            _BaseModelAlgorithmSchema.get_schema
        )

        # Difficult to handle issubclass checks with mocks; easiest way is to just
        # patch the builtin directly. Need to fail first check, pass second.
        mocker.patch("bitfount.federated.worker.issubclass", side_effect=[False, True])

        with pytest.raises(
            TypeError,
            match=re.escape(
                f"Chosen algorithm ({mock_algorithm_cls_in_registry}) is a model "
                f"algorithm, but no model schema was specified"
            ),
        ):
            _Worker._deserialize_protocol(
                self=mock_worker, serialized_protocol=serialized_protocol_modelless
            )

    def test__deserialize_protocol_fails_if_algo_schema_style_not_supported(
        self,
        mock_algorithm_cls_in_registry: Mock,
        mock_protocol_cls_in_registry: Mock,
        mock_worker: Mock,
        mocker: MockerFixture,
        monkeypatch: MonkeyPatch,
        serialized_protocol_modelless: _JSONDict,
    ) -> None:
        """Test _deserialize_protocol fails with unknown algorithm schema style."""
        # Difficult to handle issubclass checks with mocks; easiest way is to just
        # patch the builtin directly. Need to fail all checks.
        mocker.patch("bitfount.federated.worker.issubclass", return_value=False)

        with pytest.raises(
            AttributeError,
            match=re.escape(
                f"Algorithm class {mock_algorithm_cls_in_registry} does not "
                f"implement get_schema()"
            ),
        ):
            _Worker._deserialize_protocol(
                self=mock_worker, serialized_protocol=serialized_protocol_modelless
            )

    async def test_worker_run_protocol_with_model_loads_datastructure_schema(
        self,
        authoriser: _AuthorisationChecker,
        dummy_protocol: FederatedAveraging,
        mocker: MockerFixture,
    ) -> None:
        """Tests that the datastructure and schema are taken from model."""
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        worker = _Worker(
            Mock(), AsyncMock(), Mock(), authoriser, pod_identifier="dummy_id"
        )
        mocker.patch.object(worker, "_get_protocol", return_value=dummy_protocol)
        mocker.patch.object(authoriser, "verify_protocol", return_value=True)
        mocker.patch.object(dummy_protocol, "worker", return_value=AsyncMock())
        mocker.patch.object(dummy_protocol.worker, "run")
        mock_data = mocker.patch.object(worker, "_load_data_for_worker")
        await worker.run()
        mock_data.assert_called_once_with(
            datastructure=dummy_protocol.algorithm.model.datastructure,
        )

    async def test_worker_run_protocol_without_model_no_datastructure(
        self,
        authoriser: _AuthorisationChecker,
        mocker: MockerFixture,
    ) -> None:
        """Tests that the datastructure and schema are None if no model."""
        dummy_protocol = Mock(algorithm=create_autospec(ColumnAverage))
        mocker.patch.object(
            authoriser, "check_authorisation", return_value=Mock(messages=None)
        )
        worker = _Worker(
            Mock(), AsyncMock(), Mock(), authoriser, pod_identifier="dummy_id"
        )
        mocker.patch.object(worker, "_get_protocol", return_value=dummy_protocol)
        mocker.patch.object(authoriser, "verify_protocol", return_value=True)
        mocker.patch.object(dummy_protocol, "worker", return_value=AsyncMock())
        mocker.patch.object(dummy_protocol.worker, "run")
        mock_data = mocker.patch.object(worker, "_load_data_for_worker")
        await worker.run()
        mock_data.assert_called_once_with(datastructure=None)

    def test__load_data_for_worker(
        self,
        mocker: MockerFixture,
    ) -> None:
        """Tests that the worker loads the data."""
        datasource = create_datasource(classification=True)
        worker = _Worker(
            datasource, AsyncMock(), Mock(), Mock(), pod_identifier="dummy_id"
        )

        def mock_load_data(
            self_: DataSource, table_name: Optional[str], sql_query: Optional[str]
        ) -> None:
            self_._data_is_loaded = True
            self_.data = Mock(spec=pd.DataFrame)

        mocker.patch(
            "bitfount.federated.worker.DataSource.load_data",
            autospec=True,
            side_effect=mock_load_data,
        )

        # Assert that a datasource is returned is constructed
        worker._load_data_for_worker()
        assert worker.datasource is not None
        assert isinstance(worker.datasource, DataSource)

    def test__load_data_for_worker_with_datastructure_selected_cols(
        self,
    ) -> None:
        """Tests data is loaded according to datastructure and schema."""
        dataframe = create_dataset()
        datastructure = DataStructure(
            selected_cols=["A", "C", "M", "TARGET"], table=TABLE_NAME
        )
        datasource = DataSource(data_ref=dataframe)
        worker = _Worker(
            datasource, AsyncMock(), Mock(), Mock(), pod_identifier="dummy_id"
        )
        worker._load_data_for_worker(datastructure=datastructure)
        assert worker.datasource is not None
        assert isinstance(worker.datasource, DataSource)
        assert (
            sorted(worker.datasource.data.columns.tolist())
            == datastructure.selected_cols
        )

    def test__load_data_for_worker_with_datastructure_selected_extra_cols(
        self,
        caplog: LogCaptureFixture,
    ) -> None:
        """Tests that the worker loads the data according to DataStructure and schema.

        Checks that even if extra columns are provided in the DataStructure,
        they are not used when loading the datasource.
        """
        caplog.set_level("INFO")
        dataframe = create_dataset()
        datastructure = DataStructure(
            selected_cols=["A", "C", "M", "Z", "TARGET"], table=TABLE_NAME
        )
        worker = _Worker(
            DataSource(data_ref=dataframe),
            AsyncMock(),
            Mock(),
            Mock(),
            pod_identifier="dummy_id",
        )
        worker._load_data_for_worker(datastructure=datastructure)
        assert worker.datasource is not None
        assert isinstance(worker.datasource, DataSource)
        assert sorted(worker.datasource.data.columns.tolist()) == [
            "A",
            "C",
            "M",
            "TARGET",
        ]
        assert any(
            "Selected columns `Z` were not found in the data, continuing without them."
            in record.msg
            for record in caplog.records
        )

    def test__load_data_for_worker_with_datastructure_ignore_cols(
        self,
    ) -> None:
        """Tests data is loaded according to DataStructure and schema."""
        dataframe = create_dataset()
        datastructure = DataStructure(
            table=TABLE_NAME,
            ignore_cols=[
                "N",
                "O",
                "P",
                "B",
                "D",
                "E",
                "F",
                "G",
                "H",
                "I",
                "J",
                "K",
                "L",
            ],
        )
        ds = DataSource(data_ref=dataframe)
        worker = _Worker(ds, AsyncMock(), Mock(), Mock(), pod_identifier="dummy_id")
        worker._load_data_for_worker(datastructure=datastructure)
        assert worker.datasource is not None
        assert isinstance(worker.datasource, DataSource)
        assert sorted(worker.datasource.data.columns) == [
            "A",
            "C",
            "Date",
            "M",
            "TARGET",
        ]

    @pytest.mark.parametrize(
        "sql_query, schema_types_override",
        [
            (
                'SELECT "Date", "TARGET" FROM dummy_data',
                {"categorical": [{"TARGET": {"0": 0, "1": 1}}], "text": ["Date"]},
            ),
            (
                """SELECT d1."Date", d2."A" from dummy_data d1
            JOIN dummy_data_2 d2
            ON d1."Date" = d2."Date"
            """,
                {"continuous": ["A"], "text": ["Date"]},
            ),
        ],
    )
    def test__load_data_for_worker_table_as_query_pod_id(
        self,
        db_session: sqlalchemy.engine.base.Engine,
        sql_query: str,
        schema_types_override: SchemaOverrideMapping,
    ) -> None:
        """Tests sql query provided by datastructure is applied to datasource."""
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )
        pod_id = "dummy_pod_id"
        expected_output = pd.read_sql(sql_query, con=db_conn.con)
        ds = DataSource(db_conn, seed=420)
        datastructure = DataStructure(
            query={pod_id: sql_query},
            schema_types_override={pod_id: schema_types_override},
        )
        worker = _Worker(ds, AsyncMock(), Mock(), Mock(), pod_identifier=pod_id)
        worker._load_data_for_worker(
            datastructure=datastructure,
        )
        pd.testing.assert_frame_equal(ds.data, expected_output)

    @pytest.mark.parametrize(
        "sql_query, schema_types_override",
        [
            (
                'SELECT "Date", "TARGET" FROM dummy_data',
                {"categorical": [{"TARGET": {"0": 0, "1": 1}}], "text": ["Date"]},
            ),
            (
                """SELECT d1."Date", d2."A" from dummy_data d1
            JOIN dummy_data_2 d2
            ON d1."Date" = d2."Date"
            """,
                {"continuous": ["A"], "text": ["Date"]},
            ),
        ],
    )
    def test__load_data_for_worker_table_as_query(
        self,
        db_session: sqlalchemy.engine.base.Engine,
        sql_query: str,
        schema_types_override: SchemaOverrideMapping,
    ) -> None:
        """Tests sql query provided by datastructure is applied to datasource."""
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )
        pod_id = "dummy_pod_id"
        expected_output = pd.read_sql(sql_query, con=db_conn.con)
        ds = DataSource(db_conn, seed=420)
        datastructure = DataStructure(
            query=sql_query,
            schema_types_override=schema_types_override,
        )
        worker = _Worker(ds, AsyncMock(), Mock(), Mock(), pod_identifier=pod_id)
        worker._load_data_for_worker(
            datastructure=datastructure,
        )
        pd.testing.assert_frame_equal(ds.data, expected_output)

    def test__load_data_for_worker_single_table(
        self, db_session: sqlalchemy.engine.base.Engine
    ) -> None:
        """Tests table name provided by datastructure is applied to datasource."""
        table = "dummy_data"
        db_conn = DatabaseConnection(db_session, table_names=[table])
        pod_id = "dummy_pod_id"
        expected_output = pd.read_sql_table(table_name=table, con=db_conn.con)
        ds = DataSource(db_conn, seed=420)
        datastructure = DataStructure(table=table)
        worker = _Worker(ds, AsyncMock(), Mock(), Mock(), pod_identifier=pod_id)
        worker._load_data_for_worker(
            datastructure=datastructure,
        )
        pd.testing.assert_frame_equal(ds.data, expected_output)

    def test__load_data_for_worker_errors_wrong_pod_id_query(self) -> None:
        """Test error raised if DataStructure has no map for workers pod id."""
        sql_query = 'SELECT "Date", "TARGET" FROM dummy_data'
        worker_pod_id = "worker_pod_id"
        query = {"different_pod_id": sql_query}
        schema_override: Mapping[str, SchemaOverrideMapping]
        schema_override = {"different_pod_id": {"text": ["Date", "TARGET"]}}
        ds = create_datasource(classification=True)
        datastructure = DataStructure(
            query=query, schema_types_override=schema_override
        )
        worker = _Worker(ds, AsyncMock(), Mock(), Mock(), pod_identifier=worker_pod_id)
        with pytest.raises(DataStructureError):
            worker._load_data_for_worker(datastructure=datastructure)

    def test__load_data_for_worker_errors_wrong_pod_id_table(self) -> None:
        """Test error raised if DataStructure has no map for workers pod id."""
        worker_pod_id = "worker_pod_id"
        ds_table = {"different_pod_id": "table_name"}
        ds = create_datasource(classification=True)
        datastructure = DataStructure(table=ds_table)
        worker = _Worker(ds, AsyncMock(), Mock(), Mock(), pod_identifier=worker_pod_id)
        with pytest.raises(DataStructureError):
            worker._load_data_for_worker(datastructure=datastructure)

    def test__load_data_for_worker_errors_incompatiable_ds(self) -> None:
        """Test error raised with incompatible DataStructure and DataSource.

        If the datastructure table is given as a SQL query but the datasource
        is a dataframe an ValueError should be raised.
        """
        sql_query = 'SELECT "Date", "TARGET" FROM dummy_data'
        pod_id = "dummy_pod_id"
        schema_override: Mapping[str, SchemaOverrideMapping]
        schema_override = {pod_id: {"continuous": ["a", "b", "c"]}}
        ds = create_datasource(classification=True)
        datastructure = DataStructure(
            query={pod_id: sql_query},
            schema_types_override=schema_override,
        )
        worker = _Worker(ds, AsyncMock(), Mock(), Mock(), pod_identifier=pod_id)
        with pytest.raises(ValueError):
            worker._load_data_for_worker(datastructure=datastructure)
