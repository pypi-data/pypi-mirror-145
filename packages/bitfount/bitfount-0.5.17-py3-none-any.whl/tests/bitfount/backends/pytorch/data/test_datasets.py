"""Tests for PyTorchDataset classes."""
from typing import Union

import pandas as pd
import pytest
from pytest import fixture
import torch

from bitfount.backends.pytorch.data.dataloaders import _PyTorchBitfountDataLoader
from bitfount.backends.pytorch.data.datasets import _PyTorchDataset
from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import SemanticType
from tests.utils.helper import TABLE_NAME, backend_test, create_dataset, unit_test


@backend_test
@unit_test
class TestPyTorchDataset:
    """Tests for PyTorchTabularDataset class."""

    @fixture
    def dataframe(self) -> pd.DataFrame:
        """Underlying dataframe for dataset."""
        return create_dataset(image=True)

    @fixture
    def tabular_dataset(self, dataframe: pd.DataFrame) -> _PyTorchDataset:
        """Basic PyTorch tabular dataset for tests as fixture."""
        target = "TARGET"
        datasource = DataSource(dataframe)
        schema = BitfountSchema()
        schema.add_datasource_tables(datasource, table_name=TABLE_NAME)
        datasource.load_data()
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.get_feature_names(TABLE_NAME, SemanticType.TEXT)
        )
        datastructure = DataStructure(
            target=target, ignore_cols=["image"], table=TABLE_NAME
        )
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        return _PyTorchDataset(
            data=datasource.data,
            target=target,
            selected_cols=datastructure.selected_cols_w_types,
        )

    @fixture
    def image_dataset(self, dataframe: pd.DataFrame) -> _PyTorchDataset:
        """Basic PyTorch image dataset for tests as fixture."""
        target = "TARGET"
        datasource = DataSource(dataframe)
        schema = BitfountSchema()
        schema.add_datasource_tables(
            datasource,
            force_stypes={TABLE_NAME: {"image": ["image"]}},
            table_name=TABLE_NAME,
        )
        datasource.load_data()
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.get_feature_names(TABLE_NAME, SemanticType.TEXT)
        )
        datastructure = DataStructure(
            target=target, selected_cols=["image"], table=TABLE_NAME
        )
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        return _PyTorchDataset(
            data=datasource.data,
            target=target,
            selected_cols=datastructure.selected_cols_w_types,
        )

    @fixture
    def image_tab_dataset(self, dataframe: pd.DataFrame) -> _PyTorchDataset:
        """Basic PyTorchPredictionDataset dataset for tests as fixture."""
        target = "TARGET"
        datasource = DataSource(dataframe)
        schema = BitfountSchema()
        schema.add_datasource_tables(
            datasource,
            force_stypes={TABLE_NAME: {"image": ["image"]}},
            table_name=TABLE_NAME,
        )
        datasource.load_data()
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.get_feature_names(TABLE_NAME, SemanticType.TEXT)
        )
        datastructure = DataStructure(target=target, table=TABLE_NAME)
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        return _PyTorchDataset(
            data=datasource.data,
            target=target,
            selected_cols=datastructure.selected_cols_w_types,
        )

    @fixture
    def multiimage_dataframe(self) -> pd.DataFrame:
        """Underlying dataframe for multi-image dataset."""
        return create_dataset(multiimage=True)

    @fixture
    def multiimage_dataset(self, multiimage_dataframe: pd.DataFrame) -> _PyTorchDataset:
        """Basic multi-image dataset for tests as fixture."""
        target = "TARGET"
        datasource = DataSource(multiimage_dataframe)
        schema = BitfountSchema()
        schema.add_datasource_tables(
            datasource,
            force_stypes={TABLE_NAME: {"image": ["image1", "image2"]}},
            table_name=TABLE_NAME,
        )
        datasource.load_data()
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.get_feature_names(TABLE_NAME, SemanticType.TEXT)
        )
        datastructure = DataStructure(
            target=target, selected_cols=["image1", "image2", target], table=TABLE_NAME
        )
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        return _PyTorchDataset(
            data=datasource.data,
            target=target,
            selected_cols=datastructure.selected_cols_w_types,
        )

    def test_len_tab_data(
        self, dataframe: pd.DataFrame, tabular_dataset: _PyTorchDataset
    ) -> None:
        """Tests tabular dataset __len__ method."""
        assert len(tabular_dataset) == len(dataframe)

    def test_len_image_data(
        self, dataframe: pd.DataFrame, image_dataset: _PyTorchDataset
    ) -> None:
        """Tests image dataset __len__ method."""
        assert len(image_dataset) == len(dataframe)

    def test_len_image_tab_data(
        self, dataframe: pd.DataFrame, image_tab_dataset: _PyTorchDataset
    ) -> None:
        """Tests mixed dataset __len__ method."""
        assert len(image_tab_dataset) == len(dataframe)

    def test_len_multiimage_data(
        self, multiimage_dataframe: pd.DataFrame, multiimage_dataset: _PyTorchDataset
    ) -> None:
        """Tests multi-image dataset __len__ method."""
        assert len(multiimage_dataset) == len(multiimage_dataframe)

    @pytest.mark.parametrize("idx", [0, 42, 2048, torch.tensor(3999)])
    def test_idx_tab_data(
        self, idx: Union[int, torch.Tensor], tabular_dataset: _PyTorchDataset
    ) -> None:
        """Tests indexing (incl. tensors) returns the expected formats of data."""
        assert isinstance(tabular_dataset[idx], tuple)
        assert len(tabular_dataset[idx]) == 2  # split into x,y
        assert len(tabular_dataset[idx][0]) == 2  # split into tabular, support
        assert len(tabular_dataset[idx][0][0]) == 13  # training cols  check
        assert len(tabular_dataset[idx][0][1]) == 2  # support cols check
        assert len([tabular_dataset[idx][1]]) == 1  # y check

    @pytest.mark.parametrize("idx", [0, 42, 2048, torch.tensor(3999)])
    def test_idx_img_data(self, idx: int, image_dataset: _PyTorchDataset) -> None:
        """Tests indexing returns the expected formats of data."""
        assert isinstance(image_dataset[idx], tuple)
        assert len(image_dataset[idx]) == 2  # split into x,y
        assert len(image_dataset[idx][0]) == 2  # split into image, support
        assert len(image_dataset[idx][0][1]) == 2  # support cols check
        assert len([image_dataset[idx][1]]) == 1  # y check

    @pytest.mark.parametrize("idx", [0, 42, 2048, torch.tensor(3999)])
    def test_idx_img_tab_data(
        self, idx: int, image_tab_dataset: _PyTorchDataset
    ) -> None:
        """Tests indexing returns the expected formats of data."""
        assert isinstance(image_tab_dataset[idx], tuple)
        assert len(image_tab_dataset[idx]) == 2  # split into x,y
        assert len(image_tab_dataset[idx][0]) == 3  # split into tab, image, support
        assert len(image_tab_dataset[idx][0][0]) == 13  # tabular cols  check
        assert len(image_tab_dataset[idx][0][2]) == 2  # support cols check
        assert len([image_tab_dataset[idx][1]]) == 1  # y check

    @pytest.mark.parametrize("idx", [0, 42, 2048, torch.tensor(3999)])
    def test_idx_multiimg_data(
        self, idx: int, multiimage_dataset: _PyTorchDataset
    ) -> None:
        """Tests indexing returns the expected formats of data."""
        assert isinstance(multiimage_dataset[idx], tuple)
        assert len(multiimage_dataset[idx]) == 2  # split into x,y
        assert len(multiimage_dataset[idx][0]) == 2  # split into image, support
        assert isinstance(multiimage_dataset[idx][0][0], tuple)
        assert len(multiimage_dataset[idx][0][0]) == 2  # image cols check
        assert len(multiimage_dataset[idx][0][1]) == 2  # support cols check
        assert len([multiimage_dataset[idx][1]]) == 1  # y check

    @pytest.mark.parametrize("idx", [0, 42, 2048, torch.tensor(3999)])
    def test_idx_img_tab_category(
        self, idx: int, image_tab_dataset: _PyTorchDataset
    ) -> None:
        """Tests indexing with categories gives expected data formats."""
        target = "TARGET"
        data = create_dataset(image=True, multihead=True)
        datasource = DataSource(data, image_col=["image"])
        schema = BitfountSchema()
        schema.add_datasource_tables(
            datasource,
            force_stypes={
                TABLE_NAME: {"categorical": ["category"], "image": ["image"]}
            },
            table_name=TABLE_NAME,
        )
        datasource.load_data()
        datasource.data = schema.apply(datasource.data)
        datasource.data = datasource.data.drop(
            columns=schema.get_feature_names(TABLE_NAME, SemanticType.TEXT)
        )
        datastructure = DataStructure(
            target=target, multihead_col="category", multihead_size=2, table=TABLE_NAME
        )
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        dataset = _PyTorchDataset(
            data=datasource.data,
            target=target,
            multihead_col="category",
            selected_cols=datastructure.selected_cols_w_types,
        )
        assert isinstance(dataset[idx], tuple)
        assert len(dataset[idx]) == 2  # split into x,y
        assert len(dataset[idx][0]) == 3  # split into tab, image, support
        assert (
            len(dataset[idx][0][0]) == 14
        )  # tabular cols check (multihead_col included)
        assert len(dataset[idx][0][2]) == 3  # support cols check
        assert len([dataset[idx][1]]) == 1  # y check

    def test_dataloader_pytorch(self, image_tab_dataset: _PyTorchDataset) -> None:
        """Tests iteration of dataloader."""
        batch_size = 64
        dl = _PyTorchBitfountDataLoader(image_tab_dataset, batch_size=batch_size)
        iterator = iter(dl)
        output = next(iterator)
        assert isinstance(output, list)
        x, y = output
        assert len(x) == 3
        assert len(x[0]) == batch_size  # tabular
        assert len(x[1]) == batch_size  # image
        # Mypy mistakenly believes that there is no third element
        assert (
            len(x[2]) == batch_size  # type: ignore[misc] # Reason: see above
        )  # support
        assert len(y) == batch_size

    def test_dataloader_non_pytorch_img_tab(
        self, image_tab_dataset: _PyTorchDataset
    ) -> None:
        """Tests x- and y-dataframe retrieval from dataloader."""
        dl = _PyTorchBitfountDataLoader(image_tab_dataset)
        tab, img = dl.get_x_dataframe()
        y = dl.get_y_dataframe()
        assert len(tab) == len(y)
        assert len(img) == len(y)
        assert len(y.columns) == 1
        assert len(tab.columns) == 13
        assert len(img.columns) == 1

    def test_dataset_works_only_with_continuous_features(
        self, dataframe: pd.DataFrame
    ) -> None:
        """Test no errors are raised if the dataset only has continuous features."""
        datasource = DataSource(dataframe.loc[:, ["A", "B", "TARGET"]])
        datasource.load_data()
        schema = BitfountSchema()
        schema.add_datasource_tables(datasource, table_name=TABLE_NAME)
        datastructure = DataStructure(
            target=["TARGET"],
            table=TABLE_NAME,
        )
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        dataset = _PyTorchDataset(
            data=datasource.data,
            target=["TARGET"],
            selected_cols=datastructure.selected_cols_w_types,
        )
        assert "categorical" not in schema.tables[0].features
        idx = 10
        assert isinstance(dataset[idx], tuple)
        assert len(dataset[idx]) == 2  # split into x,y
        assert len(dataset[idx][0]) == 2  # split into tabular, support
        assert len(dataset[idx][0][0]) == 2  # training cols  check
        assert len(dataset[idx][0][1]) == 2  # support cols check
        assert len([dataset[idx][1]]) == 1  # y check

    def test_dataset_works_without_target(self, dataframe: pd.DataFrame) -> None:
        """Test no errors are raised if the dataset has no target."""
        datasource = DataSource(dataframe.loc[:, ["A", "B"]])
        datasource.load_data()
        schema = BitfountSchema()
        schema.add_datasource_tables(datasource, table_name=TABLE_NAME)
        datastructure = DataStructure(table=TABLE_NAME)
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        dataset = _PyTorchDataset(
            data=datasource.data,
            selected_cols=datastructure.selected_cols_w_types,
        )
        idx = 10
        assert isinstance(dataset[idx], tuple)
        assert len(dataset[idx]) == 2  # split into x,y
        assert len(dataset[idx][0]) == 2  # split into tabular, support
        assert len(dataset[idx][0][0]) == 2  # training cols  check
        assert len(dataset[idx][0][1]) == 2  # support cols check
        assert len([dataset[idx][1]]) == 1  # y check
        for i in range(0, len(dataset)):
            assert dataset[i][1] == 0  # all target values default to 0.

    def test_dataset_works_only_with_categorical_features(
        self, dataframe: pd.DataFrame
    ) -> None:
        """Test no errors are raised if the dataset only has categorical features."""
        datasource = DataSource(dataframe.loc[:, ["M", "N", "TARGET"]])
        datasource.load_data()
        schema = BitfountSchema()
        schema.add_datasource_tables(
            datasource,
            force_stypes={TABLE_NAME: {"categorical": ["TARGET"]}},
            table_name=TABLE_NAME,
        )
        datastructure = DataStructure(target=["TARGET"], table=TABLE_NAME)
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        dataset = _PyTorchDataset(
            data=datasource.data,
            target=["TARGET"],
            selected_cols=datastructure.selected_cols_w_types,
        )
        assert "continuous" not in schema.tables[0].features
        idx = 10
        assert isinstance(dataset[idx], tuple)
        assert len(dataset[idx]) == 2  # split into x,y
        assert len(dataset[idx][0]) == 2  # split into tabular, support
        assert len(dataset[idx][0][0]) == 2  # training cols  check
        assert len(dataset[idx][0][1]) == 2  # support cols check
        assert len([dataset[idx][1]]) == 1  # y check
