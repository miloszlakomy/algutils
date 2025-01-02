import os
import re
import sys
from typing import Any


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
