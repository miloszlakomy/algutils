import pprint as pp
from typing import Any, Optional

import pygments
import pygments.formatter
import pygments.formatters
import pygments.lexer
import pygments.lexers
import pygments.style
import rich.console


def cprint(value: Any) -> None:
    print(cformat(value))


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
        lexer = _guess_lexer(
            value=value,
            value_type=value_type,
        )

    str_value = str(value)

    highlighted_str = pygments.highlight(
        code=str_value,
        lexer=lexer,
        formatter=_determine_formatter(style=style),
    )

    return highlighted_str.removesuffix("\n")


def _guess_lexer(value: Any, value_type: Optional[type]) -> pygments.lexer.Lexer:
    if value_type is None:
        value_type = type(value)

    if value_type is not str:
        return pygments.lexers.PythonLexer()

    str_value = value

    try:
        lexer = pygments.lexers.guess_lexer(str_value)
    except pygments.util.ClassNotFound:
        lexer = pygments.lexers.PythonLexer()

    highlighted_str = _highlight(
        value=value,
        lexer=lexer,
    )

    ansi_esc_code_start_sequence = "\x1b["
    if ansi_esc_code_start_sequence in highlighted_str:
        return lexer

    return pygments.lexers.PythonLexer()


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
