import inspect
import io
import pprint as pp
import re
import shutil
from typing import Any


def dprint(name: str, value: Any = None) -> None:
    _DPS.dprint(name, value)


def finish() -> None:
    _DPS.finish()


def clear_and_finish() -> None:
    _DPS.clear_and_finish()


def _parent_locals(depth: int = 1) -> dict[str, Any]:
    return inspect.getouterframes(inspect.currentframe())[depth + 1][0].f_locals


class _DPS:
    """Dynamic print singleton"""

    _names: list[str] = []
    _names_to_values: dict[str, str] = {}
    _last_print: str = ""

    def __init__(self) -> None:
        raise NotImplementedError()

    @staticmethod
    def set_name_to_value(name: str, value: Any) -> None:
        if name not in _DPS._names_to_values:
            _DPS._names.append(name)

        last_value_length = 0
        if name in _DPS._names_to_values:
            last_value_length = len(_DPS._names_to_values[name])

        if isinstance(value, str):
            str_value = value
        else:
            str_value = pp.pformat(value)

        # Overwrite last value with space characters
        _DPS._names_to_values[name] = str_value + " " * (
            last_value_length - len(str_value)
        )

    @staticmethod
    def dprint(name: str, value: Any = None) -> None:
        if value is None:
            value = _parent_locals()[name]

        _DPS.set_name_to_value(name, value)

        _DPS._clear()
        _DPS._reset_cursor()
        _DPS._print_all()

    @staticmethod
    def finish() -> None:
        _DPS._names.clear()
        _DPS._names_to_values.clear()
        _DPS._last_print = ""

    @staticmethod
    def clear_and_finish() -> None:
        _DPS._clear()
        _DPS._reset_cursor()
        _DPS.finish()

    @staticmethod
    def _clear() -> None:
        _DPS._reset_cursor()
        # re ignores newlines
        print(
            re.sub(pattern=".", repl=" ", string=_DPS._last_print),
            end="",
        )

    @staticmethod
    def _print_all() -> None:
        stream = io.StringIO()

        for name in _DPS._names:
            value = _DPS._names_to_values[name]
            stream.write(f"{name}={value}\n")

        print(
            stream.getvalue(),
            end="",
        )

        _DPS._last_print = stream.getvalue()

    @staticmethod
    def _reset_cursor() -> None:
        _DPS._move_cursor_up(number_of_lines=_str_height(_DPS._last_print))

    @staticmethod
    def _move_cursor_up(number_of_lines: int) -> None:
        print(f"\033[{number_of_lines + 1}A")


def _str_height(arg: Any) -> int:
    s = str(arg)
    lines = s.split("\n")

    height = -1
    terminal_width = shutil.get_terminal_size().columns
    for line in lines:
        height += len(line) // terminal_width + 1

    return height
