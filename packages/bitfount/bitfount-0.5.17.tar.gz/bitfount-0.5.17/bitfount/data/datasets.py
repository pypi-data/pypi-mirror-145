"""Classes concerning datasets."""
from abc import ABC, abstractmethod
from functools import cached_property
from typing import (
    Any,
    Dict,
    Iterator,
    List,
    Literal,
    Mapping,
    Optional,
    OrderedDict,
    Sequence,
    Tuple,
    Union,
    cast,
)

import numpy as np
import pandas as pd
from skimage import color, io
from sqlalchemy import text

from bitfount.data.datasource import DatabaseLoader
from bitfount.data.types import _SemanticTypeValue
from bitfount.transformations.base_transformation import Transformation
from bitfount.transformations.batch_operations import BatchTimeOperation
from bitfount.transformations.processor import TransformationProcessor
from bitfount.utils import _array_version

_DATABASE_PARTITION_SIZE: int = 100


class _BaseBitfountDataset(ABC):
    """Base class for representing a dataset."""

    x_columns: List[str]
    x_var: Tuple[Any, Any, np.ndarray]
    y_columns: List[str]
    y_var: np.ndarray

    embedded_col_names: List[str]
    image_columns: List[str]
    processors: Dict[int, TransformationProcessor]
    image: np.ndarray
    tabular: np.ndarray
    support_cols: np.ndarray

    def __init__(
        self,
        selected_cols: Mapping[_SemanticTypeValue, List[str]],
        target: Optional[Union[str, List[str]]] = None,
        batch_transforms: Optional[List[BatchTimeOperation]] = None,
        batch_transformation_step: Optional[Literal["train", "validation"]] = None,
        weights_col: Optional[str] = None,
        multihead_col: Optional[str] = None,
        ignore_classes_col: Optional[str] = None,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.selected_cols = selected_cols
        self.target = target
        self.batch_transforms = batch_transforms
        self.batch_transformation_step = batch_transformation_step
        self.weights_col = weights_col
        self.multihead_col = multihead_col
        self.ignore_classes_col = ignore_classes_col

        self._set_column_name_attributes()
        self._set_batch_transformation_processors()

    @abstractmethod
    def __len__(self) -> int:
        raise NotImplementedError

    def _set_column_name_attributes(self) -> None:
        """Sets the attributes concerning column names.

        Namely, `self.x_columns`, `self.y_columns`, `self.embedded_col_names`,
        and `self.image_columns`.
        """
        self.image_columns = self.selected_cols.get("image", [])
        self.embedded_col_names = self.selected_cols.get("categorical", [])
        self.x_columns = (
            self.embedded_col_names
            + self.selected_cols.get("continuous", [])
            + self.selected_cols.get("image", [])
        )
        if self.target is not None:
            self.y_columns = _array_version(self.target)

    def _set_batch_transformation_processors(self) -> None:
        """Sets `self.processors` for batch transformations."""
        if self.batch_transforms is not None:
            if self.batch_transformation_step is None:
                raise ValueError(
                    "'batch_transformation_step' must be provided "
                    "if 'batch_transformations' are provided"
                )

            # We create a dictionary mapping each image feature to the corresponding
            # list of transformations. This dictionary must be an OrderedDict so that
            # the order of the features is preserved and indexable. Currently, we only
            # support image transformations at batch time.
            feature_transforms: OrderedDict[
                str, List[BatchTimeOperation]
            ] = OrderedDict({i: [] for i in self.selected_cols.get("image", [])})

            for tfm in self.batch_transforms:
                if tfm.arg in feature_transforms:
                    feature_transforms[tfm.arg].append(tfm)

            # Each feature that will be transformed needs to have its own transformation
            # processor. These processors need to correspond to the index of the feature
            # to be transformed because at batch time, the feature name is unavailable -
            # we only have the feature index. Finally, we only leave transformations if
            # the 'step' corresponds to the 'step' of the Dataset. This is to optimise
            # for efficiency only since the processor will ignore transformations that
            # are not relevant to the current step at batch time anyway.
            self.processors: Dict[int, TransformationProcessor] = {
                list(feature_transforms).index(col): TransformationProcessor(
                    [
                        cast(Transformation, i)
                        for i in tfms
                        if i.step == self.batch_transformation_step
                    ],
                )
                for col, tfms in feature_transforms.items()
            }

    def _transform_image(self, img: np.ndarray, idx: int) -> np.ndarray:
        """Performs image transformations if they have been specified.

        Args:
            img: The image to be transformed.
            idx: The index of the image.

        Returns:
            The transformed image.

        """
        if not self.batch_transforms:
            return img

        self.batch_transformation_step = cast(
            Literal["train", "validation"], self.batch_transformation_step
        )
        return self.processors[idx].batch_transform(
            img, step=self.batch_transformation_step
        )

    def _load_images(
        self, idx: Union[int, Sequence[int]]
    ) -> Union[np.ndarray, Tuple[np.ndarray, ...]]:
        """Loads images and performs transformations if specified.

        This involves first converting grayscale images to RGB if necessary.

        Args:
            idx: The index to be loaded.

        Returns:
            Loaded and transformed image.

        """
        img_features = self.image[idx]
        imgs: Tuple[np.ndarray, ...] = tuple(
            io.imread(image, plugin="pil") for image in img_features
        )
        imgs = tuple(
            color.gray2rgb(image_array) if len(image_array.shape) < 3 else image_array
            for image_array in imgs
        )
        imgs = tuple(
            self._transform_image(image_array, i) for i, image_array in enumerate(imgs)
        )

        if len(img_features) == 1:
            return imgs[0]

        return imgs

    def _set_support_column_values(self, data: pd.DataFrame) -> None:
        """Sets `self.support_cols` - auxiliary columns for loss manipulation."""
        if self.weights_col:
            weights = data.loc[:, [self.weights_col]].values.astype(np.float32)
            self.x_columns.append(self.weights_col)
        else:
            weights = np.ones(len(data), dtype=np.float32)
        weights = weights.reshape(len(weights), 1)

        if self.ignore_classes_col:
            ignore_classes = data.loc[:, [self.ignore_classes_col]].values.astype(
                np.int64
            )
        else:
            ignore_classes = -np.ones(len(data), dtype=np.int64)
        ignore_classes = ignore_classes.reshape(len(ignore_classes), 1)

        if self.multihead_col:
            category = data.loc[:, [self.multihead_col]].values
            category = category.reshape(len(category), 1)
            self.support_cols = cast(
                np.ndarray, np.concatenate((weights, ignore_classes, category), axis=1)
            )
        else:
            self.support_cols = cast(
                np.ndarray, np.concatenate((weights, ignore_classes), axis=1)
            )

    def _set_image_values(self, data: pd.DataFrame) -> None:
        """Sets `self.image`."""
        if self.image_columns != []:
            for (i, col) in enumerate(self.image_columns):
                x_img = np.expand_dims(data.loc[:, col].values, axis=1)
                if i == 0:
                    self.image = x_img

                else:
                    self.image = np.concatenate((self.image, x_img), axis=1)
        else:
            self.image = np.array([])

    def _set_tabular_values(self, data: pd.DataFrame) -> None:
        """Sets `self.tabular`."""
        x1_var = data.loc[:, self.embedded_col_names].values.astype(np.int64)
        x2_var = data.loc[:, self.selected_cols.get("continuous", [])].values.astype(
            np.float32
        )
        self.tabular = np.concatenate((x1_var, x2_var), axis=1)

    def _set_target_values(
        self, target: Optional[Union[pd.DataFrame, pd.Series]]
    ) -> None:
        """Sets `self.y_var`."""
        if target is not None:
            self.y_var = cast(np.ndarray, target.values)
        else:
            self.y_var = np.array([])

    def _get_xy(
        self, data: pd.DataFrame
    ) -> Tuple[pd.DataFrame, Optional[Union[pd.DataFrame, pd.Series]]]:
        """Returns the x and y variables.

        By default, there is no target unless `self.target` has been specified.
        """
        X, Y = data, None

        if self.target is not None:
            X = X.drop(columns=self.target).reset_index(drop=True)
            Y = data[self.target].reset_index(drop=True)
        return X, Y

    def _getitem(
        self, idx: Union[int, Sequence[int]]
    ) -> Tuple[Tuple[Union[np.ndarray, Tuple[np.ndarray, ...]], ...], np.ndarray]:
        """Returns the item referenced by index `idx` in the data."""
        image: Union[np.ndarray, Tuple[np.ndarray, ...]]
        tab: np.ndarray
        sup: np.ndarray

        # Set the target, if the dataset has no supervision,
        # choose set the default value to be 0.
        target = self.y_var[idx] if len(self.y_var) else np.array(0)

        # If the Dataset contains both tabular and image data
        if self.image.size and self.tabular.size:
            tab = self.tabular[idx]
            sup = self.support_cols[idx]
            image = self._load_images(idx)
            return (tab, image, sup), target

        # If the Dataset contains only tabular data
        elif self.tabular.size:
            tab = self.tabular[idx]
            sup = self.support_cols[idx]
            return (tab, sup), target

        # If the Dataset contains only image data
        else:
            sup = self.support_cols[idx]
            image = self._load_images(idx)
            return (image, sup), target


class _BitfountDataset(_BaseBitfountDataset):
    """A dataset for supervised tasks.

    When indexed, returns numpy arrays corresponding to
    categorical features, continuous features, weights and target value (and
    optionally category)
    """

    def __init__(
        self,
        data: pd.DataFrame,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.data = data
        X, Y = self._get_xy(data)

        self._set_image_values(X)
        self._set_tabular_values(X)
        self._set_support_column_values(X)
        # Package tabular, image and support columns together under the x_var attribute
        self.x_var = (self.tabular, self.image, self.support_cols)
        self._set_target_values(Y)

    def __len__(self) -> int:
        return len(self.x_var[0])


class _IterableBitfountDataset(_BaseBitfountDataset):
    """Iterable Dataset.

    Currently, this is only used for Database connections.
    """

    def __init__(
        self,
        db: DatabaseLoader,
        sql_query: str,
        max_row_buffer: int = 500,
        **kwargs: Any,
    ):
        super().__init__(**kwargs)
        self.db = db
        self.sql_query = sql_query
        self.max_row_buffer = max_row_buffer

    @cached_property
    def _len(self) -> int:
        """Cached length of the dataset.

        This is only computed once as it could be very slow to compute depending on the
        query.
        """
        with self.db.con.connect() as con:
            # Ignoring the security warning because the sql query is trusted and will
            # be executed regardless.
            result = con.execute(
                text(f"SELECT COUNT(*) FROM ({self.sql_query}) q")  # nosec
            )
            return cast(int, result.scalar_one())

    def __iter__(
        self,
    ) -> Iterator[
        Tuple[Tuple[Union[np.ndarray, Tuple[np.ndarray, ...]], ...], np.ndarray]
    ]:
        with self.db.con.connect() as con:
            result = con.execution_options(
                stream_results=True, max_row_buffer=self.max_row_buffer
            ).execute(text(self.sql_query))
            for partition in result.partitions(_DATABASE_PARTITION_SIZE):
                data = pd.DataFrame(partition, columns=list(result.keys()))
                self.data = data
                X, Y = self._get_xy(data)
                # TODO: [BIT-1559] Apply schema to data here
                self._set_image_values(X)
                self._set_tabular_values(X)
                self._set_support_column_values(X)
                # Package tabular, image and support columns together under the x_var
                # attribute
                self.x_var = (self.tabular, self.image, self.support_cols)
                self._set_target_values(Y)

                for idx in range(len(data)):
                    yield self._getitem(idx)

    def __len__(self) -> int:
        return self._len
