import inspect
import io
import os
from pprint import pformat
import re
import shutil
from typing import Any

from algutils.color_print import cformat, cpformat


def dprint(
    name: str,
    value: Any = None,
    use_color_print: bool = True,
    use_pprint: bool = True,
    use_pprint_for_strings: bool = False,
) -> None:
    _DPS.dprint(
        name=name,
        value=value,
        use_color_print=use_color_print,
        use_pprint=use_pprint,
        use_pprint_for_strings=use_pprint_for_strings,
    )


def finish() -> None:
    _DPS.finish()


def clear_and_finish() -> None:
    _DPS.clear_and_finish()


def _parent_module_calling_function_locals_and_globals() -> dict[str, Any]:
    return _parent_locals_and_globals(depth=_current_module_frame_depth())


def _parent_locals_and_globals(depth: int = 1) -> dict[str, Any]:
    frame = inspect.getouterframes(inspect.currentframe())[depth + 1][0]

    return {
        **frame.f_globals,
        **frame.f_locals,
    }


def _str_height(arg: Any) -> int:
    s = str(arg)
    lines = s.split("\n")

    height = -1
    terminal_width = shutil.get_terminal_size().columns
    for line in lines:
        height += len(line) // terminal_width + 1

    return height


def _current_module_name() -> str:
    return _file_path_to_module_name(__file__)


def _file_path_to_module_name(file_path: str) -> str:
    return os.path.basename(file_path).removesuffix(".py")


def _current_module_frame_depth() -> int:
    depth = 0
    for frame in inspect.getouterframes(inspect.currentframe()):
        frame_module_name = _file_path_to_module_name(frame.filename)
        if frame_module_name != _current_module_name():
            break
        depth += 1

    return depth - 1


class _DPS:
    """Dynamic print singleton"""

    _names: list[str] = []
    _names_to_values: dict[str, str] = {}
    _last_print: str = ""

    def __init__(self) -> None:
        raise NotImplementedError()

    @staticmethod
    def dprint(
        name: str,
        value: Any,
        use_color_print: bool,
        use_pprint: bool,
        use_pprint_for_strings: bool,
    ) -> None:
        if value is None:
            value = _parent_module_calling_function_locals_and_globals()[name]

        _DPS._set_name_to_value(
            name=name,
            value=value,
            use_color_print=use_color_print,
            use_pprint=use_pprint,
            use_pprint_for_strings=use_pprint_for_strings,
        )

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
    def _set_name_to_value(
        name: str,
        value: Any,
        use_color_print: bool,
        use_pprint: bool,
        use_pprint_for_strings: bool,
    ) -> None:
        if name not in _DPS._names_to_values:
            _DPS._names.append(name)

        last_value_length = 0
        if name in _DPS._names_to_values:
            last_value_length = len(_DPS._names_to_values[name])

        formatters = {
            # Use pprint
            True: {
                # Use color_print
                True: cpformat,
                False: pformat,
            },
            False: {
                True: cformat,
                False: str,
            },
        }

        format_str = formatters[use_pprint_for_strings][use_color_print]
        format_any = formatters[use_pprint][use_color_print]

        if isinstance(value, str):
            str_value = format_str(value)
        else:
            str_value = format_any(value)

        # Overwrite last value with space characters
        _DPS._names_to_values[name] = str_value + " " * (
            last_value_length - len(str_value)
        )

    @staticmethod
    def _clear() -> None:
        _DPS._reset_cursor()
        # Doesn't replace "\n". re ignores newlines with r"."
        print(
            re.sub(pattern=r".", repl=" ", string=_DPS._last_print),
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
