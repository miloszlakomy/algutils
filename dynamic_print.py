import inspect
import io
import re
import shutil
from typing import Any


def dprint(name: str, value: Any = None) -> None:
    if value is None:
        value = _parent_locals()[name]

    _DynamicPrintSingleton.set_name_to_value(name, value)
    _DynamicPrintSingleton.dprint()


def finish() -> None:
    _DynamicPrintSingleton.finish()


def clear_and_finish() -> None:
    _DynamicPrintSingleton.clear_and_finish()


def _parent_locals(depth:int = 1) -> dict[str, Any]:
    return inspect.getouterframes(inspect.currentframe())[depth+1][0].f_locals


class _DynamicPrintSingleton:
    _names: list[str] = []
    _names_to_values: dict[str, str] = {}
    _last_print: str = ""

    def __init__(self) -> None:
        raise NotImplementedError()

    @staticmethod
    def set_name_to_value(name: str, value: Any) -> None:
        str_value = str(value)

        if name not in _DynamicPrintSingleton._names_to_values:
            _DynamicPrintSingleton._names.append(name)

        last_value_length = 0
        if name in _DynamicPrintSingleton._names_to_values:
            last_value_length = len(_DynamicPrintSingleton._names_to_values[name])

        # Overwrite last value with space characters
        _DynamicPrintSingleton._names_to_values[name] = str_value + " " * (
            last_value_length - len(str_value)
        )

    @staticmethod
    def dprint() -> None:
        _DynamicPrintSingleton._clear()
        _DynamicPrintSingleton._reset_cursor()
        _DynamicPrintSingleton._print_all()

    @staticmethod
    def finish() -> None:
        _DynamicPrintSingleton._names.clear()
        _DynamicPrintSingleton._names_to_values.clear()
        _DynamicPrintSingleton._last_print = ""

    @staticmethod
    def clear_and_finish() -> None:
        _DynamicPrintSingleton._clear()
        _DynamicPrintSingleton._reset_cursor()
        _DynamicPrintSingleton.finish()

    @staticmethod
    def _clear() -> None:
        _DynamicPrintSingleton._reset_cursor()
        # re ignores newlines
        print(
            re.sub(pattern=".", repl=" ", string=_DynamicPrintSingleton._last_print),
            end="",
        )

    @staticmethod
    def _print_all() -> None:
        stream = io.StringIO()

        for name in _DynamicPrintSingleton._names:
            value = _DynamicPrintSingleton._names_to_values[name]
            stream.write(f"{name}={value}\n")

        print(
            stream.getvalue(),
            end="",
        )

        _DynamicPrintSingleton._last_print = stream.getvalue()

    @staticmethod
    def _reset_cursor() -> None:
        _DynamicPrintSingleton._move_cursor_up(
            number_of_lines=_str_height(_DynamicPrintSingleton._last_print)
        )

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
