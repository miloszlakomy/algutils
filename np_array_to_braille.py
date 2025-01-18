from typing import Any

from nptyping import Bool, NDArray
import numpy as np

from algutils.int_to_braille import int_to_braille


Char = str


def np_array_to_braille(a: NDArray[Any, Bool]) -> str:
    """np_array_to_braille

    a = np.array([
    [False, True , True ],
    [True , False, True ],
    [False, True , True ],
    [True , False, True ],
    [True , True , True ],
    ])

    ->

    ⡪⡇
    ⠉⠁
    """
    cols, rows = a.shape

    return "\n".join(
        "".join(
            np_array_to_braille_character(_pad(a[y : y + 4, x : x + 2]))
            for x in range(0, rows, 2)
        )
        for y in range(0, cols, 4)
    )


def np_array_to_braille_character(a: NDArray[Any, Bool]) -> Char:
    """np_array_to_braille_character

    np.array([
    [False, True ],
    [True , False],
    [False, True ],
    [True , True ],
    ])

    -> '⣪'
    """
    return int_to_braille(sum(int(v) * 2**i for i, v in enumerate(a.ravel()[:8])))


def _pad(a: NDArray[Any, Bool]) -> NDArray[Any, Bool]:
    shape = (4, 2)

    if a.shape == shape:
        return a

    b = np.full(shape, False)
    b[: a.shape[0], : a.shape[1]] = a

    return b
