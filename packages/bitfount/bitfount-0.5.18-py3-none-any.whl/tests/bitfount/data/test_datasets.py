"""Test dataset classes in data/datasets.py."""

from typing import Iterator, cast
from unittest.mock import Mock

from PIL import Image
import numpy as np
import pandas as pd
import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount.data.datasets import _BitfountDataset, _IterableBitfountDataset
from bitfount.data.datasource import DatabaseLoader, DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import SemanticType
from bitfount.data.utils import DatabaseConnection
from tests.utils.helper import DATASET_ROW_COUNT, TABLE_NAME, create_dataset, unit_test


@unit_test
class TestDataset:
    """Tests for Dataset class."""

    @fixture
    def dataframe(self) -> pd.DataFrame:
        """Underlying dataframe for single image datasets."""
        return create_dataset(image=True)

    def test_len_tab_data(
        self, dataframe: pd.DataFrame, tabular_dataset: _BitfountDataset
    ) -> None:
        """Tests tabular dataset __len__ method."""
        assert len(tabular_dataset) == len(dataframe)

    def test_len_img_data(
        self, dataframe: pd.DataFrame, image_tab_dataset: _BitfountDataset
    ) -> None:
        """Tests image dataset __len__ method."""
        assert len(image_tab_dataset) == len(dataframe)

    def test_len_img_tab_data(
        self, dataframe: pd.DataFrame, image_dataset: _BitfountDataset
    ) -> None:
        """Tests dataset __len__ method."""
        assert len(image_dataset) == len(dataframe)

    def test_len_multiimg_data(
        self, multiimage_dataframe: pd.DataFrame, multiimage_dataset: _BitfountDataset
    ) -> None:
        """Tests multi-image dataset __len__ method."""
        assert len(multiimage_dataset) == len(multiimage_dataframe)

    def test_batch_transformation_step_missing_raises_value_error(
        self, dataframe: pd.DataFrame
    ) -> None:
        """Tests that a ValueError is raised if batch transformation step is missing."""
        target = "TARGET"
        datasource = DataSource(dataframe)
        datasource.load_data()
        schema = BitfountSchema()
        schema.add_datasource_tables(
            datasource,
            force_stypes={TABLE_NAME: {"image": ["image"]}},
            table_name=TABLE_NAME,
        )
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.get_feature_names(TABLE_NAME, SemanticType.TEXT)
        )
        datastructure = DataStructure(
            target=target,
            selected_cols=["image", target],
            image_cols=["image"],
            table=TABLE_NAME,
        )
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        with pytest.raises(ValueError):
            _BitfountDataset(
                data=datasource.data,
                target=target,
                selected_cols=datastructure.selected_cols_w_types,
                batch_transforms=datastructure.get_batch_transformations(),
            )

    def test_transform_image(self, image_dataset: _BitfountDataset) -> None:
        """Test transform_image method."""
        assert image_dataset.batch_transforms is not None
        img_array = np.array(Image.new("RGB", size=(224, 224), color=(55, 100, 2)))
        transformed_image = image_dataset._transform_image(img_array, 0)
        assert isinstance(transformed_image, np.ndarray)
        assert transformed_image.shape == (224, 224, 3)

        # Assert that the transformed image is not the same as the original
        with pytest.raises(AssertionError):
            np.testing.assert_array_equal(img_array, transformed_image)

    def test_load_image(self, image_dataset: _BitfountDataset) -> None:
        """Test transform_image method."""
        loaded_transformed_image = image_dataset._load_images(0)
        assert isinstance(loaded_transformed_image, np.ndarray)
        assert loaded_transformed_image.shape == (224, 224, 3)

    # The below comment can be removed unless anyone thinks we need more tests.
    # TODO: [BIT-983] Add non-backend dataset tests


