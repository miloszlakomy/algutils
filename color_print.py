import os
import pprint as pp
from typing import Any, Optional

import pygments
import pygments.formatter
import pygments.formatters
import pygments.lexer
import pygments.lexers
import pygments.style
import rich.console

import algutils.utils


def cprint(*values: list[Any], **print_options: dict[str, Any]) -> None:
    if (
        os.getenv("COLOR", default="").lower() == "always"
        or algutils.utils.is_stdout_a_terminal()
    ):
        print(
            *(cformat(value) for value in values),
            **print_options,
        )  # type: ignore[call-overload]
    else:
        print(*values, **print_options)  # type: ignore[call-overload]


def cformat(*values: list[Any], sep=" ", end="") -> str:
    joined_values = sep.join(values) + end
    highlighted_str = _highlight(joined_values)

    return highlighted_str


def cpprint(*values: list[Any], **print_options: dict[str, Any]) -> None:
    if (
        os.getenv("COLOR", default="").lower() == "always"
        or algutils.utils.is_stdout_a_terminal()
    ):
        print(
            *(cpformat(value) for value in values),
            **print_options,
        )  # type: ignore[call-overload]
    else:
        print(*values, **print_options)  # type: ignore[call-overload]


def cpformat(*values: list[Any], sep=" ", end="") -> str:
    joined_values = sep.join(values) + end
    formatted_str = pp.pformat(joined_values)
    highlighted_formatted_str = _highlight(formatted_str)

    return highlighted_formatted_str


def _highlight(
    value: Any,
    lexer: Optional[pygments.lexer.Lexer] = None,
    style: pygments.style.Style = "borland",
) -> str:
    if lexer is None:
        lexer = pygments.lexers.PythonLexer(
            stripall=False,
            stripnl=False,
            ensurenl=False,
        )

    str_value = str(value)

    highlighted_str = pygments.highlight(
        code=str_value,
        lexer=lexer,
        formatter=_determine_formatter(style=style),
    )

    highlighted_str_without_ansi_underlines = _remove_ansi_underlines(highlighted_str)

    return highlighted_str_without_ansi_underlines


def _determine_formatter(
    style: pygments.style.Style,
) -> pygments.formatter.Formatter[Any]:
    color_support = rich.console.Console().style

    formatter_cls: type[pygments.formatter.Formatter[Any]]
    if color_support == "truecolor":
        formatter_cls = pygments.formatters.TerminalTrueColorFormatter
    elif color_support == "256":
        formatter_cls = pygments.formatters.Terminal256Formatter
    else:
        formatter_cls = pygments.formatters.TerminalFormatter

    formatter = formatter_cls(style=style)

    return formatter


def _remove_ansi_underlines(ansi_string: str) -> str:
    # Define the ANSI escape codes for underlining
    underline_ansi_escape_codes = {
        # Underline start
        "\x1b[4m",
        "\x1b[04m",
        # Underline end
        "\x1b[24m",
    }

    # Remove underline start and end codes
    for pattern in underline_ansi_escape_codes:
        ansi_string = ansi_string.replace(pattern, "")

    return ansi_string
