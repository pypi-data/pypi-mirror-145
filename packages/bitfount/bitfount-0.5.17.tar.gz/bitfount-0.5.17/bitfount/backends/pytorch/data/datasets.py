"""PyTorch implementations for Bitfount Dataset classes."""
from typing import Sequence, Tuple, Union

import numpy as np
import torch
from torch.utils.data import Dataset as PTDataset
from torch.utils.data import IterableDataset as PTIterableDataset

from bitfount.backends.pytorch.data.utils import _index_tensor_handler
from bitfount.data.datasets import _BitfountDataset, _IterableBitfountDataset


class _PyTorchDataset(_BitfountDataset, PTDataset):
    """See base class."""

    def __getitem__(
        self, idx: Union[int, Sequence[int], torch.Tensor]
    ) -> Tuple[Tuple[Union[np.ndarray, Tuple[np.ndarray, ...]], ...], np.ndarray]:
        idx = _index_tensor_handler(idx)
        return self._getitem(idx)


class _PyTorchIterableDataset(_IterableBitfountDataset, PTIterableDataset):
    """See base class."""

    pass
