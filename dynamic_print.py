import shutil
from typing import Any


def dprint(name: str, value: Any) -> None:
    _DynamicPrintSingleton.set_name_to_value(name, value)
    _DynamicPrintSingleton.dprint()


def finish() -> None:
    _DynamicPrintSingleton.finish()


def clear_and_finish() -> None:
    _DynamicPrintSingleton.clear_and_finish()


class _DynamicPrintSingleton:
    _names: list[str] = []
    _names_to_values: dict[str, str] = {}
    _last_number_of_lines_printed: int = 0

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
        _DynamicPrintSingleton._reset_cursor()
        _DynamicPrintSingleton._print_all()

    @staticmethod
    def finish() -> None:
        _DynamicPrintSingleton._names.clear()
        _DynamicPrintSingleton._names_to_values.clear()
        _DynamicPrintSingleton._last_number_of_lines_printed = 0

    @staticmethod
    def clear_and_finish() -> None:
        terminal_width = shutil.get_terminal_size().columns

        _DynamicPrintSingleton._reset_cursor()
        for _ in range(_DynamicPrintSingleton._last_number_of_lines_printed):
            print(" " * terminal_width)
        _DynamicPrintSingleton._reset_cursor()

        _DynamicPrintSingleton.finish()

    @staticmethod
    def _print_all() -> None:
        for name in _DynamicPrintSingleton._names:
            value = _DynamicPrintSingleton._names_to_values[name]
            print(f"{name}={value}")

        _DynamicPrintSingleton._last_number_of_lines_printed = len(
            _DynamicPrintSingleton._names
        )

    @staticmethod
    def _reset_cursor() -> None:
        _DynamicPrintSingleton._move_cursor_up(
            number_of_lines=_DynamicPrintSingleton._last_number_of_lines_printed
        )

    @staticmethod
    def _move_cursor_up(number_of_lines: int) -> None:
        print(f"\033[{number_of_lines + 1}A")
