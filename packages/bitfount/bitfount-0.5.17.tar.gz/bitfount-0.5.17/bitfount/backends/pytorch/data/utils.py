"""PyTorch data utility functions to be found here."""
from typing import Sequence, Union, cast

import torch


def _index_tensor_handler(
    idx: Union[int, Sequence[int], torch.Tensor]
) -> Union[int, Sequence[int]]:
    """Converts pytorch tensors to integers or lists of integers for indexing."""
    if torch.is_tensor(idx):
        idx = cast(torch.Tensor, idx)
        list_idx: list = idx.tolist()
        return list_idx
    else:
        idx = cast(Union[int, Sequence[int]], idx)
        return idx
