"""Tests datasource.py."""
from functools import partial
import logging
from pathlib import Path
import re
from typing import Callable, Tuple
from unittest.mock import Mock

from _pytest.logging import LogCaptureFixture
import numpy as np
import pandas as pd
import pytest
from pytest import fixture
from pytest_mock import MockerFixture
import sqlalchemy

from bitfount.data.databunch import _BitfountDataBunch
from bitfount.data.datasource import DataSource
from bitfount.data.datasplitters import _DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.data.exceptions import DataNotLoadedError, DataNotSplitError
from bitfount.data.schema import TableSchema
from bitfount.data.types import DataPathModifiers
from bitfount.data.utils import DatabaseConnection, _hash_str
from tests.utils import PytestRequest
from tests.utils.helper import (
    DATASET_ROW_COUNT,
    TABLE_NAME,
    create_dataset,
    create_datastructure,
    integration_test,
    unit_test,
)


class FakeSplitter(_DatasetSplitter):
    """Fake Splitter that just returns predefined indices."""

    def __init__(
        self,
        train_indices: np.ndarray,
        validation_indices: np.ndarray,
        test_indices: np.ndarray,
    ):
        self.train_indices = train_indices
        self.validation_indices = validation_indices
        self.test_indices = test_indices

    @classmethod
    def splitter_name(cls) -> str:
        """Splitter name for config."""
        return "FakeSplitter"

    def create_dataset_splits(
        self, data: pd.DataFrame
    ) -> Tuple[np.ndarray, np.ndarray, np.ndarray]:
        """Returns predefined indices and provided data."""
        return self.train_indices, self.validation_indices, self.test_indices


@fixture
def datastructure() -> DataStructure:
    """Fixture for datastructure."""
    return create_datastructure()


@fixture
def mock_databunch(mocker: MockerFixture) -> None:
    """Mocked _BitfountDataBunch."""
    mocker.patch.object(_BitfountDataBunch, "create_datasets", autospec=True)


