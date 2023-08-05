"""Classes concerning sources of data."""
from __future__ import annotations

from abc import ABC, abstractmethod
import logging
import os
from typing import Any, Dict, Iterable, List, Optional, Sequence, Set, Union, cast

import numpy as np
import pandas as pd
from pydantic import AnyUrl
import sqlalchemy
from sqlalchemy import MetaData, Table
from sqlalchemy.orm import Session
from sqlalchemy.sql.base import Executable

from bitfount.data.datasplitters import _DatasetSplitter
from bitfount.data.exceptions import DataNotLoadedError, DataNotSplitError
from bitfount.data.types import DataPathModifiers
from bitfount.data.utils import DatabaseConnection, _generate_dtypes_hash, _hash_str
from bitfount.types import _Dtypes
from bitfount.utils import seed_all

logger = logging.getLogger(__name__)


class _BaseLoader(ABC):
    """Abstract Base Loader from which all other data loaders must inherit."""

    def __init__(self) -> None:
        self.data: Optional[pd.DataFrame] = None

    @abstractmethod
    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Implement this method to get distinct values from list of columns."""
        raise NotImplementedError

    @abstractmethod
    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Implement this method to get single column from dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_data(self, **kwargs: Any) -> Optional[pd.DataFrame]:
        """Implement this method to loads and return dataset."""
        raise NotImplementedError

    @abstractmethod
    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Implement this method to get the columns and column types from dataset."""
        raise NotImplementedError


class CSVLoader(_BaseLoader):
    """Loader for loading csv files."""

    def __init__(self, path: Union[os.PathLike, AnyUrl, str]):
        if not str(path).endswith(".csv"):
            raise TypeError("Please provide a Path or URL to a CSV file.")
        self.path = str(path)
        self.data: pd.DataFrame = pd.read_csv(self.path)

    def get_data(self, **kwargs: Any) -> pd.DataFrame:
        """Loads and returns data from CSV dataset.

        Returns:
            A DataFrame-type object which contains the data.
        """
        return self.data

    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in CSV dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.

        """
        return {col: self.data[col].unique() for col in col_names}

    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from CSV dataset.

        Args:
            col_name: The name of the column which should be loaded.

        Returns:
            The column request as a series.
        """
        csv_df: pd.DataFrame = pd.read_csv(self.path, usecols=np.asarray([col_name]))
        return csv_df[col_name]

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Loads and returns the columns and column types of the CSV dataset.

        Returns:
            A mapping from column names to column types.
        """
        data = self.data.convert_dtypes()
        dtypes: _Dtypes = data.dtypes.to_dict()
        return dtypes


class DataFrameLoader(_BaseLoader):
    """Loader for loading dataframes."""

    def __init__(self, data: pd.DataFrame):
        self.data: pd.DataFrame = data

    def get_values(
        self, col_names: List[str], **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in DataFrame dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.
        """
        return {col: self.data[col].unique() for col in col_names}

    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from dataframe dataset.

        Args:
            col_name: The name of the column which should be loaded.

        Returns:
            The column request as a series.
        """
        return self.data[col_name]

    def get_data(self, **kwargs: Any) -> pd.DataFrame:
        """Loads and returns datafrom DataFrame dataset.

        Returns:
            A DataFrame-type object which contains the data.
        """
        return self.data

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Loads and returns the columns and column types from the Dataframe dataset.

        Returns:
            A mapping from column names to column types.
        """
        data = self.data.convert_dtypes()
        dtypes: _Dtypes = data.dtypes.to_dict()
        return dtypes


