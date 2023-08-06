"""SQL query algorithm."""
from __future__ import annotations

import os
from typing import Any, List, Optional, Type, Union, cast

from marshmallow import Schema as MarshmallowSchema
from marshmallow import fields, post_load
import pandas as pd
import pandasql  # type: ignore[import] # reason: typing issues with this import

from bitfount.data.datasource import DataSource
from bitfount.data.exceptions import DuplicateColumnError
from bitfount.data.utils import DatabaseConnection
from bitfount.federated.algorithms.base import (
    _BaseAlgorithmFactory,
    _BaseAlgorithmSchema,
    _BaseModellerAlgorithm,
    _BaseWorkerAlgorithm,
)
from bitfount.federated.logging import _get_federated_logger
from bitfount.federated.mixins import _SQLAlgorithmMixIn
from bitfount.federated.privacy.differential import DPPodConfig

logger = _get_federated_logger(__name__)


class _ModellerSide(_BaseModellerAlgorithm):
    """Modeller side of the SqlQuery algorithm."""

    def initialise(
        self,
        pretrained_file: Optional[Union[str, os.PathLike]] = None,
        **kwargs: Any,
    ) -> None:
        """Nothing to initialise here."""
        pass

    def run(self, results: List[pd.DataFrame]) -> List[pd.DataFrame]:
        """Simply returns results."""
        return results


class _WorkerSide(_BaseWorkerAlgorithm):
    """Worker side of the SqlQuery algorithm."""

    def __init__(self, *, query: str, **kwargs: Any) -> None:
        self.datasource: DataSource
        self.query = query
        super().__init__(**kwargs)

    def initialise(
        self,
        datasource: DataSource,
        pod_dp: Optional[DPPodConfig] = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        """Sets Datasource."""
        datasource.load_data()
        self.datasource = datasource

    def run(self) -> pd.DataFrame:
        """Returns the mean of the field in `DataSource` dataframe."""
        if self.datasource.multi_table and isinstance(
            self.datasource.data_ref, DatabaseConnection
        ):
            # Connect to the db directly if you are working with a multitable.
            # This is set to engine in the post init of DatabaseConnection,
            # but mypy is complaining.
            conn = self.datasource.data_ref.con.connect()
            output = pd.read_sql(sql=self.query, con=conn)
        else:
            # For SQL queries on a dataframe/ single table.
            if not self.datasource._data_is_loaded:
                self.datasource.load_data()
                df = self.datasource.data
            elif self.datasource._data_is_loaded:
                df = self.datasource.data
            if df is None:
                raise (ValueError("No data on which to execute SQL query."))

            if ("from df" not in self.query) and ("FROM df" not in self.query):
                raise ValueError(
                    "The default table is called 'df'.",
                    "Please ensure your SQL query operates on that table.",
                )

            try:
                # We assume that the query includes something like 'from df'.
                output = pandasql.sqldf(self.query, {"df": df})
            except pandasql.PandaSQLException as ex:
                raise ValueError(
                    f"Error executing SQL query: [{self.query}], got error [{ex}]"
                )
        if any(output.columns.duplicated()):
            raise DuplicateColumnError(
                f"""The following column names are duplicated in the output
                dataframe: {output.columns[output.columns.duplicated()]}.
                Please rename them in the query, and try again.
                """
            )
        return cast(pd.DataFrame, output)


class SqlQuery(_BaseAlgorithmSchema, _BaseAlgorithmFactory, _SQLAlgorithmMixIn):
    """Simple algorithm for running a SQL query on a table.

    Args:
        query: The SQL query to execute.

    Attributes:
        name: The name of the algorithm.
        field: The name of the column to take the mean of.
    """

    def __init__(self, *, query: str, **kwargs: Any):
        super().__init__()
        self.query = query

    def modeller(self, **kwargs: Any) -> _ModellerSide:
        """Returns the modeller side of the SqlQuery algorithm."""
        return _ModellerSide(**kwargs)

    def worker(self, **kwargs: Any) -> _WorkerSide:
        """Returns the worker side of the SqlQuery algorithm."""
        return _WorkerSide(query=self.query, **kwargs)

    @staticmethod
    def get_schema(**kwargs: Any) -> Type[MarshmallowSchema]:
        """Returns the schema for SqlQuery."""

        class Schema(_BaseAlgorithmFactory._Schema):

            query = fields.Str()

            @post_load
            def recreate_factory(self, data: dict, **_kwargs: Any) -> SqlQuery:
                return SqlQuery(**data)

        return Schema