@unit_test
class TestDataSource:
    """Tests core DataSource functionality with a CSV file."""

    @fixture(scope="function", params=["pandas", "image"])
    def datasource_generator(self, request: PytestRequest) -> Callable[..., DataSource]:
        """Dataset loader for use in tests."""
        image = False
        if request.param == "image":
            image = True
        data = create_dataset(image=image)
        if image:
            return partial(DataSource, data_ref=data, seed=420)

        return partial(DataSource, data_ref=data, seed=420)

    def test_training_set(
        self,
        datastructure: DataStructure,
        datasource_generator: Callable[..., DataSource],
        mock_databunch: None,
    ) -> None:
        """Checks training set is behaving correctly."""
        test_percentage = 25
        validation_percentage = 55
        train_percentage = (100 - test_percentage) - validation_percentage
        data_source = datasource_generator(
            data_splitter=FakeSplitter(
                np.array(range(int(DATASET_ROW_COUNT * (train_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (validation_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (test_percentage / 100)))),
            )
        )
        data_source.load_data()
        # split data in DataBunch into training, validation, test sets
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), data_source)
        # assert columns match the original data
        assert data_source.data.shape[1] == data_source.train_set.shape[1]
        # assert there are the expected number of rows
        assert (
            int(train_percentage * data_source.data.shape[0] / 100)
            == data_source.train_set.shape[0]
        )

    def test_validation_set(
        self,
        datastructure: DataStructure,
        datasource_generator: Callable[..., DataSource],
        mock_databunch: None,
    ) -> None:
        """Checks validation set is behaving correctly."""
        test_percentage = 25
        validation_percentage = 55
        train_percentage = (100 - test_percentage) - validation_percentage
        data_source = datasource_generator(
            data_splitter=FakeSplitter(
                np.array(range(int(DATASET_ROW_COUNT * (train_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (validation_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (test_percentage / 100)))),
            )
        )
        data_source.load_data()
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), data_source)
        # assert columns match the original data
        assert data_source.data.shape[1] == data_source.validation_set.shape[1]
        # assert there are the expected number of rows
        assert (
            int(validation_percentage * data_source.data.shape[0] / 100)
            == data_source.validation_set.shape[0]
        )

    def test_test_set(
        self,
        datastructure: DataStructure,
        datasource_generator: Callable[..., DataSource],
        mock_databunch: None,
    ) -> None:
        """Checks test set is behaving correctly."""
        test_percentage = 25
        validation_percentage = 55
        train_percentage = (100 - test_percentage) - validation_percentage
        data_source = datasource_generator(
            data_splitter=FakeSplitter(
                np.array(range(int(DATASET_ROW_COUNT * (train_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (validation_percentage / 100)))),
                np.array(range(int(DATASET_ROW_COUNT * (test_percentage / 100)))),
            )
        )
        data_source.load_data()
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), data_source)
        # assert columns match the original data
        assert data_source.data.shape[1] == data_source.test_set.shape[1]
        # assert there are the expected number of rows
        assert (
            int(test_percentage * data_source.data.shape[0] / 100)
            == data_source.test_set.shape[0]
        )

    def test_zero_validation_test_size(
        self,
        datasource_generator: Callable[..., DataSource],
        datastructure: DataStructure,
        mock_databunch: None,
    ) -> None:
        """Checks Dataset object behaves properly when if valid and test pct are 0."""
        data_source = datasource_generator(
            data_splitter=FakeSplitter(
                train_indices=np.array(range(DATASET_ROW_COUNT)),
                validation_indices=np.array([]),
                test_indices=np.array([]),
            )
        )
        data_source.load_data()
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), data_source)
        assert len(data_source.data) == len(data_source.train_set)
        assert data_source.test_idxs is not None
        assert data_source.validation_idxs is not None
        assert len(data_source.test_idxs) == 0
        assert len(data_source.validation_idxs) == 0

    def test_tabular_datasource_errors(self) -> None:
        """Checks DataSource object errors via wrong first argument."""
        with pytest.raises(TypeError):
            DataSource("test1", seed=420).load_data()  # type: ignore[arg-type] # Reason: purpose of test # noqa: B950

        with pytest.raises(TypeError):
            test_path = Path("/my/root/directory")
            DataSource(test_path, seed=420).load_data()

    def test_datasource_modifiers_path_prefix(self) -> None:
        """Tests functionality for providing image path prefix."""
        data = create_dataset()
        data["image"] = "image_file_name"
        modifiers = {"image": DataPathModifiers({"prefix": "/path/to/"})}
        dataset = DataSource(data_ref=data, seed=420, modifiers=modifiers)
        dataset.load_data()
        assert len(dataset.data["image"].unique()) == 1
        assert dataset.data["image"].unique()[0] == "/path/to/image_file_name"

    def test_image_datasource_ext_suffix(self) -> None:
        """Tests functionality for finding images by file extension."""
        data = create_dataset()
        data["image"] = "image_file_name"
        modifiers = {"image": DataPathModifiers({"suffix": ".jpeg"})}
        dataset = DataSource(data_ref=data, seed=420, modifiers=modifiers)
        dataset.load_data()
        assert len(dataset.data["image"].unique()) == 1
        assert dataset.data["image"].unique()[0] == "image_file_name.jpeg"

    def test_image_datasource_ext_prefix_suffix(self) -> None:
        """Tests functionality for finding images by file extension."""
        data = create_dataset()
        data["image"] = "image_file_name"
        modifiers = {
            "image": DataPathModifiers({"prefix": "/path/to/", "suffix": ".jpeg"})
        }
        dataset = DataSource(data_ref=data, seed=420, modifiers=modifiers)
        dataset.load_data()
        assert len(dataset.data["image"].unique()) == 1
        assert dataset.data["image"].unique()[0] == "/path/to/image_file_name.jpeg"

    def test_multiple_img_datasource_modifiers(self) -> None:
        """Tests functionality for finding multiple images by file extension."""
        data = create_dataset(multiimage=True, img_size=1)
        data["image1"] = "image1_file_name"
        data["image2"] = "image2_file_name"
        modifiers = {
            "image1": DataPathModifiers({"prefix": "/path/to/"}),
            "image2": DataPathModifiers({"suffix": ".jpeg"}),
        }
        dataset = DataSource(data_ref=data, seed=420, modifiers=modifiers)
        dataset.load_data()
        assert len(dataset.data["image1"].unique()) == 1
        assert dataset.data["image1"].unique()[0] == "/path/to/image1_file_name"
        assert len(dataset.data["image2"].unique()) == 1
        assert dataset.data["image2"].unique()[0] == "image2_file_name.jpeg"

    def test_tabular_datasource_read_csv_correctly(self, tmp_path: Path) -> None:
        """Tests DataSource loading from csv."""
        file_path = tmp_path / "tabular_data_test.csv"
        data = create_dataset()
        data.to_csv(file_path)
        ds = DataSource(file_path)
        ds.load_data()
        assert hasattr(ds, "data")

    def test_ignored_cols_list_excluded_from_df(self) -> None:
        """Tests that a list of ignore_cols are ignored in the data."""
        data = create_dataset()
        data["image"] = "image_file_name"
        ignore_cols = ["N", "O", "P"]
        dataset = DataSource(
            data_ref=data,
            seed=420,
            ignore_cols=ignore_cols,
            image_col=["image"],
            image_extension="jpeg",
        )
        dataset.load_data()
        assert not any(item in dataset.data.columns for item in ignore_cols)

    def test_ignored_single_col_list_excluded_from_df(self) -> None:
        """Tests that a str ignore_cols is ignored in the data."""
        data = create_dataset()
        data["image"] = "image_file_name"
        ignore_cols = "N"
        dataset = DataSource(
            data_ref=data,
            seed=420,
            ignore_cols=ignore_cols,
            image_col=["image"],
            image_extension="jpeg",
        )
        dataset.load_data()
        assert ignore_cols not in dataset.data.columns

    def test_hash(
        self, datasource_generator: Callable[..., DataSource], mocker: MockerFixture
    ) -> None:
        """Tests hash is called on the dtypes."""
        datasource = datasource_generator()
        expected_hash = f"hash_{id(datasource._table_hashes)}"
        mock_hash_function: Mock = mocker.patch(
            "bitfount.data.datasource._generate_dtypes_hash",
            return_value=expected_hash,
            autospec=True,
        )
        datasource.get_dtypes()

        actual_hash = datasource.hash

        # Check hash is expected return and how it was called
        assert actual_hash == _hash_str(str([expected_hash]))
        mock_hash_function.assert_called_once()

    def test_datasource_data_split_flag_updated(
        self, datastructure: DataStructure, mock_databunch: None
    ) -> None:
        """Tests that the data_is_split flag is updated."""
        data = create_dataset()
        ds = DataSource(data, selected_cols=["M", "F"])
        ds.load_data()
        assert ds._data_is_split is False
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), ds)
        assert ds._data_is_split is True

    def test_datasource_data_split_called_twice(
        self,
        datastructure: DataStructure,
        caplog: LogCaptureFixture,
        mock_databunch: None,
    ) -> None:
        """Tests that the log is printed if split_data called twice."""
        caplog.set_level(logging.INFO)
        data = create_dataset()
        ds = DataSource(data, selected_cols=["M", "F"])
        ds.load_data()
        assert ds._data_is_split is False
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), ds)
        assert ds._data_is_split is True
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), ds)
        assert "Data is already split, resuming with the current split." in caplog.text