class DatabaseLoader(_BaseLoader):
    """Data source for loading data from databases."""

    def __init__(self, db_conn: DatabaseConnection):
        self.db_conn: DatabaseConnection = db_conn
        self.data: Optional[pd.DataFrame] = None
        self.table_names = self.db_conn.table_names
        self._con: Optional[sqlalchemy.engine.Engine] = None

    @property
    def query(self) -> Optional[Executable]:
        """A SQLAlchemy executable query."""
        if self.db_conn.query:
            return sqlalchemy.sql.expression.text(self.db_conn.query)
        else:
            return None

    @property
    def con(self) -> sqlalchemy.engine.Engine:
        """Sqlalchemy engine."""
        if not self._con:
            self._con = self.db_conn.con
        return self._con

    def _validate_table_name(self, table_name: Optional[str]) -> str:
        """Validate the table name is exists in the database.

        Args:
            table_name: The name of the table.

        Returns:
            The valid table name.

        Raises:
            ValueError: If the data is multi-table but no table name provided.
            ValueError: If the table name is not found in the data.
        """
        if self.db_conn.multi_table:
            if table_name is None:
                raise ValueError("No table name provided for multi-table datasource.")
            if self.table_names:
                if table_name not in self.table_names:
                    raise ValueError(
                        f"Table name {table_name} not found in the data. "
                        f"Available tables: {self.db_conn.table_names}"
                    )
        else:
            # If the data is not multi-table and there is no query, there must
            # necessarily be one table name. Reassuring mypy of this.
            assert self.db_conn.table_names is not None  # nosec
            assert len(self.db_conn.table_names) == 1  # nosec
            table_name = self.db_conn.table_names[0]
        return table_name

    def get_values(
        self, col_names: List[str], table_name: Optional[str] = None, **kwargs: Any
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in Database dataset.

        Args:
            col_names: The list of the columns whose distinct values should be
                returned.
            table_name: The name of the table to which the column exists. Required
                for multi-table databases.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.
        """
        metadata = MetaData(self.con)
        output: Dict[str, Iterable[Any]] = {}
        if self.query is not None:
            # TODO: [BIT-1595] change to load memory using sqlalchemy FrozenResult
            self.data = cast(pd.DataFrame, pd.read_sql(self.query, con=self.con))
            for col_name in col_names:
                output[col_name] = self.data[col_name].unique()
        else:
            table_name = self._validate_table_name(table_name)

            table = Table(
                table_name,
                metadata,
                schema=self.db_conn.db_schema,
                autoload=True,
                autoload_with=self.con,
            )
            with Session(self.con) as session:
                for col_name in col_names:
                    values = np.array(
                        [v for v, in session.query(table.columns[col_name]).distinct()]
                    )
                    output[col_name] = values
        return output

    def get_column(self, col_name: str, **kwargs: Any) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from Database dataset.

        Args:
            col_name: The name of the column which should be loaded.
            table_name: The name of the table to which the column exists. Required
                for multi-table databases.

        Returns:
            The column request as a series.

        Raises:
            ValueError: If the data is multi-table but no table name provided.
            ValueError: If the table name is not found in the data.
        """
        results: Iterable[Any]
        table_name = kwargs.get("table_name")
        metadata = MetaData(self.con)
        if self.query is not None:
            with Session(self.con) as session:
                results = session.execute(self.query).columns(col_name)
        else:
            table_name = self._validate_table_name(table_name)
            table = Table(
                table_name,
                metadata,
                schema=self.db_conn.db_schema,
                autoload=True,
                autoload_with=self.con,
            )
            with Session(self.con) as session:
                results = session.query(table.columns[col_name])

        series = pd.Series([v for v, in results])
        return series

    def get_data(self, **kwargs: Any) -> Optional[pd.DataFrame]:
        """Loads and returns data from Database dataset.

        Args:
            sql_query: A SQL query string required for multi table data sources.

        Returns:
            A DataFrame-type object which contains the data.
        """
        sql_query = kwargs.get("sql_query")
        table_name = kwargs.get("table_name")
        data: Optional[pd.DataFrame] = None
        if self.db_conn.multi_table:
            # If data is multi-table, `data.table_names` can't be None
            assert self.db_conn.table_names is not None  # nosec
            if sql_query:
                data = pd.read_sql_query(sql=sql_query, con=self.db_conn.con)
            elif table_name:
                data = pd.read_sql_table(table_name=table_name, con=self.con)
        elif self.db_conn.query:
            data = pd.read_sql_query(sql=self.db_conn.query, con=self.db_conn.con)
        else:
            # If the data is not multi-table and there is no query, there must
            # necessarily be one table name. Reassuring mypy of this.
            assert self.db_conn.table_names is not None  # nosec
            assert len(self.db_conn.table_names) == 1  # nosec
            data = pd.read_sql_table(
                table_name=self.db_conn.table_names[0],
                con=self.con,
                schema=self.db_conn.db_schema,
            )
        self.data = data
        return data

    def get_dtypes(self, **kwargs: Any) -> _Dtypes:
        """Loads and returns the columns and column types from the Database dataset.

        Args:
            table_name: The name of the column which should be loaded. Only
                required for multitable database.

        Returns:
            A mapping from column names to column types.
        """
        table_name = kwargs.get("table_name")
        metadata = MetaData(self.con)
        dtypes: _Dtypes
        if self.query is not None:
            with Session(self.con) as session:
                result = session.execute(self.query).fetchone()
            data = pd.DataFrame([result])
            dtypes = data.convert_dtypes().dtypes.to_dict()

        else:
            table_name = self._validate_table_name(table_name)

            table = Table(
                table_name,
                metadata,
                schema=self.db_conn.db_schema,
                autoload=True,
                autoload_with=self.db_conn.con,
            )
            dtypes = {col.name: np.dtype(col.type.python_type) for col in table.columns}

        return dtypes


class DataSource:
    """DataSource class which encapsulates data.

    Args:
        data_ref: The reference of the data to load.
        data_splitter: Approach used for splitting the data into training, test,
            validation. Defaults to None.
        seed: Random number seed. Used for setting random seed for all libraries.
            Defaults to None.
        modifiers: Dictionary used for modifying paths/ extensions in the dataframe.
            Defaults to None.
        ignore_cols: Column/list of columns to be ignored from the data.
            Defaults to None.
        **kwargs: Additional keyword arguments to be passed to the underlying function
            which loads the data.

    Attributes:
        data: A Dataframe-type object which contains the data.
        data_ref: The reference of the data to load.
        data_splitter: Approach used for splitting the data into training, test,
            validation.
        seed: Random number seed. Used for setting random seed for all libraries.
        train_idxs: A numpy array containing the indices of the data which
            will be used for training.
        validation_idxs: A numpy array containing the indices of the data which
            will be used for validation.
        test_idxs: A numpy array containing the indices of the data which
            will be used for testing.

    Raises:
        TypeError: If data format is not supported.
        ValueError: If `image_col` is specified but can't be found in `data`.
        ValueError: If both `ignore_cols` and `selected_cols` are specified.
    """

    def __init__(
        self,
        data_ref: Union[os.PathLike, AnyUrl, DatabaseConnection, pd.DataFrame],
        data_splitter: Optional[_DatasetSplitter] = None,
        seed: Optional[int] = None,
        modifiers: Optional[Dict[str, DataPathModifiers]] = None,
        ignore_cols: Optional[Union[str, Sequence[str]]] = None,
        **kwargs: Any,
    ):
        self.data_ref = data_ref
        self._kwargs = kwargs
        self.data: pd.DataFrame
        self.loader = self.get_loader()
        self._data_is_split: bool = False
        self._data_is_loaded: bool = False
        self.seed = seed
        self._ignore_cols = ignore_cols
        self._modifiers = modifiers
        seed_all(self.seed)

        self.train_idxs: Optional[np.ndarray] = None
        self.validation_idxs: Optional[np.ndarray] = None
        self.test_idxs: Optional[np.ndarray] = None
        self._table_hashes: Set[str] = set()

        self.data_splitter = data_splitter

    @property
    def multi_table(self) -> bool:
        """Attribute to specify whether the datasource is multi table."""
        if isinstance(self.data_ref, DatabaseConnection):
            return self.data_ref.multi_table
        else:
            return False

    @property
    def hash(self) -> str:
        """The hash associated with this DataSource.

        This is the hash of the static information regarding the underlying DataFrame,
        primarily column names and content types but NOT anything content-related
        itself. It should be consistent across invocations, even if additional data
        is added, as long as the DataFrame is still compatible in its format.

        Returns:
            The hexdigest of the DataFrame hash.
        """
        if not self._table_hashes:
            raise DataNotLoadedError(
                "Data is not loaded yet. Please call `get_dtypes` first."
            )
        else:
            return _hash_str(str(sorted(self._table_hashes)))

    def get_loader(self) -> _BaseLoader:
        """Determine loader based on the type of the `data_ref`."""
        loader: _BaseLoader
        if isinstance(self.data_ref, (os.PathLike, AnyUrl, str)):
            if not str(self.data_ref).endswith(".csv"):
                raise TypeError("Please provide a Path or URL to a CSV file.")
            loader = CSVLoader(self.data_ref)
        elif isinstance(self.data_ref, pd.DataFrame):
            loader = DataFrameLoader(self.data_ref)
        elif isinstance(self.data_ref, DatabaseConnection):
            loader = DatabaseLoader(self.data_ref)
        else:
            raise TypeError(f"Can't read data of type {type(self.data_ref)}")
        return loader

    def _modify_column(
        self,
        column: Union[np.ndarray, pd.Series],
        modifier_dict: DataPathModifiers,
    ) -> Union[np.ndarray, pd.Series]:
        """Modify the given column.

        Args:
            column: The column you are operating on.
            modifier_dict: A dictionary with the key as the
            prefix/suffix and the value to be prefixed/suffixed.
        """
        # Get the modifier dictionary:
        for modifier_type, modifier_string in modifier_dict.items():
            if modifier_type == "prefix":
                column = modifier_string + column.astype(str)

            elif modifier_type == "suffix":
                column = column.astype(str) + modifier_string
        return column

    def _modify_file_paths(self, modifiers: Dict[str, DataPathModifiers]) -> None:
        """Modifies image file paths if provided.

        Args:
            modifiers: A dictionary with the column name and
            prefix and/or suffix to modify file path.
        """
        for column_name in modifiers.keys():
            # Get the modifier dictionary:
            modifier_dict = modifiers[column_name]
            self.data[column_name] = self._modify_column(
                self.data[column_name], modifier_dict
            )

    def _get_data(
        self, sql_query: Optional[str] = None, table_name: Optional[str] = None
    ) -> Optional[pd.DataFrame]:
        """Loads and returns data.

        Args:
            sql_query: A SQL query string required for multi table data sources.

        Returns:
            A DataFrame-type object which contains the data.
        """
        data = self.loader.get_data(sql_query=sql_query, table_name=table_name)
        return data

    def get_features(self) -> List[str]:
        """Returns the features of the data.

        Returns:
            A list of the feature names in the data.

        Raises:
            DataNotLoadedError: If data is not loaded.
        """
        if self._data_is_loaded:
            feature_names: List[str] = self.data.columns
            return feature_names

        raise DataNotLoadedError(
            "Data is not loaded yet. Please call `load_data` first."
        )

    def get_dtypes(self, table_name: Optional[str] = None) -> _Dtypes:
        """Loads and returns the columns and column types of the data.

        Args:
            table_name: The name of the column which should be loaded. Only
                required for multitable database.

        Returns:
            A mapping from column names to column types.
        """
        dtypes: _Dtypes = self.loader.get_dtypes(table_name=table_name)
        if self.loader.data is not None:
            self.data = self.loader.data
            self._data_is_loaded = True

        if self._ignore_cols:
            if isinstance(self._ignore_cols, str):
                self._ignore_cols = [self._ignore_cols]
            for col in self._ignore_cols:
                if col in dtypes.keys():
                    del dtypes[col]
        self._table_hashes.add(_generate_dtypes_hash(dtypes))
        return dtypes

    def get_values(
        self, col_names: List[str], table_name: Optional[str] = None
    ) -> Dict[str, Iterable[Any]]:
        """Get distinct values from columns in data.

        Args:
            col_names: The list of the column whose distinct values should be
                returned.
            table_name: The name of the table to which the column exists. Required
                for multi-table databases.

        Returns:
            The distinct values of the requested column as a mapping from col name to
            a series of distinct values.
        """
        return self.loader.get_values(col_names=col_names, table_name=table_name)

    def get_column(
        self, col_name: str, table_name: Optional[str] = None
    ) -> Union[np.ndarray, pd.Series]:
        """Loads and returns single column from dataset.

        Args:
            col_name: The name of the column which should be loaded.
            table_name: The name of the table to which the column exists. Required
                for multi-table databases.

        Returns:
            The column request as a series.
        """
        column = self.loader.get_column(col_name=col_name, table_name=table_name)
        if self._modifiers:
            if modifier_dict := self._modifiers.get(col_name):
                column = self._modify_column(column, modifier_dict)
        return column

    def load_data(
        self, sql_query: Optional[str] = None, table_name: Optional[str] = None
    ) -> None:
        """Load the data for the datasource.

        This method is idempotent so it can be called multiple times without
        reloading the data.

        Raises:
            TypeError: If data format is not supported.#
        """
        if not self._data_is_loaded:
            data = self._get_data(sql_query=sql_query, table_name=table_name)
            if not self.multi_table:
                assert data is not None  # nosec
            if data is not None:
                # If _ignore_cols is set on the datasource should
                # we ignore them even if they are selected in
                # the sql_query? I am assuming yes here.
                if self._ignore_cols:
                    if isinstance(self._ignore_cols, str):
                        self._ignore_cols = [self._ignore_cols]
                    for col in self._ignore_cols:
                        # If columns already ignored in data, ignore errors.
                        data = data.drop(col, axis=1, errors="ignore")

                self.data = data

                if self._modifiers:
                    self._modify_file_paths(self._modifiers)

                self._data_is_loaded = True

    @property
    def train_set(self) -> pd.DataFrame:
        """Train set portion of `self.data`.

        Returns:
            A dataframe-type object containing the data points with indices
            from the `self.train_idxs`.The indices will be reset in this train set.

        Raises:
            DataNotSplitError: If the data has not been split.
        """
        if self.train_idxs is None:
            raise DataNotSplitError("No train set exists. Split the data first.")

        train_df: pd.DataFrame = self.data.loc[self.train_idxs.tolist()]
        train_df = train_df.reset_index(drop=True)
        return train_df

    @property
    def validation_set(self) -> pd.DataFrame:
        """Validation set portion of `self.data`.

        Returns:
            A dataframe-type object containing the data points with indices
            from the `self.validation_idxs`.The indices will be reset
            in this validation set.

        Raises:
            DataNotSplitError: If the data has not been split.
        """
        if self.validation_idxs is None:
            raise DataNotSplitError("No validation set exists. Split the data first.")

        validation_df: pd.DataFrame = self.data.loc[self.validation_idxs.tolist()]
        validation_df = validation_df.reset_index(drop=True)
        return validation_df

    @property
    def test_set(self) -> pd.DataFrame:
        """Test set portion of `self.data`.

        Returns:
            A dataframe-type object containing the data points with indices
            from the `self.test_idxs`.The indices will be reset in this test set.

        Raises:
            DataNotSplitError: If the data has not been split.
        """
        if self.test_idxs is None:
            raise DataNotSplitError("No test set exists. Split the data first.")

        test_df: pd.DataFrame = self.data.loc[self.test_idxs.tolist()]
        test_df = test_df.reset_index(drop=True)
        return test_df
