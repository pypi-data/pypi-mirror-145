"""Tests databunch.py."""
from typing import cast
from unittest.mock import PropertyMock, create_autospec

import pytest
from pytest import fixture
from pytest_mock import MockerFixture

from bitfount.data.databunch import _BitfountDataBunch
from bitfount.data.dataloaders import _BitfountDataLoader
from bitfount.data.datasource import DataSource
from bitfount.data.datasplitters import _DatasetSplitter
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from tests.utils import PytestRequest
from tests.utils.helper import (
    TABLE_NAME,
    create_dataset,
    create_datasource,
    create_schema,
    unit_test,
)


@unit_test
class TestBitfountDataBunch:
    """Tests for BitfountDataBunch class."""

    @fixture
    def data_bunch(self) -> _BitfountDataBunch:
        """Returns instance of BitfountDataBunch."""
        dataset = create_dataset()
        datasource = DataSource(dataset)
        schema = BitfountSchema(
            datasource, force_categorical=["TARGET"], table_name=TABLE_NAME
        )
        return _BitfountDataBunch(
            data_structure=DataStructure(target="TARGET", table=TABLE_NAME),
            schema=schema.tables[0],
            datasource=datasource,
        )

    def test_create_datasets_with_missing_columns(self) -> None:
        """Test that columns are created if they exist in schema.

        This tests whether a DataSource which is missing columns listed in the Schema
        has those missing columns added to it, to ensure that transformations
        can be applied across pods with varying schemas
        """
        dataset_with_all_columns = create_dataset()
        datasource_with_all_columns = DataSource(dataset_with_all_columns)
        datasource_with_all_columns.load_data()
        schema_with_all_columns = BitfountSchema(
            datasource_with_all_columns,
            force_stypes={TABLE_NAME: {"categorical": ["TARGET"]}},
            table_name=TABLE_NAME,
        )
        dataset_missing_some_columns = dataset_with_all_columns.drop(
            columns=["A", "B", "I"]
        )
        datasource = DataSource(dataset_missing_some_columns)
        datasource.load_data()
        databunch = _BitfountDataBunch(
            data_structure=DataStructure(target="TARGET", table=TABLE_NAME),
            schema=schema_with_all_columns.tables[0],
            datasource=datasource,
        )

        created_train_dataset = databunch.get_train_dataloader().dataset
        created_validation_dataset = cast(
            _BitfountDataLoader, databunch.get_validation_dataloader()
        ).dataset
        created_test_dataset = cast(
            _BitfountDataLoader, databunch.get_test_dataloader()
        ).dataset

        text_columns = ["I", "J", "K", "L"]
        assert set(
            created_train_dataset.x_columns + created_train_dataset.y_columns
        ) == set([i for i in dataset_with_all_columns.columns if i not in text_columns])
        assert set(
            created_validation_dataset.x_columns + created_validation_dataset.y_columns
        ) == set([i for i in dataset_with_all_columns.columns if i not in text_columns])
        assert set(
            created_test_dataset.x_columns + created_test_dataset.y_columns
        ) == set([i for i in dataset_with_all_columns.columns if i not in text_columns])


