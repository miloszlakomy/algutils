#!/usr/bin/env python3

import os.path
import sys

# Allow running the script without explicitly setting PYTHONPATH.
# Not the best solution but hey, as long as it works.
sys.path += [
    os.path.dirname(os.path.dirname(os.path.dirname(os.path.realpath(__file__))))
]

import numpy as np
import typing
import termios
import contextlib
from algutils.utils import *
from algutils.np_array_to_braille import np_array_to_braille
from algutils.braille_canvas import BrailleCanvas, Point, Rectangle


def map_coords(coord: Point, src: Rectangle, dst: Rectangle) -> Point:
    scale = Point(x=dst.width / src.width, y=dst.height / src.height)
    offset = Point(x=dst.left - src.left * scale.x, y=dst.top - src.top * scale.y)
    return Point(x=coord.x * scale.x + offset.x, y=coord.y * scale.y + offset.y)


class Characters:
    """
    Set of characters used to draw plot axes.
    """

    AXIS_X = "═"
    AXIS_X_END = "▶"
    AXIS_Y = "║"
    AXIS_Y_END = "▲"
    AXIS_ORIGIN = "╚"


class Escapes:
    """
    ANSI escape codes used to adjust terminal output.
    See https://gist.github.com/ConnerWill/d4b6c776b509add763e17f9f113fd25b
    """

    ENABLE_ALTERNATE_SCREEN = b"\x1b[?1049h"
    DISABLE_ALTERNATE_SCREEN = b"\x1b[?1049l"
    HIDE_CURSOR = b"\x1b[?25l"
    SHOW_CURSOR = b"\x1b[?25h"

    # 0;0 are 0-based line;column coordinates, with top-left being 0;0.
    MOVE_CURSOR_TO_ORIGIN = b"\x1b[0;0H"


def ansi_scoped_enable(enable: bytes, disable: bytes):
    if os.isatty(sys.stdout.fileno()):
        sys.stdout.buffer.write(enable)
        sys.stdout.flush()
    try:
        yield
    finally:
        if os.isatty(sys.stdout.fileno()):
            sys.stdout.buffer.write(disable)
            sys.stdout.flush()


@contextlib.contextmanager
def hide_cursor():
    yield from ansi_scoped_enable(Escapes.HIDE_CURSOR, Escapes.SHOW_CURSOR)


@contextlib.contextmanager
def use_alternate_screen():
    """
    Switches to terminal's "alternate screen", clearing the plot from terminal on exit.
    """
    yield from ansi_scoped_enable(
        Escapes.ENABLE_ALTERNATE_SCREEN,
        Escapes.DISABLE_ALTERNATE_SCREEN,
    )


class Plot:
    def __init__(self, series: typing.List[float]):
        if os.isatty(sys.stdout.fileno()):
            self.term_rows, self.term_cols = termios.tcgetwinsize(sys.stdout)
        else:
            self.term_rows, self.term_cols = (
                os.getenv("ROWS", default=50),
                os.getenv("COLS", default=200),
            )
        self.series = series
        y_tics = [
            min(series)
            + (max(series) - min(series))
            * (idx / (self.term_rows - self.x_axis_margin - 1))
            for idx in range(self.term_rows - self.x_axis_margin)
        ]
        self.y_tics = list(reversed(["{:.02f}".format(tic) for tic in y_tics]))
        # -1 for the axis lines
        self.canvas = BrailleCanvas(
            char_rows=self.term_rows - self.x_axis_margin - 1,
            char_columns=self.term_cols - self.y_axis_margin - 1,
        )

        # Rectangles representing the value (src) and canvas (dst) coordinate space
        # Used to convert incoming value series into something canvas will understand
        src_rect = Rectangle(
            top_left=Point(x=float(0), y=max(series)),
            bottom_right=Point(x=float(len(series)), y=min(series)),
        )
        dst_rect = self.canvas.bounds_rectangle()

        if src_rect.width == 0 or src_rect.height == 0:
            return

        def convert(point: Point):
            mapped = map_coords(point, src_rect, dst_rect)
            # BrailleCanvas expects y,x order
            return (mapped.y, mapped.x)

        points = [convert(Point(x=idx, y=val)) for idx, val in enumerate(series)]

        for u, v in zip(points[:-1], points[1:]):
            self.canvas.draw_line(u, v)

    @property
    def x_axis_margin(self) -> int:
        """
        Number of terminal columns reserved for y axis labels,
        Does not include space use by the axis itself.
        """
        return 1

    @property
    def y_axis_margin(self) -> int:
        """
        Number of terminal columns reserved for y axis labels.
        Does not include space use by the axis itself.
        """
        if self.y_tics:
            return max(len(tic) for tic in self.y_tics) + 1
        else:
            return 0

    @property
    def x_axis(self) -> typing.List[str]:
        """
        A list of strings representing the entire line containing the X axis of
        the plot and its labels.

        The elements are intended to be appended to rendered plot, one element
        per line.

        First element includes padding for the labels of the Y axis and
        ASCII-art of the X-axis.

        Second element includes min and max values of the visible plot.
        It's not really related to the X axis, but oh well.
        """
        lines = [
            (" " * self.y_axis_margin)
            + Characters.AXIS_ORIGIN
            + (Characters.AXIS_X * (self.term_cols - self.y_axis_margin - 3))
            + Characters.AXIS_X_END
        ]
        lines += ["min = {}; max = {}".format(min(self.series), max(self.series))]
        return lines

    @property
    def y_axis(self) -> typing.List[str]:
        """
        A list of strings representing the Y axis and its labels.

        Each element includes a Y-axis label, optionally left-padded, and a
        part of the ASCII-art of the Y axis.
        Each element should be prepended to corresponding line of the braille plot.
        """
        top_fmt = "{{:>{}}} {}".format(self.y_axis_margin - 1, Characters.AXIS_Y_END)
        mid_fmt = "{{:>{}}} {}".format(self.y_axis_margin - 1, Characters.AXIS_Y)
        return [top_fmt.format(self.y_tics[0])] + [
            mid_fmt.format(tic) for tic in self.y_tics[1:]
        ]

    def __str__(self) -> str:
        plot = str(self.canvas)
        plot_lines = plot.split("\n")
        lines = [
            prefix + plot_line for prefix, plot_line in zip(self.y_axis, plot_lines)
        ]
        lines += self.x_axis
        return "\n".join(lines)


def main():
    try:
        with hide_cursor(), use_alternate_screen():
            series = []
            for line in sys.stdin:
                value = float(line)
                series = (series + [value])[-100:]
                if os.isatty(sys.stdout.fileno()):
                    sys.stdout.buffer.write(Escapes.MOVE_CURSOR_TO_ORIGIN)
                else:
                    sys.stdout.write("\n")
                sys.stdout.write(str(Plot(series)))
                sys.stdout.flush()
    except KeyboardInterrupt:
        # do clean exit on Ctrl+C
        pass


if __name__ == "__main__":
    main()
