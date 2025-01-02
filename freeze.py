from collections.abc import Hashable
import typing
from typing import Any

import numpy as np

from algutils.frozen_ndarray import FrozenNDArray
from algutils.utils import is_hashable


def freeze(x: Any) -> Hashable:
    if hasattr(x, "__next__"):  # Iterator
        return tuple(freeze(y) for y in x)

    if is_hashable(x):
        return typing.cast(Hashable, x)

    if isinstance(x, (list, tuple)):
        return tuple(freeze(y) for y in x)

    if isinstance(x, set):
        return frozenset(freeze(y) for y in x)

    if isinstance(x, np.ndarray):
        return FrozenNDArray(x)

    raise UnsupportedFreezeType(type(x))


class UnsupportedFreezeType(TypeError):
    pass
