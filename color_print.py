import pprint as pp
from typing import Any, Optional

import pygments
import pygments.formatter
import pygments.formatters
import pygments.lexer
import pygments.lexers
import pygments.style
import rich.console


def cprint(*values: list[Any], **print_options: dict[str, Any]) -> None:
    print(*(cformat(value) for value in values), **print_options)


def cformat(value: Any) -> str:
    highlighted_str = _highlight(value)

    return highlighted_str


def cpprint(value: Any) -> None:
    print(cpformat(value))


def cpformat(value: Any) -> str:
    formatted_str = pp.pformat(value)
    highlighted_formatted_str = _highlight(formatted_str, value_type=type(value))

    return highlighted_formatted_str


def _highlight(
    value: Any,
    lexer: Optional[pygments.lexer.Lexer] = None,
    value_type: Optional[type] = None,
    style: pygments.style.Style = "borland",
) -> str:
    if lexer is None:
        lexer = pygments.lexers.PythonLexer()

    str_value = str(value)

    highlighted_str = pygments.highlight(
        code=str_value,
        lexer=lexer,
        formatter=_determine_formatter(style=style),
    )

    return highlighted_str.removesuffix("\n")


def _determine_formatter(style: pygments.style.Style) -> pygments.formatter.Formatter:
    color_support = rich.console.Console().style

    if color_support == "truecolor":
        formatter_cls = pygments.formatters.TerminalTrueColorFormatter
    elif color_support == "256":
        formatter_cls = pygments.formatters.Terminal256Formatter
    else:
        formatter_cls = pygments.formatters.TerminalFormatter

    formatter = formatter_cls(style=style)

    return formatter
