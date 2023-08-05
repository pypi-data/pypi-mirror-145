"""Tests dataloaders.py."""
import numpy as np
import pandas as pd
import pytest
from pytest import fixture

from bitfount.data.dataloaders import _BitfountDataLoader
from bitfount.data.datasets import _BitfountDataset
from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import SemanticType
from tests.utils.helper import TABLE_NAME, create_dataset, unit_test


class TestDataLoaders:
    """Tests BitfountDataloader."""

    @fixture
    def dataframe(self) -> pd.DataFrame:
        """Dataframe fixture."""
        df = create_dataset(image=True)
        # Drop the date column until we support datetime.
        return df.drop(columns=["Date"])

    @unit_test
    def test_get_x_dataframe_tabular_only(self, dataframe: pd.DataFrame) -> None:
        """Tests get_x_dataframe for tabular data."""
        df = dataframe.drop(columns=["image"])
        datasource = DataSource(df)
        datasource.load_data()
        datastucture = DataStructure(target="TARGET", table=TABLE_NAME)
        schema = BitfountSchema()
        schema.add_datasource_tables(datasource, table_name=TABLE_NAME)
        datastucture.set_training_column_split_by_semantic_type(schema.tables[0])
        dataset = _BitfountDataset(
            df, target="TARGET", selected_cols=datastucture.selected_cols_w_types
        )
        dl = _BitfountDataLoader(dataset=dataset)
        x_df = dl.get_x_dataframe()
        # Drop target and text columns
        new_df = df.drop(columns=["TARGET", "I", "J", "K", "L"])
        assert isinstance(x_df, pd.DataFrame)
        assert set(x_df.columns) == set(new_df.columns)

    @unit_test
    def test_get_x_dataframe_image_only(self, dataframe: pd.DataFrame) -> None:
        """Tests get_x_dataframe for tabular data."""
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
        dataset = _BitfountDataset(
            df, target="TARGET", selected_cols=datastucture.selected_cols_w_types
        )
        dl = _BitfountDataLoader(dataset=dataset)
        x_df = dl.get_x_dataframe()
        assert isinstance(x_df, pd.DataFrame)
        assert x_df.equals(df[["image"]])

    @unit_test
    def test_get_x_dataframe_image_and_tab(self, dataframe: pd.DataFrame) -> None:
        """Tests get_x_dataframe for tabular data."""
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
        dataset = _BitfountDataset(
            dataframe, target="TARGET", selected_cols=datastucture.selected_cols_w_types
        )
        dl = _BitfountDataLoader(dataset=dataset)
        x_df = dl.get_x_dataframe()
        # Drop target, image, and text columns
        new_df = dataframe.drop(columns=["TARGET", "I", "J", "K", "L", "image"])
        assert isinstance(x_df, tuple)
        assert set(x_df[0].columns) == set(new_df.columns)
        assert x_df[1].equals(dataframe[["image"]])

    @unit_test
    def test_empty_dataframe_raises_valerror(self, dataframe: pd.DataFrame) -> None:
        """Tests get_x_dataframe with empty df raises error."""
        df = pd.DataFrame(dataframe[["TARGET"]])
        datasource = DataSource(df)
        datasource.load_data()
        datastucture = DataStructure(
            target="TARGET", selected_cols=["TARGET"], table=TABLE_NAME
        )
        schema = BitfountSchema()
        schema.add_datasource_tables(datasource, table_name=TABLE_NAME)
        datastucture.set_training_column_split_by_semantic_type(schema.tables[0])
        dataset = _BitfountDataset(
            dataframe, target="TARGET", selected_cols=datastucture.selected_cols_w_types
        )
        dl = _BitfountDataLoader(dataset=dataset)
        with pytest.raises(ValueError):
            dl.get_x_dataframe()

    @unit_test
    def test_dataloader_tab(self, tabular_dataset: _BitfountDataset) -> None:
        """Tests x- and y-dataframe retrieval from dataloader for tabular data."""
        df = _BitfountDataLoader(tabular_dataset)
        x = df.get_x_dataframe()
        y = df.get_y_dataframe()
        assert isinstance(x, pd.DataFrame)
        assert len(x) == len(y)
        assert len(x.columns) == 12
        assert len(y.columns) == 1

    @unit_test
    def test_dataloader_img(self, image_dataset: _BitfountDataset) -> None:
        """Tests x- and y-dataframe retrieval from dataloader for image data."""
        df = _BitfountDataLoader(image_dataset)
        x = df.get_x_dataframe()
        y = df.get_y_dataframe()
        assert isinstance(x, pd.DataFrame)
        assert len(x) == len(y)
        assert len(x.columns) == 1
        assert len(y.columns) == 1

    @unit_test
    def test_dataloader_img_tab(self, image_tab_dataset: _BitfountDataset) -> None:
        """Tests x- and y-dataframe retrieval from dataloader."""
        df = _BitfountDataLoader(image_tab_dataset)
        x = df.get_x_dataframe()
        y = df.get_y_dataframe()
        assert isinstance(x, tuple)
        tab, img = x
        assert len(tab) == len(y)
        assert len(img) == len(y)
        assert len(y.columns) == 1
        assert len(tab.columns) == 12
        assert len(img.columns) == 1

    @unit_test
    def test_dataloader_multiimage(self, multiimage_dataset: _BitfountDataset) -> None:
        """Tests x- and y-dataframe retrieval from dataloader for multi-image."""
        df = _BitfountDataLoader(multiimage_dataset)
        x = df.get_x_dataframe()
        y = df.get_y_dataframe()
        assert isinstance(x, pd.DataFrame)
        assert len(x) == len(y)
        assert len(x.columns) == 2
        assert len(y.columns) == 1

    @unit_test
    def test_dataloader_multilabel(self) -> None:
        """Tests x- and y-dataframe retrieval from dataloader for multilabel target."""
        data = create_dataset(image=True)
        data = data.assign(TARGET_2=np.zeros(len(data)))
        data.loc[(data.A < 700) & (data.F < 0.5) & (data.D % 2 == 1), "TARGET_2"] = 1
        datasource = DataSource(data)
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
        datastructure = DataStructure(target=["TARGET", "TARGET_2"], table=TABLE_NAME)
        datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
        multilabel_dataset = _BitfountDataset(
            data=datasource.data,
            target=["TARGET", "TARGET_2"],
            selected_cols=datastructure.selected_cols_w_types,
        )
        df = _BitfountDataLoader(multilabel_dataset)
        x = df.get_x_dataframe()
        y = df.get_y_dataframe()
        assert isinstance(x, tuple)
        tab, img = x
        assert len(tab) == len(y)
        assert len(img) == len(y)
        assert len(y.columns) == 2
        assert len(tab.columns) == 13
        assert len(img.columns) == 1