class TestDatabaseConnectionDataSource:
    """Tests DataSource with a DatabaseConnection."""

    @integration_test
    def test_database_single_table_input(
        self,
        datastructure: DataStructure,
        db_session: sqlalchemy.engine.base.Engine,
        mock_databunch: None,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Single table database connection.
        """
        db_conn = DatabaseConnection(db_session, table_names=["dummy_data"])
        dataset = DataSource(db_conn, seed=420)
        dataset.load_data()
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), dataset)
        assert dataset.data is not None
        assert not dataset.multi_table
        assert dataset.train_idxs is not None
        assert dataset.validation_idxs is not None
        assert dataset.test_idxs is not None
        assert len(dataset.train_idxs) + len(dataset.validation_idxs) + len(
            dataset.test_idxs
        ) == len(dataset.data)

    @unit_test
    def test_mock_database_single_table_input(
        self,
        datastructure: DataStructure,
        mock_engine: Mock,
        mock_pandas_read_sql_table: None,
        mock_databunch: None,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Mock single table database connection.
        """
        db_conn = DatabaseConnection(mock_engine, table_names=["dummy_data"])
        dataset = DataSource(db_conn, seed=420)
        dataset.load_data()
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), dataset)
        assert dataset.data is not None
        assert not dataset.multi_table
        assert dataset.train_idxs is not None
        assert dataset.validation_idxs is not None
        assert dataset.test_idxs is not None
        assert len(dataset.train_idxs) + len(dataset.validation_idxs) + len(
            dataset.test_idxs
        ) == len(dataset.data)

    @integration_test
    def test_database_multi_table_input(
        self,
        db_session: sqlalchemy.engine.base.Engine,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Multi-table database connection.
        """
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )

        dataset = DataSource(db_conn, seed=420)

        # Test when load_data is called without query
        # DataSource has no data attribute
        dataset.load_data()
        assert not hasattr(dataset, "data")
        # Test when load_data is called WITH query
        # DataSource has no data attribute
        query = "SELECT 'Date', 'TARGET' FROM dummy_data"
        dataset.load_data(query)
        assert hasattr(dataset, "data")
        expected_output = pd.read_sql(query, con=db_conn.con)
        pd.testing.assert_frame_equal(dataset.data, expected_output)
        assert dataset.multi_table

    @unit_test
    def test_database_multi_table_input_table_name(
        self,
        db_session: sqlalchemy.engine.base.Engine,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Multi-table database connection, load single table.
        """
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )

        dataset = DataSource(db_conn, seed=420)

        # Test when load_data is called without query
        # DataSource has no data attribute
        dataset.load_data()
        assert not hasattr(dataset, "data")
        # Test when load_data is called WITH query
        # DataSource has no data attribute
        table_name = "dummy_data"
        dataset.load_data(table_name=table_name)
        assert hasattr(dataset, "data")

    @unit_test
    def test_mock_database_multi_table_input(
        self, mock_engine: Mock, mocker: MockerFixture
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Mock multi-table database connection.
        """
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        dataset = DataSource(db_conn, seed=420)
        # Test when load_data is called without query
        # DataSource has no data attribute
        dataset.load_data()
        assert not hasattr(dataset, "data")
        # Test when load_data is called WITH query
        # DataSource has no data attribute
        query = "SELECT 'Date', 'TARGET' FROM dummy_data"
        read_sql_mock = mocker.patch.object(pd, "read_sql_query")
        dataset.load_data(sql_query=query)
        assert hasattr(dataset, "data")
        read_sql_mock.assert_called_once_with(sql=query, con=mock_engine)
        assert dataset.multi_table

    @integration_test
    def test_database_query_input(
        self,
        datastructure: DataStructure,
        db_session: sqlalchemy.engine.base.Engine,
        mock_databunch: None,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Query database connection.
        """
        db_conn = DatabaseConnection(
            db_session,
            query="""
            SELECT *
            FROM dummy_data d1
            LEFT JOIN dummy_data_2 d2
            ON 'd1.Date' = 'd2.Date'
            """,
        )
        dataset = DataSource(db_conn, seed=420)
        dataset.load_data()
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), dataset)
        assert not dataset.multi_table
        assert dataset.data is not None
        assert dataset.train_idxs is not None
        assert dataset.validation_idxs is not None
        assert dataset.test_idxs is not None
        assert len(dataset.train_idxs) + len(dataset.validation_idxs) + len(
            dataset.test_idxs
        ) == len(dataset.data)

    @integration_test
    @pytest.mark.parametrize(
        "query",
        [
            'SELECT "Date", "TARGET" FROM blah',
            'SELECT "invalid", FROM blah',
            '"invalid" from blah',
        ],
    )
    def test_database_query_sql_error(
        self, db_session: sqlalchemy.engine.base.Engine, query: str
    ) -> None:
        """Checks DataSource raises sqlalchemy error."""
        db_conn = DatabaseConnection(
            db_session,
            table_names=["dummy_data", "dummy_data_2"],
        )

        dataset = DataSource(db_conn, seed=420)
        with pytest.raises(sqlalchemy.exc.ProgrammingError):
            dataset.load_data(sql_query=query)

    @unit_test
    def test_mock_database_query_input(
        self,
        datastructure: DataStructure,
        mock_engine: Mock,
        mock_pandas_read_sql_query: None,
        mock_databunch: None,
    ) -> None:
        """Checks DataSource initialises correctly with `DatabaseConnection`.

        Mock query database connection.
        """
        db_conn = DatabaseConnection(
            mock_engine,
            query="""
            SELECT *
            FROM dummy_data d1
            LEFT JOIN dummy_data_2 d2
            ON 'd1.Date' = 'd2.Date'
            """,
        )
        dataset = DataSource(db_conn, seed=420)
        dataset.load_data()
        # split data in DataBunch into training, validation, test sets
        _BitfountDataBunch(datastructure, TableSchema(TABLE_NAME), dataset)
        assert not dataset.multi_table
        assert dataset.data is not None
        assert dataset.train_idxs is not None
        assert dataset.validation_idxs is not None
        assert dataset.test_idxs is not None
        assert len(dataset.train_idxs) + len(dataset.validation_idxs) + len(
            dataset.test_idxs
        ) == len(dataset.data)

    @unit_test
    def test_hash_multitable_raises_value_error(self, mock_engine: Mock) -> None:
        """Tests hash function raises `DataNotLoadedError` if data is not loaded."""
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        dataset = DataSource(db_conn, seed=420)
        with pytest.raises(DataNotLoadedError):
            dataset.hash

    @unit_test
    def test_training_set_unsplit_raises_value_error(self, mock_engine: Mock) -> None:
        """Tests that calling the `training_set` property raises an error.

        The error should be a `DataNotSplitError` when the data has not been split yet.
        """
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        dataset = DataSource(db_conn, seed=420)
        dataset.load_data()
        with pytest.raises(DataNotSplitError):
            dataset.train_set

    @unit_test
    def test_validation_set_unsplit_raises_value_error(self, mock_engine: Mock) -> None:
        """Tests that calling the `validation_set` property raises an error.

        The error should be a `DataNotSplitError` when the data has not been split yet.
        """
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        dataset = DataSource(db_conn, seed=420)
        dataset.load_data()
        with pytest.raises(DataNotSplitError):
            dataset.validation_set

    @unit_test
    def test_test_set_unsplit_raises_value_error(self, mock_engine: Mock) -> None:
        """Tests that calling the `test_set` property raises an error.

        The error should be a `DataNotSplitError` when the data has not been split yet.
        """
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        dataset = DataSource(db_conn, seed=420)
        dataset.load_data()
        with pytest.raises(DataNotSplitError):
            dataset.test_set

    @unit_test
    def test_value_error_raised_if_no_table_name_provided_for_multitable_datasource(
        self, mock_engine: Mock
    ) -> None:
        """Tests ValueError raised if table_name missing for multi-table DataSource."""
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DataSource(db_conn, seed=420)
        ds.load_data()
        with pytest.raises(
            ValueError, match="No table name provided for multi-table datasource."
        ):
            ds.get_dtypes()

    @unit_test
    def test_value_error_raised_if_table_not_found_for_multitable_datasource(
        self, mock_engine: Mock
    ) -> None:
        """Tests ValueError raised if table is missing for multi-table DataSource."""
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DataSource(db_conn, seed=420)
        ds.load_data()
        with pytest.raises(
            ValueError,
            match=re.escape(
                "Table name not_a_table not found in the data. "
                + "Available tables: ['dummy_data', 'dummy_data_2']"
            ),
        ):
            ds.get_dtypes("not_a_table")

    @unit_test
    def test_mock_get_dtypes_reads_and_returns_table_schema(
        self, mock_engine: Mock, mocker: MockerFixture
    ) -> None:
        """Tests that the `get_dtypes` method returns a dictionary.

        Also checks that the dtypes hash is added appropriately.
        """
        db_conn = DatabaseConnection(
            mock_engine, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DataSource(db_conn, seed=420)
        mocker.patch.object(ds.loader, "get_dtypes", return_value={})

        assert len(ds._table_hashes) == 0
        assert isinstance(ds.get_dtypes("dummy_data"), dict)
        assert len(ds._table_hashes) == 1

    @integration_test
    def test_get_dtypes_reads_and_returns_table_schema(
        self, db_session: sqlalchemy.engine.base.Engine
    ) -> None:
        """Tests that the `get_dtypes` method returns a dictionary.

        Also checks that the dtypes hash is added appropriately.
        """
        db_conn = DatabaseConnection(
            db_session, table_names=["dummy_data", "dummy_data_2"]
        )
        ds = DataSource(db_conn, seed=420)
        assert len(ds._table_hashes) == 0
        table = ds.get_dtypes("dummy_data")
        assert isinstance(table, dict)
        assert len(ds._table_hashes) == 1
