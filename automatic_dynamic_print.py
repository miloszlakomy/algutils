import functools
import io
import sys
from typing import Any, Callable, Optional, TextIO

import algutils.dynamic_print
import algutils.utils


def adprint(
    name: str,
    value: Any = None,
    use_color_print: bool = True,
    use_pprint: bool = True,
    use_pprint_for_strings: bool = False,
    cleanup_function: Optional[Callable[[], None]] = None,
) -> None:
    _ADPS.apply_output_captures_once()

    if cleanup_function is not None:
        _ADPS.set_cleanup_function(cleanup_function)

    with _ADPS.InsideADPrintCall():
        algutils.dynamic_print.dprint(
            name=name,
            value=value,
            use_color_print=use_color_print,
            use_pprint=use_pprint,
            use_pprint_for_strings=use_pprint_for_strings,
            skip_module_names={_current_module_name()},
        )


def _current_module_name() -> str:
    return algutils.utils._file_path_to_module_name(__file__)


class _ADPS:
    """Automatic dynamic print singleton"""

    _cleanup_function_called: bool = False
    _currently_inside_adprint_call: bool = False
    _cleanup_function: Callable[[], None] = algutils.dynamic_print.clear_and_finish

    class InsideADPrintCall:
        def __enter__(self) -> None:
            _ADPS._currently_inside_adprint_call = True

        def __exit__(self, *_: list[Any]) -> None:
            _ADPS._currently_inside_adprint_call = False

    def __init__(self) -> None:
        raise NotImplementedError()

    @functools.cache
    @staticmethod
    def apply_output_captures_once() -> None:
        _ADPS._apply_output_capture(sys.stdout)
        _ADPS._apply_output_capture(sys.stderr)

    @staticmethod
    def set_cleanup_function(cleanup_function: Callable[[], None]) -> None:
        _ADPS._cleanup_function = cleanup_function

    @staticmethod
    def _apply_output_capture(stream: TextIO) -> None:
        @functools.wraps(stream.write)
        def write(text: str) -> int:
            if _ADPS._currently_inside_adprint_call:
                _ADPS._cleanup_function_called = False
            if not _ADPS._currently_inside_adprint_call:
                if not _ADPS._cleanup_function_called:
                    _ADPS._cleanup_function_called = True
                    _ADPS._cleanup_function()

            return real_stream_write(text)

        real_stream_write, stream.write = stream.write, write  # type: ignore[method-assign]