@unit_test
class TestCreateDataBunch:
    """Tests basic databunch generator."""

    @fixture(scope="function", params=[True, False])
    def datasource(self, request: PytestRequest) -> DataSource:
        """Parameterised creation of DataSource (with optional image col) for tests."""
        data = create_dataset(image=request.param)
        if request.param:
            datasource = DataSource(data, seed=420, image_col=["image"])
            datasource.load_data()
            return datasource

        datasource = DataSource(data, seed=420)
        datasource.load_data()
        return datasource

    @fixture
    def datasource_w_loss_weights(self) -> DataSource:
        """Creates a datasource with loss_weights column."""
        ds = create_datasource(classification=True, loss_weights=True)
        ds.load_data()
        return ds

    @fixture
    def schema(self) -> BitfountSchema:
        """Creates a schema."""
        return create_schema(classification=True, loss_weights=True)

    def test_databunch_local_with_schema(self, datasource: DataSource) -> None:
        """Checks databunch creation with schema."""
        target = "TARGET"
        schema = BitfountSchema()
        schema.add_datasource_tables(
            datasource,
            force_stypes={TABLE_NAME: {"categorical": [target]}},
            table_name=TABLE_NAME,
        )
        datastructure = DataStructure(target=target, table=TABLE_NAME)

        db = _BitfountDataBunch(
            data_structure=datastructure, schema=schema.tables[0], datasource=datasource
        )
        assert target == db.target

    def test_databunch_ignore_cols(
        self, datasource_w_loss_weights: DataSource, schema: BitfountSchema
    ) -> None:
        """Checks that the appropriate ignore_columns are ignored."""
        datastructure = DataStructure(
            target="TARGET",
            ignore_cols=["A", "B", "G", "H"],
            loss_weights_col="weights",
            table=TABLE_NAME,
        )
        db = _BitfountDataBunch(
            data_structure=datastructure,
            schema=schema.tables[0],
            datasource=datasource_w_loss_weights,
        )
        # Schema also has text columns : "I", "J", "K", "L"
        assert set(db.ignore_cols) == set(
            ["TARGET", "weights", "A", "B", "G", "H", "I", "J", "K", "L"]
        )

    def test_databunch_selected_cols(
        self, datasource_w_loss_weights: DataSource, schema: BitfountSchema
    ) -> None:
        """Checks that the appropriate ignore_columns are ignored."""
        datastructure = DataStructure(
            target="TARGET",
            selected_cols=[
                "E",
                "F",
                "G",
                "H",
                "M",
                "N",
                "O",
                "P",
                "TARGET",
                "weights",
            ],
            loss_weights_col="weights",
            table=TABLE_NAME,
        )
        db = _BitfountDataBunch(
            data_structure=datastructure,
            schema=schema.tables[0],
            datasource=datasource_w_loss_weights,
        )
        assert set(db.ignore_cols) == set(
            ["TARGET", "weights", "A", "B", "C", "D", "I", "J", "K", "L", "Date"]
        )

    def test_databunch_text_columns_are_ignored_even_if_selected(
        self, datasource_w_loss_weights: DataSource, schema: BitfountSchema
    ) -> None:
        """Checks that the text columns are ignored even if selected."""
        datastructure = DataStructure(
            target="TARGET",
            selected_cols=[
                "E",
                "F",
                "G",
                "H",
                "I",  # text
                "J",  # text
                "K",  # text
                "L",  # test
                "M",
                "N",
                "O",
                "P",
                "TARGET",
                "weights",
            ],
            loss_weights_col="weights",
            table=TABLE_NAME,
        )
        db = _BitfountDataBunch(
            data_structure=datastructure,
            schema=schema.tables[0],
            datasource=datasource_w_loss_weights,
        )
        assert set(db.ignore_cols) == set(
            ["TARGET", "weights", "A", "B", "C", "D", "I", "J", "K", "L", "Date"]
        )

    @pytest.mark.parametrize(
        "add_datasource_split, add_datastructure_split",
        [
            (True, True),
            (True, True),
            (False, True),
            (False, False),
        ],
    )
    def test_databunch_split_data(
        self,
        datasource: DataSource,
        add_datasource_split: bool,
        add_datastructure_split: bool,
        mocker: MockerFixture,
    ) -> None:
        """Checks databunch uses correct split.

        If datasource has a data_splitter, use it to split the data.
        Else if the datastructure has a data_splitter use that splitter.
        Else ust the PercentageSplitter.
        """
        if add_datasource_split:
            data_splitter = create_autospec(_DatasetSplitter)
            data_splitter.create_dataset_splits.return_value = (None, None, None)
            mocker.patch.object(
                datasource,
                "data_splitter",
                new_callable=PropertyMock(return_value=data_splitter),
            )

        target = "TARGET"
        schema = BitfountSchema()
        schema.add_datasource_tables(
            datasource,
            force_stypes={TABLE_NAME: {"categorical": [target]}},
            table_name=TABLE_NAME,
        )
        datastructure = DataStructure(target=target, table=TABLE_NAME)
        if add_datastructure_split:
            data_splitter = create_autospec(_DatasetSplitter)
            data_splitter.create_dataset_splits.return_value = (None, None, None)
            mocker.patch.object(
                datastructure,
                "data_splitter",
                new_callable=PropertyMock(return_value=data_splitter),
            )

        mock_perc_splitter = mocker.patch("bitfount.data.databunch.PercentageSplitter")
        mock_perc_splitter.return_value.create_dataset_splits.return_value = (
            None,
            None,
            None,
        )
        with mocker.patch.object(_BitfountDataBunch, "create_datasets"):

            _BitfountDataBunch(
                data_structure=datastructure,
                schema=schema.tables[0],
                datasource=datasource,
            )

        if add_datasource_split:
            assert datasource.data_splitter is not None
            datasource.data_splitter.create_dataset_splits.assert_called_once()  # type: ignore[attr-defined] # Reason: patched attribute  # noqa: B950
            if datastructure.data_splitter:
                datastructure.data_splitter.create_dataset_splits.assert_not_called()  # type: ignore[attr-defined] # Reason: patched attribute  # noqa: B950
            mock_perc_splitter.return_value.create_dataset_splits.assert_not_called()
        elif add_datastructure_split:
            assert datastructure.data_splitter is not None
            datastructure.data_splitter.create_dataset_splits.assert_called_once()  # type: ignore[attr-defined] # Reason: patched attribute  # noqa: B950
            mock_perc_splitter.return_value.create_dataset_splits.assert_not_called()
        else:
            mock_perc_splitter.return_value.create_dataset_splits.assert_called_once()
