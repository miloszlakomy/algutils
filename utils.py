from abc import abstractmethod
from collections.abc import Iterable
from copy import deepcopy
from itertools import chain, dropwhile
import math
from numbers import Integral, Real
import os
import random
import re
import sys
from typing import (
    Any,
    Generator,
    Iterator,
    Optional,
    SupportsFloat,
    SupportsIndex,
    Type,
    TypeVar,
)

import numpy as np
from nptyping import NDArray


T = TypeVar("T")


class Vector:
    @abstractmethod
    def __iter__(self) -> Iterator[SupportsFloat | SupportsIndex]:
        pass

    @abstractmethod
    def __getitem__(self, index: Any) -> Any:
        pass

    @abstractmethod
    def __setitem__(self, index: Any, value: Any) -> None:
        pass

    @abstractmethod
    def __len__(self) -> int:
        pass

    @abstractmethod
    def __add__(self, other: Any) -> Any:
        pass

    @abstractmethod
    def __sub__(self, other: Any) -> Any:
        pass

    @abstractmethod
    def __mul__(self, other: Any) -> Any:
        pass

    @abstractmethod
    def __truediv__(self, other: Any) -> Any:
        pass

    @abstractmethod
    def __radd__(self, other: Any) -> Any:
        pass

    @abstractmethod
    def __rsub__(self, other: Any) -> Any:
        pass

    @abstractmethod
    def __rmul__(self, other: Any) -> Any:
        pass

    @abstractmethod
    def __rtruediv__(self, other: Any) -> Any:
        pass


EPSILON = 1e-9


def debug() -> bool:
    return os.getenv("DEBUG") is not None or verbose_debug()


def verbose_debug() -> bool:
    return os.getenv("DEBUG", "").lower() in ["v", "verbose"] or very_verbose_debug()


vdebug = verbose_debug


def very_verbose_debug() -> bool:
    return os.getenv("DEBUG", "").lower() in ["vv", "veryverbose", "very verbose"]


vvdebug = very_verbose_debug


def file_path_to_module_name(file_path: str) -> str:
    return os.path.basename(file_path).removesuffix(".py")


def indent(string: str, times: int) -> str:
    return re.sub(
        pattern=r"(?m)^",
        repl=times * "    ",
        string=string,
    )


def is_hashable(obj: Any) -> bool:
    try:
        _ = hash(obj)
    except TypeError:
        return False
    return True


def is_stdout_a_terminal() -> bool:
    return os.isatty(sys.stdout.fileno())


def iterable_length(iterable: Iterable[Any]) -> int:
    return sum(1 for _ in iterable)


def vector_range(
    start_or_stop: Optional[Vector] = None,
    /,
    stop: Optional[Vector] = None,
    step: Optional[Real | Vector] = None,
    *,
    start: Optional[Vector] = None,
) -> Generator[Vector]:
    if start is None and start_or_stop is None:
        raise ValueError(
            "Arguments `start' and `start_or_stop' can't both be None."
            f" Got `start={start}', start_or_stop=`{start_or_stop}'."
        )

    if start is not None and start_or_stop is not None:
        raise ValueError(
            "Arguments `start' and `start_or_stop' are mutually exclusive."
            f" Got `start={start}', start_or_stop=`{start_or_stop}'."
        )

    if start is not None and stop is None:
        raise ValueError(
            "Argument `stop' is required when argument `start' is set."
            f" Got `start={start}', `stop={stop}'."
        )

    if step is not None and is_scalar_or_vector_almost_zero(step):
        raise ValueError(f"Argument `step' must not be zero. Got `step={step}'.")

    args = (start_or_stop, stop, step, start)
    arg_lens = set()
    for arg in args:
        try:
            arg_lens.add(len(arg))
        except TypeError:  # TypeError: object of type 'NoneType' has no len()
            pass
    if len(arg_lens) != 1:
        raise ValueError(
            f"""
Ambiguous number of dimensions. Got:
`{vector_range.__name__}(
    start_or_stop={start_or_stop},
    /,
    stop={stop},
    step={step},
    *,
    start={start},
)'.
            """.strip()
        )

    number_of_dimensions = next(iter(arg_lens))

    if start is None:
        if stop is None:
            stop = start_or_stop
            start = deepcopy(stop)
            for i in range(number_of_dimensions):
                start[i] = 0
        else:
            start = start_or_stop

    if are_vectors_almost_equal(start, stop):
        return iter([])

    if step is None:
        step = 1

    if isinstance(step, Real):
        step_length = step
        step = deepcopy(stop)
        for i in range(number_of_dimensions):
            step[i] -= start[i]
        step = normalize_vector(step)
        for i in range(number_of_dimensions):
            step[i] *= step_length

    return _impl_vector_range(start, stop, step)


