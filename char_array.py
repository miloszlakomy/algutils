import re
from typing import Any, Optional, TextIO

from nptyping import NDArray
from nptyping.typing_ import Str
import numpy as np


Char = Str
CharArray = NDArray[Any, Char]


class OutOfCharArrayIndexError(IndexError):
    @staticmethod
    def matches(e: IndexError) -> bool:
        return bool(
            re.match(
                pattern=r"index \d+ is out of bounds for axis \d+ with size \d+",
                string=str(e),
            )
        )

    @staticmethod
    def cast_if_matches(e: IndexError) -> IndexError:
        if OutOfCharArrayIndexError.matches(e):
            return OutOfCharArrayIndexError(e)
        return e


def load_char_array(input_file: TextIO) -> CharArray:
    char_array = np.loadtxt(input_file, dtype=str, comments=None)
    char_array = char_array.view("U1").reshape(char_array.size, -1)

    return char_array


def print_char_array(char_array: CharArray, prefix: Optional[str] = None) -> None:
    print(char_array_to_pretty_string(char_array, prefix))


def char_array_to_pretty_string(
    char_array: CharArray, prefix: Optional[str] = None
) -> str:
    string = "\n".join("".join(row_str) for row_str in char_array)

    if prefix is not None:
        string = f"{prefix}\n{string}"

    return string
