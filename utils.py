from collections.abc import Iterable
import os
import re
import sys
from typing import Any


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