def _impl_vector_range(start: Vector, stop: Vector, step: Vector) -> Generator[Vector]:
    data_types = {type(coordinate) for coordinate in chain(start, stop, step)}
    if any(not issubclass(data_type, Integral) for data_type in data_types):
        if any(issubclass(data_type, Integral) for data_type in data_types):
            non_integral_data_types = {
                data_type
                for data_type in data_types
                if not issubclass(data_type, Integral)
            }

            if len(non_integral_data_types) > 1:
                raise ValueError(
                    f"Ambiguous data type. Got data types: `{data_types}'."
                )

            data_type = next(iter(non_integral_data_types))

            start = _cast_vector_data_type(start, data_type)
            stop = _cast_vector_data_type(stop, data_type)
            step = _cast_vector_data_type(step, data_type)

    number_of_dimensions = len(start)

    difference = deepcopy(stop)
    for i in range(number_of_dimensions):
        difference[i] -= start[i]
    if not are_vectors_almost_collinear(difference, step):
        raise ValueError(
            "`step' not collinear with `stop - start'."
            f" Got `start={start}', `stop={stop}', `step={step}'."
        )

    start_plus_step = deepcopy(start)
    for i in range(number_of_dimensions):
        start_plus_step[i] += step[i]
    if math.dist(start, stop) < math.dist(start_plus_step, stop):
        return

    initial_difference_signs = [np.sign(coord) for coord in difference]

    intermediate = deepcopy(start)
    while (
        not are_vectors_almost_equal(intermediate, stop)
        and initial_difference_signs == [np.sign(coord) for coord in difference]
    ):
        yield deepcopy(intermediate)
        for i in range(number_of_dimensions):
            intermediate[i] += step[i]
            difference[i] -= step[i]


def is_vector_almost_zero(v: Vector) -> bool:
    return all(math.isclose(coordinate, 0, abs_tol=1e-9) for coordinate in v)


def is_scalar_or_vector_almost_zero(value: Real | Vector) -> bool:
    try:
        _ = len(value)
    except TypeError:  # TypeError: object of type 'int' has no len()
        v = [value]
    else:
        v = value
    return is_vector_almost_zero(v)


def normalize_vector(v: Vector) -> Vector:
    number_of_dimensions = len(v)

    zero_vector = deepcopy(v)
    for i in range(number_of_dimensions):
        zero_vector[i] = 0

    v_length = math.dist(zero_vector, v)

    unit_vector = deepcopy(v)
    for i in range(number_of_dimensions):
        unit_vector[i] /= v_length

    return unit_vector


def are_vectors_almost_collinear(u: Vector, v: Vector) -> bool:
    minus_v = deepcopy(v)
    for i in range(len(minus_v)):
        minus_v[i] *= -1

    return (
        are_vectors_almost_equal(normalize_vector(u), normalize_vector(v))
        or are_vectors_almost_equal(normalize_vector(u), normalize_vector(minus_v))
    )


def are_vectors_almost_equal(u: Vector, v: Vector) -> bool:
    if len(u) != len(v):
        raise ValueError(
            "Inconsistent number of dimensions."
            f" Got: `{are_vectors_almost_equal.__name__}(u={u}, v={v})'."
        )

    number_of_dimensions = len(u)

    return all(math.isclose(u_i, v_i, abs_tol=1e-9) for u_i, v_i in zip(u, v))


def _cast_vector_data_type(v: Vector, data_type: Type[T]) -> Vector:
    if isinstance(v, NDArray):
        return v.astype(data_type)

    v_copy = deepcopy(v)
    for i in range(len(v_copy)):
        v_copy[i] = data_type(v_copy[i])
    return v_copy


def vectors_sum(u: Vector, v: Vector) -> Vector:
    if len(u) != len(v):
        raise ValueError(
            "Inconsistent number of dimensions."
            f" Got: `{vectors_sum.__name__}(u={u}, v={v})'."
        )

    number_of_dimensions = len(u)

    w = deepcopy(u)
    for i in range(number_of_dimensions):
        w[i] += v[i]

    return w


def vectors_difference(u: Vector, v: Vector) -> Vector:
    if len(u) != len(v):
        raise ValueError(
            "Inconsistent number of dimensions."
            f" Got: `{vectors_difference.__name__}(u={u}, v={v})'."
        )

    number_of_dimensions = len(u)

    w = deepcopy(u)
    for i in range(number_of_dimensions):
        w[i] -= v[i]

    return w


def multiply_vector(v: Vector, times: float) -> Vector:
    number_of_dimensions = len(v)

    u = deepcopy(v)
    for i in range(number_of_dimensions):
        u[i] *= times

    return u


def jiggle_vector(v: Vector) -> Vector:
    number_of_dimensions = len(v)

    jiggled_vector = deepcopy(v)
    for i in range(number_of_dimensions):
        jiggled_vector[i] += EPSILON * random.uniform(-1, 1)

    return jiggled_vector
