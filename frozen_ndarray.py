from typing import Any, Optional

from nptyping import NDArray
import numpy as np


class FrozenNDArray(np.ndarray[Any, Any]):
    def __new__(cls, *args: list[Any], **kwargs: dict[str, Any]) -> NDArray[Any, Any]:
        input_array: Optional[NDArray[Any, Any]] = None
        if args and isinstance(args[0], np.ndarray):
            input_array = args[0]
            args = args[1:]
        if "input_array" in kwargs:
            if input_array is not None:
                raise TypeError(
                    "FrozenNDArray() got multiple values for argument 'input_array'"
                )
            if not isinstance(kwargs["input_array"], np.ndarray):
                raise TypeError(
                    "FrozenNDArray() argument `input_array' must be an np.ndarray,"
                    f" actual type `{type(kwargs["input_array"])}',"
                    f" value `{kwargs["input_array"]}'"
                )
            input_array = kwargs.pop("input_array")

        if input_array is not None:
            if args or kwargs:
                raise ValueError(
                    "If FrozenNDArray() argument `input_array' is set,"
                    f" no other arguments are allowed. input_array=`{input_array}',"
                    f" args=`{args}', kwargs=`{kwargs}'"
                )

            obj = input_array.copy().view(cls)
            obj.setflags(write=False)
            return obj

        return FrozenNDArray(input_array=np.array(*args, **kwargs))

    def __hash__(self) -> int:  # type: ignore[override]
        return hash(self.tobytes())

    def __bool__(self) -> bool:
        return set(self.flat) in [{}, {True}]
