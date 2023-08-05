"""Pytest fixtures for data tests."""

from typing import Any, Generator
from unittest.mock import Mock

from _pytest.monkeypatch import MonkeyPatch
import pandas as pd
import psycopg
from pytest import fixture
from pytest_mock import MockerFixture
import sqlalchemy

from bitfount.data.datasets import _BitfountDataset
from bitfount.data.datasource import DataSource
from bitfount.data.datastructure import DataStructure
from bitfount.data.schema import BitfountSchema
from bitfount.data.types import SemanticType
from tests.utils.helper import TABLE_NAME, create_dataset


@fixture
def dataframe() -> pd.DataFrame:
    """Underlying dataframe for single image datasets."""
    return create_dataset(image=True)


@fixture
def tabular_dataset(dataframe: pd.DataFrame) -> _BitfountDataset:
    """Basic tabular dataset for tests as fixture."""
    target = "TARGET"
    datasource = DataSource(dataframe)
    datasource.load_data()
    schema = BitfountSchema()
    schema.add_datasource_tables(datasource, table_name=TABLE_NAME)
    datasource.data = schema.apply(datasource.data)
    datasource.data = datasource.data.drop(
        columns=schema.get_feature_names(TABLE_NAME, SemanticType.TEXT)
    )
    datastructure = DataStructure(
        target=target, ignore_cols=["image"], table=TABLE_NAME
    )
    datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
    return _BitfountDataset(
        data=datasource.data,
        target=target,
        selected_cols=datastructure.selected_cols_w_types,
    )


@fixture
def image_dataset(dataframe: pd.DataFrame) -> _BitfountDataset:
    """Basic image dataset for tests as fixture."""
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
        table=TABLE_NAME,
        selected_cols=["image", target],
        image_cols=["image"],
        batch_transforms=[
            {
                "image": {
                    "step": "train",
                    "output": True,
                    "arg": "image",
                    "transformations": [
                        {"Resize": {"height": 224, "width": 224}},
                        "Normalize",
                    ],
                }
            }
        ],
    )
    datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
    return _BitfountDataset(
        data=datasource.data,
        target=target,
        selected_cols=datastructure.selected_cols_w_types,
        batch_transforms=datastructure.get_batch_transformations(),
        batch_transformation_step="train",
    )


@fixture
def image_tab_dataset(dataframe: pd.DataFrame) -> _BitfountDataset:
    """Basic tabular and image dataset for tests as fixture."""
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
    datastructure = DataStructure(target=target, image_cols=["image"], table=TABLE_NAME)
    datastructure.set_training_column_split_by_semantic_type(schema.tables[0])
    return _BitfountDataset(
        data=datasource.data,
        target=target,
        selected_cols=datastructure.selected_cols_w_types,
    )


@fixture
def multiimage_dataframe() -> pd.DataFrame:
    """Underlying dataframe for multi-image dataset."""
    return create_dataset(multiimage=True)


@fixture
def multiimage_dataset(multiimage_dataframe: pd.DataFrame) -> _BitfountDataset:
    """Basic multi-image dataset for tests as fixture."""
    target = "TARGET"
    datasource = DataSource(multiimage_dataframe)
    datasource.load_data()
    schema = BitfountSchema()
    schema.add_datasource_tables(
        datasource,
        force_stypes={TABLE_NAME: {"image": ["image1", "image2"]}},
        table_name=TABLE_NAME,
    )
    datasource.data = schema.apply(datasource.data)
    datasource.data = datasource.data.drop(
        columns=schema.get_feature_names(TABLE_NAME, SemanticType.TEXT)
    )
    datastructure = DataStructure(
        target=target,
        selected_cols=["image1", "image2", target],
        table=TABLE_NAME,
    )
    datastructure.set_training_column_split_by_semantic_type(schema.tables[0])

    return _BitfountDataset(
        data=datasource.data,
        target=target,
        selected_cols=datastructure.selected_cols_w_types,
    )


@fixture
def mock_pandas_read_sql_table(monkeypatch: MonkeyPatch) -> None:
    """Pandas `read_sql_table()` mocked."""
    data = create_dataset()

    def get_df(**_kwargs: Any) -> pd.DataFrame:
        return data

    monkeypatch.setattr(pd, "read_sql_table", get_df)


@fixture
def mock_pandas_read_sql_query(monkeypatch: MonkeyPatch) -> None:
    """Pandas `read_sql_query()` mocked."""
    data = create_dataset()

    def get_df(**_kwargs: Any) -> pd.DataFrame:
        return data

    monkeypatch.setattr(pd, "read_sql_query", get_df)


@fixture
def mock_inspector(mocker: MockerFixture) -> Generator[Mock, None, None]:
    """Automatically mocks sqlalchemy inspector and yields mocked object."""
    mock_inspector = Mock(
        default_schema_name="public", spec=sqlalchemy.engine.Inspector
    )
    mock_inspector.get_schema_names.return_value = ["public"]
    mock_inspector.get_table_names.return_value = ["dummy_data", "dummy_data_2"]
    mocker.patch("bitfount.data.utils.inspect", return_value=mock_inspector)
    yield mock_inspector


@fixture
def mock_engine(mock_inspector: Mock) -> Generator[Mock, None, None]:
    """Returns mock sqlalchemy engine."""
    yield Mock(spec=sqlalchemy.engine.base.Engine)


@fixture
def db_session(
    postgresql: psycopg.Connection,
) -> Generator[sqlalchemy.engine.base.Engine, None, None]:
    """Creates a dummy postgres database connection."""
    connection = (
        f"postgresql+psycopg2://{postgresql.info.user}:"
        f"@{postgresql.info.host}:{postgresql.info.port}/{postgresql.info.dbname}"
    )
    engine = sqlalchemy.create_engine(connection)

    df = create_dataset()
    df2 = create_dataset()

    # The tables should never already exist in the database so we set it to fail
    # if it does to catch any potential setup errors.
    df.to_sql("dummy_data", engine, if_exists="fail", index=False)
    df2.to_sql("dummy_data_2", engine, if_exists="fail", index=False)

    yield engine