class TestIterableDataset:
    """Tests for Iterable Dataset class."""

    @fixture
    def dataframe(self) -> pd.DataFrame:
        """Underlying dataframe for tabular datasets."""
        return create_dataset()

    @unit_test
    def test_len_magic_method(self, mock_engine: Mock, mocker: MockerFixture) -> None:
        """Tests that __len__ magic method returns correct row count."""
        # Mocks `execute` method on the SQLAlchemy connection object and the
        # `scalar_one` method on the resulting cursor result to return the
        # dataset row count
        mock_db_connection = Mock()
        mock_result = Mock()
        mock_result.scalar_one.return_value = DATASET_ROW_COUNT
        mock_db_connection.execute.return_value = mock_result

        # Creates a multitable DatabaseConnection object
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        # Mocks `connect` method and resulting context manager on SQLAlchemy Engine
        mocker.patch.object(
            db_conn.con, "connect"
        ).return_value.__enter__.return_value = mock_db_connection

        # Creates DataSource and _IterableBitfountDataset objects
        ds = DataSource(db_conn, seed=420)
        dataset = _IterableBitfountDataset(
            cast(DatabaseLoader, ds.get_loader()),
            sql_query="SELECT * FROM doesntmatter",
            selected_cols={"continuous": ["columns", "dont", "matter"]},
        )

        # Calls __len__ method on dataset
        dataset_length = len(dataset)

        # Makes assertions on call stack in order
        # Ignoring mypy errors because `connect` has been patched to return a Mock
        db_conn.con.connect.assert_called_once()  # type: ignore[attr-defined] # Reason: see above # noqa: B950
        db_conn.con.connect.return_value.__enter__.assert_called_once()  # type: ignore[attr-defined]  # Reason: see above # noqa: B950
        mock_db_connection.execute.assert_called_once()
        mock_result.scalar_one.assert_called_once()

        # Makes assertion on final result
        assert dataset_length == DATASET_ROW_COUNT

    @unit_test
    def test_iter_magic_method(
        self, mock_engine: Mock, mocker: MockerFixture, dataframe: pd.DataFrame
    ) -> None:
        """Tests that __iter__ magic method works as expected."""
        # Mocks `execute` method on the SQLAlchemy connection object and the
        # `scalar_one` method on the resulting cursor result to return the
        # dataset row count
        mock_db_connection = Mock()
        mock_result = Mock()

        class MockPartition:
            """Mock class to represent database result paritions."""

            def __iter__(self) -> Iterator[np.ndarray]:
                """Iterator just returns one set of dataframe values."""
                for i in [dataframe.values]:
                    yield i

        mock_result.partitions.return_value = MockPartition()
        mock_result.keys.return_value = dataframe.columns
        mock_db_connection.execution_options.return_value = mock_db_connection
        mock_db_connection.execute.return_value = mock_result

        # Creates a multitable DatabaseConnection object
        db_conn = DatabaseConnection(
            mock_engine,
            table_names=["dummy_data", "dummy_data_2"],
        )
        # Mocks `connect` method and resulting context manager on SQLAlchemy Engine
        mocker.patch.object(
            db_conn.con, "connect"
        ).return_value.__enter__.return_value = mock_db_connection

        # Creates DataSource and _IterableBitfountDataset objects
        ds = DataSource(db_conn, seed=420)
        dataset = _IterableBitfountDataset(
            cast(DatabaseLoader, ds.get_loader()),
            sql_query="SELECT * FROM doesntmatter",
            selected_cols={"continuous": ["A", "E", "H"]},
        )

        # Calls __iter__ method on dataset
        dataset_iterator = iter(dataset)
        x, y = next(dataset_iterator)  # First output of iterator
        assert len(x) == 2
        assert isinstance(x, tuple)
        assert isinstance(x[0], np.ndarray)
        assert isinstance(y, np.ndarray)

        # Makes assertions on call stack in order
        # Ignoring mypy errors because `connect` has been patched to return a Mock
        db_conn.con.connect.assert_called_once()  # type: ignore[attr-defined] # Reason: see above # noqa: B950
        db_conn.con.connect.return_value.__enter__.assert_called_once()  # type: ignore[attr-defined] # Reason: see above # noqa: B950
        mock_db_connection.execution_options.assert_called_once()
        mock_db_connection.execute.assert_called_once()
