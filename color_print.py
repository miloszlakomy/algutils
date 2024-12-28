import pprint as pp
from typing import Any

import pygments
import pygments.formatters
import pygments.lexer
import pygments.lexers


def cprint(value: Any) -> None:
    print(cformat(value))


def cformat(value: Any) -> str:
    highlighted_str = _highlight(value)

    return highlighted_str


def cpprint(value: Any) -> None:
    print(cpformat(value))


def cpformat(value:Any) -> str:
    formatted_str = pp.pformat(value)
    highlighted_formatted_str = _highlight(formatted_str, value_type = type(value))

    return highlighted_formatted_str


def _highlight(value: Any, lexer: pygments.lexer.Lexer = None, value_type: type = None) -> str:
    if lexer is None:
        lexer = _guess_lexer(
            value=value,
            value_type=value_type,
        )

    str_value = str(value)

    highlighted_str = pygments.highlight(
        code=str_value,
        lexer=lexer,
        formatter=pygments.formatters.TerminalFormatter(),
    )

    return highlighted_str


def _guess_lexer(value: Any, value_type: type) -> pygments.lexer.Lexer:
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
