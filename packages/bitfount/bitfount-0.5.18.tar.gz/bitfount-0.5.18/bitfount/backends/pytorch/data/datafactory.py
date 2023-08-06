"""PyTorch implementations of the datafactory module contents."""
from typing import Any, List, Literal, Mapping, Optional, Union

import pandas as pd

from bitfount.backends.pytorch.data.dataloaders import (
    _BasePyTorchBitfountDataLoader,
    _PyTorchBitfountDataLoader,
    _PyTorchIterableBitfountDataLoader,
)
from bitfount.backends.pytorch.data.datasets import (
    _PyTorchDataset,
    _PyTorchIterableDataset,
)
from bitfount.data.datafactory import _DataFactory
from bitfount.data.datasets import _BaseBitfountDataset
from bitfount.data.types import _SemanticTypeValue
from bitfount.transformations.batch_operations import BatchTimeOperation


class _PyTorchDataFactory(_DataFactory):
    """A PyTorch-specific implementation of the DataFactory provider."""

    def create_dataloader(
        self,
        data: _BaseBitfountDataset,
        batch_size: Optional[int] = None,
    ) -> _BasePyTorchBitfountDataLoader:
        """See base class."""
        if isinstance(data, _PyTorchIterableDataset):
            return _PyTorchIterableBitfountDataLoader(
                dataset=data, batch_size=batch_size
            )
        elif isinstance(data, _PyTorchDataset):
            return _PyTorchBitfountDataLoader(data, batch_size=batch_size)

        raise TypeError(
            "The _PyTorchDataFactory class only supports "
            "subclasses of PyTorch Dataset for creating a DataLoader."
        )

    def create_dataset(
        self,
        data: pd.DataFrame,
        selected_cols: Mapping[_SemanticTypeValue, List[str]],
        target: Optional[Union[str, List[str]]] = None,
        batch_transforms: Optional[List[BatchTimeOperation]] = None,
        batch_transformation_step: Optional[Literal["train", "validation"]] = None,
        **kwargs: Any,
    ) -> Union[_PyTorchDataset, _PyTorchIterableDataset]:
        """See base class."""
        # TODO: [BIT-1559] Add the option for returning an iterable dataset here
        return _PyTorchDataset(
            data=data,
            target=target,
            selected_cols=selected_cols,
            batch_transforms=batch_transforms,
            batch_transformation_step=batch_transformation_step,
            **kwargs,
        )
