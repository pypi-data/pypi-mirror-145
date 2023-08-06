"""Tests dataloaders.py."""
from unittest.mock import MagicMock

import pandas as pd
import pytest
from pytest import fixture

from bitfount.backends.pytorch.data.dataloaders import (
    DEFAULT_BUFFER_SIZE,
    _PyTorchBitfountDataLoader,
    _PyTorchIterableBitfountDataLoader,
)
from bitfount.backends.pytorch.data.datasets import (
    _PyTorchDataset,
    _PyTorchIterableDataset,
)
from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from tests.utils.helper import TABLE_NAME, backend_test, create_dataset, unit_test


@backend_test
class TestPyTorchBitfountDataLoader:
    """Tests _PyTorchBitfountDataLoader."""

    @fixture
    def dataframe(self) -> pd.DataFrame:
        """Dataframe fixture."""
        df = create_dataset(image=True)
        # Drop the date column until we support datetime.
        return df.drop(columns=["Date"])

    @unit_test
    def test_iterator_tab_data(self, dataframe: pd.DataFrame) -> None:
        """Tests iteration of dataloader for tabular data."""
        df = dataframe.drop(columns=["image"])
        datasource = DataSource(df)
        datasource.load_data()
        datastucture = DataStructure(target="TARGET", table=TABLE_NAME)
        schema = BitfountSchema()
        schema.add_datasource_tables(datasource, table_name=TABLE_NAME)
        datastucture.set_training_column_split_by_semantic_type(schema.tables[0])
        dataset = _PyTorchDataset(
            df, target="TARGET", selected_cols=datastucture.selected_cols_w_types
        )
        batch_size = 16
        dl = _PyTorchBitfountDataLoader(dataset=dataset, batch_size=batch_size)
        dl_iterator = iter(dl)
        batch = next(dl_iterator)
        assert isinstance(batch, list)
        assert isinstance(batch[0], list)  # x data
        assert len(batch[0][0]) == batch_size  # tabular x data
        assert len(batch[0][1]) == batch_size  # x support columns
        assert len(batch[1]) == batch_size  # y data

    @unit_test
    def test_iterator_image_data(self, dataframe: pd.DataFrame) -> None:
        """Tests iteration of dataloader for image data."""
        df = dataframe[["image", "TARGET"]]
        datasource = DataSource(df)
        datasource.load_data()
        datastucture = DataStructure(target="TARGET", table=TABLE_NAME)
        schema = BitfountSchema()
        schema.add_datasource_tables(
            datasource,
            force_stypes={TABLE_NAME: {"image": ["image"]}},
            table_name=TABLE_NAME,
        )
        datastucture.set_training_column_split_by_semantic_type(schema.tables[0])
        dataset = _PyTorchDataset(
            df, target="TARGET", selected_cols=datastucture.selected_cols_w_types
        )
        batch_size = 16
        dl = _PyTorchBitfountDataLoader(dataset=dataset, batch_size=batch_size)
        dl_iterator = iter(dl)
        batch = next(dl_iterator)
        assert isinstance(batch, list)
        assert isinstance(batch[0], list)  # x data
        assert len(batch[0][0]) == batch_size  # image x data
        assert len(batch[0][1]) == batch_size  # x support columns
        assert len(batch[1]) == batch_size  # y data

    @unit_test
    def test_iterator_image_tab_data(self, dataframe: pd.DataFrame) -> None:
        """Tests iteration of dataloader for mixed image and tabular data."""
        datasource = DataSource(dataframe)
        datasource.load_data()
        datastucture = DataStructure(target="TARGET", table=TABLE_NAME)
        schema = BitfountSchema()
        schema.add_datasource_tables(
            datasource,
            force_stypes={TABLE_NAME: {"image": ["image"]}},
            table_name=TABLE_NAME,
        )
        datastucture.set_training_column_split_by_semantic_type(schema.tables[0])
        dataset = _PyTorchDataset(
            dataframe, target="TARGET", selected_cols=datastucture.selected_cols_w_types
        )
        batch_size = 16
        dl = _PyTorchBitfountDataLoader(dataset=dataset, batch_size=batch_size)
        dl_iterator = iter(dl)
        batch = next(dl_iterator)
        assert isinstance(batch, list)
        assert isinstance(batch[0], list)  # x data
        assert len(batch[0][0]) == batch_size  # tabular x data
        assert len(batch[0][1]) == batch_size  # image x data
        assert len(batch[0][2]) == batch_size  # x support columns
        assert len(batch[1]) == batch_size  # y data


@backend_test
class TestPyTorchIterableBitfountDataLoader:
    """Tests _PyTorchIterableBitfountDataLoader."""

    @unit_test
    @pytest.mark.parametrize(
        "dataset_length,batch_size,expected_buffer_size",
        [
            # Dataset length is the expected buffer size since it is smaller than the
            # default buffer size.
            (100, 16, 100),
            # DEFAULT_BUFFER_SIZE is the expected buffer size since it is smaller than
            # the dataset length but larger than the batch size.
            (100000, 1, DEFAULT_BUFFER_SIZE),
            # Batch size is the expected buffer size since it is larger than the default
            # buffer size.
            (100, 1024, 1024),
        ],
    )
    def test_buffer_size(
        self, dataset_length: int, batch_size: int, expected_buffer_size: int
    ) -> None:
        """Tests buffer size property calculation."""
        dataset = MagicMock(spec=_PyTorchIterableDataset)
        dataset.__len__.return_value = dataset_length
        dataloader = _PyTorchIterableBitfountDataLoader(
            dataset=dataset, batch_size=batch_size
        )
        assert dataloader.buffer_size == expected_buffer_size

    @unit_test
    @pytest.mark.parametrize(
        "shuffle,secure_rng,batch_size,iterator_size",
        [
            # Tests with iterator that is smaller than the batch size
            (True, True, 8, 6),
            (False, False, 8, 7),
            # Tests with iterator that is equal to or just greater than the batch size
            (True, False, 8, 8),
            (False, False, 8, 9),
            # Tests with iterator that is significantly greater than the batch size
            # with no remainder
            (True, True, 32, 64),
            (False, False, 32, 96),
            # Tests with iterator that is significantly greater than the batch size
            # with a remainder
            (True, False, 32, 65),
            (False, False, 32, 325),
        ],
    )
    def test_iterator(
        self, shuffle: bool, secure_rng: bool, batch_size: int, iterator_size: int
    ) -> None:
        """Tests iteration of dataloader."""
        dataset = MagicMock(spec=_PyTorchIterableDataset)
        dataset.__iter__.return_value = iter(range(iterator_size))
        dataloader = _PyTorchIterableBitfountDataLoader(
            dataset=dataset,
            batch_size=batch_size,
            shuffle=shuffle,
            secure_rng=secure_rng,
        )
        for i, batch in enumerate(dataloader, start=1):
            assert isinstance(batch, list)
            if iterator_size - (i * batch_size) >= batch_size:
                assert len(batch) == batch_size
            else:  # last batch may have fewer elements
                assert len(batch) <= batch_size

            if shuffle:
                # There is an extremely slim chance that the order of the elements in
                # the shuffled batch will be in the same order they started in but this
                # is negligible for our batch sizes as long as it is not the final batch
                # where there may be fewer elements (e.g. just 1).
                if len(batch) == batch_size:
                    assert sorted(batch) != batch
            else:
                assert sorted(batch) == batch
