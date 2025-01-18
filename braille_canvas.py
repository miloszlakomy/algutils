from collections import defaultdict
from itertools import chain
import math

import numpy as np

from algutils import utils
from algutils.char_array import char_array_to_string, string_to_char_array
from algutils.np_array_to_braille import np_array_to_braille
from algutils.ordered_set import OrderedSet
from algutils.utils import EPSILON


class BrailleCanvas:
    """BrailleCanvas

    (y, x) coordinates are used.

    (0.0, 0.0) is the first dot.

    Coordinates (1.0, 1.0) are at
    (0.0, 0.0) + (half character width, half character width).

    (0.0, 0.0) corresponds to the dot at (0.0  , 0.0  ).
    (1.0, 1.0) corresponds to the dot at (0.75 , 0.775).

    Note that (2.3, 2.0) is a better fit for (2.0, 2.0) than (1.525, 2.0).

    (2.0, 2.0) corresponds to the dot at (2.3  , 2.0  ).
    (3.0, 3.0) corresponds to the dot at (2.3  , 2.775).
    (4.0, 4.0) corresponds to the dot at (4.4  , 4.0  ).
    (5.0, 5.0) corresponds to the dot at (5.15 , 4.775).
    """

    CHAR_Y_TO_X_RATIO = 2.2
    CHAR_WIDTH = 2.0
    CHAR_HEIGHT = CHAR_WIDTH * CHAR_Y_TO_X_RATIO  # 4.4
    DOTS_ROWS_IN_CHAR = 4
    DOTS_COLS_IN_CHAR = 2
    DOTS_Y_TO_X_RATIO = CHAR_Y_TO_X_RATIO * DOTS_COLS_IN_CHAR / DOTS_ROWS_IN_CHAR
    # 3d array
    CHAR_DOTS_COORDS = np.array([
        [(1.475, 0.7  ), (1.475, 1.475)],
        [(2.225, 0.7  ), (2.225, 1.475)],
        [(3.0  , 0.7  ), (3.0  , 1.475)],
        [(3.775, 0.7  ), (3.775, 1.475)],
    ])
    CHAR_DOTS_MIN_X = min(x for y, x in chain(*CHAR_DOTS_COORDS))
    CHAR_DOTS_MAX_X = max(x for y, x in chain(*CHAR_DOTS_COORDS))
    CHAR_DOTS_MIN_Y = min(y for y, x in chain(*CHAR_DOTS_COORDS))
    CHAR_DOTS_MAX_Y = max(y for y, x in chain(*CHAR_DOTS_COORDS))
    CHAR_DOTS_RIGHT_PADDING = CHAR_DOTS_MIN_X
    CHAR_DOTS_TOP_PADDING = CHAR_DOTS_MIN_Y
    CHAR_DOTS_LEFT_PADDING = CHAR_WIDTH - CHAR_DOTS_MAX_X
    CHAR_DOTS_BOTTOM_PADDING = CHAR_HEIGHT - CHAR_DOTS_MAX_Y
    ALIGNED_CHAR_RECTANGLE_CORNER = (
        (CHAR_DOTS_BOTTOM_PADDING - CHAR_DOTS_TOP_PADDING) / 2,
        (CHAR_DOTS_RIGHT_PADDING - CHAR_DOTS_LEFT_PADDING) / 2,
    )
    CANVAS_ZERO_YX_COORDS = CHAR_DOTS_COORDS[0][0]

    def __init__(self, char_rows: int, char_columns: int) -> None:
        self.char_rows = char_rows
        self.char_columns = char_columns

        self.dots = np.full(
            shape=(
                _BC.DOTS_ROWS_IN_CHAR * char_rows,
                _BC.DOTS_COLS_IN_CHAR * char_columns,
            ),
            fill_value=False,
        )

        self._texts_row_col_to_strings: defaultdict[tuple[int, int], list[str]]
        self._texts_row_col_to_strings = defaultdict(list)

    def draw_point(self, yx_coords: tuple[int, int]) -> None:
        if self._out_of_bounds(yx_coords):
            return

        self.dots[self._closest_dot_row_col(yx_coords)] = True

    def draw_line(
        self,
        start_yx_coords: tuple[int, int],
        stop_yx_coords: tuple[int, int],
        offset: float = 0.0,
    ) -> None:
        start_yx_coords = tuple(utils.jiggle_vector(list(start_yx_coords)))
        stop_yx_coords = tuple(utils.jiggle_vector(list(stop_yx_coords)))

        if 2 * offset >= math.dist(start_yx_coords, stop_yx_coords):
            return

        difference = utils.vectors_difference(
            list(stop_yx_coords),
            list(start_yx_coords),
        )
        normalized_difference = tuple(utils.normalize_vector(list(difference)))
        offset_vector = tuple(
            utils.multiply_vector(list(normalized_difference), times=offset)
        )

        start_yx_coords = tuple(
            utils.vectors_sum(list(start_yx_coords), offset_vector)
        )
        stop_yx_coords = tuple(
            utils.vectors_difference(list(stop_yx_coords), offset_vector)
        )

        dots_row_col_to_draw = OrderedSet()
        for yx_coords in chain(
            utils.vector_range(list(start_yx_coords), list(stop_yx_coords), .5),
            [stop_yx_coords],
        ):
            if self._out_of_bounds(yx_coords):
                continue

            r, c = closest_dot_row_col = self._closest_dot_row_col(yx_coords)

            dots_row_col_to_draw.add(closest_dot_row_col)

            if len(
                dots_row_col_to_draw & {
                    dot_row_col
                    for dot_row_col
                    in (
                        (r-1, c-1), (r-1, c  ), (r-1, c+1),
                        (r  , c-1), (r  , c  ), (r  , c+1),
                        (r+1, c-1), (r+1, c  ), (r+1, c+1),
                    )
                }
            ) > 2:
                dots_row_col_to_draw.pop(index=-2)

        for dot_row_col in dots_row_col_to_draw:
            self.dots[dot_row_col] = True

    def draw_arrow(
        self,
        start_yx_coords: tuple[int, int],
        stop_yx_coords: tuple[int, int],
        arrow_head_side_length: float = 3.5,
        offset: float = 0.0,
    ) -> None:
        start_yx_coords = tuple(utils.jiggle_vector(list(start_yx_coords)))
        stop_yx_coords = tuple(utils.jiggle_vector(list(stop_yx_coords)))

        distance = math.dist(start_yx_coords, stop_yx_coords)
        if 2 * offset >= distance:
            offset = distance / 2 - EPSILON

        difference = utils.vectors_difference(
            list(stop_yx_coords),
            list(start_yx_coords),
        )
        normalized_difference = tuple(utils.normalize_vector(list(difference)))
        offset_vector = tuple(
            utils.multiply_vector(list(normalized_difference), times=offset)
        )

        start_yx_coords = tuple(
            utils.vectors_sum(list(start_yx_coords), offset_vector)
        )
        stop_yx_coords = tuple(
            utils.vectors_difference(list(stop_yx_coords), offset_vector)
        )

        arrow_head_forward_unbound_vector = (
            utils.multiply_vector(
                utils.normalize_vector(
                    utils.vectors_difference(
                        list(stop_yx_coords),
                        list(start_yx_coords),
                    ),
                ),
                arrow_head_side_length,
            )
        )
        # Equilateral triangle.
        arrow_head_vertices_unbound_vectors = [
            (0.0, 0.0),
            rotate_vector_clockwise(
                arrow_head_forward_unbound_vector,
                radians=5 / 6 * math.pi,
            ),
            rotate_vector_counterclockwise(
                arrow_head_forward_unbound_vector,
                radians=5 / 6 * math.pi,
            ),
        ]
        arrow_head_vertices = [
            utils.vectors_sum(
                list(stop_yx_coords),
                list(arrow_head_vertex_unbound_vector),
            )
            for arrow_head_vertex_unbound_vector
            in arrow_head_vertices_unbound_vectors
        ]

        self.draw_line(start_yx_coords, stop_yx_coords)

        for ui, u in enumerate(arrow_head_vertices):
            for v in arrow_head_vertices[ui + 1 :]:
                self.draw_line(u, v)

    def write_text(self, yx_coords: tuple[int, int], text: str) -> None:
        char_row_col = self._yx_coords_to_char_row_col(yx_coords)
        self._texts_row_col_to_strings[char_row_col].append(text)

    def bounds(self) -> tuple[float, float]:
        bottom_right_char_top_left_corner_canvas_yx = (
            (self.char_rows - 1) * _BC.CHAR_HEIGHT,
            (self.char_columns - 1) * _BC.CHAR_WIDTH,
        )

        top_left_dot_canvas_yx = top_left_dot_char_yx = _BC.CHAR_DOTS_COORDS[0][0]

        bottom_right_dot_char_yx = _BC.CHAR_DOTS_COORDS[-1][-1]
        bottom_right_dot_canvas_yx = (
            _BC.CHAR_DOTS_COORDS[-1][-1] + bottom_right_char_top_left_corner_canvas_yx
        )

        return bottom_right_dot_canvas_yx - top_left_dot_canvas_yx

    def __str__(self) -> str:
        braille_array_string = np_array_to_braille(self.dots)
        char_array = string_to_char_array(braille_array_string)

        for (y, x), text in self._texts_row_col_to_strings.items():
            annotation_length = min(
                len(text),
                self.char_columns - x,
            )
            char_array[y, x : x + annotation_length] = list(text[:annotation_length])

        return char_array_to_string(char_array)

    def _out_of_bounds(self, yx_coords: tuple[int, int]) -> bool:
        y, x = yx_coords
        bounds_y, bounds_x = self.bounds()
        return (not 0.0 <= y <= bounds_y) or (not 0.0 <= x <= bounds_x)

    def _yx_coords_to_char_row_col(self, yx_coords: tuple[int, int]) -> tuple[int, int]:
        y, x = yx_coords

        start_y, start_x = _BC.CANVAS_ZERO_YX_COORDS
        canvas_y = y + start_y
        canvas_x = x + start_x

        acrc_y, acrc_x = _BC.ALIGNED_CHAR_RECTANGLE_CORNER
        aligned_canvas_y = canvas_y + acrc_y
        aligned_canvas_x = canvas_x + acrc_x

        char_row = int(aligned_canvas_y / _BC.CHAR_HEIGHT)
        char_row = max(char_row, 0)
        char_row = min(char_row, self.char_rows - 1)

        char_col = int(aligned_canvas_x / _BC.CHAR_WIDTH)
        char_col = max(char_col, 0)
        char_col = min(char_col, self.char_columns - 1)

        char_row_col = (char_row, char_col)
        return char_row_col

    def _closest_dot_row_col(self, yx_coords: tuple[int, int]) -> tuple[int, int]:
        y, x = yx_coords

        start_y, start_x = _BC.CANVAS_ZERO_YX_COORDS
        canvas_y = y + start_y
        canvas_x = x + start_x

        acrc_y, acrc_x = _BC.ALIGNED_CHAR_RECTANGLE_CORNER
        aligned_canvas_y = canvas_y + acrc_y
        aligned_canvas_x = canvas_x + acrc_x

        char_row = int(aligned_canvas_y / _BC.CHAR_HEIGHT)
        char_row = max(char_row, 0)
        char_row = min(char_row, self.char_rows - 1)

        char_col = int(aligned_canvas_x / _BC.CHAR_WIDTH)
        char_col = max(char_col, 0)
        char_col = min(char_col, self.char_columns - 1)

        char_y = canvas_y - char_row * _BC.CHAR_HEIGHT
        char_x = canvas_x - char_col * _BC.CHAR_WIDTH
        char_yx = (char_y, char_x)

        all_char_dot_row_col_indices = [
            (row, col)
            for row in range(_BC.DOTS_ROWS_IN_CHAR)
            for col in range(_BC.DOTS_COLS_IN_CHAR)
        ]

        char_dot_row_col = min(
            all_char_dot_row_col_indices,
            key=lambda char_dot_row_col: math.dist(
                char_yx,
                _BC.CHAR_DOTS_COORDS[*char_dot_row_col],
            ),
        )

        dot_row_col_character_offset = np.array([
            char_row * _BC.DOTS_ROWS_IN_CHAR,
            char_col * _BC.DOTS_COLS_IN_CHAR,
        ])

        return tuple(char_dot_row_col + dot_row_col_character_offset)

    def _dot_row_col_to_yx_coords(self, dot_row_col: tuple[int, int]) -> tuple[int, int]:
        dot_row, dot_col = dot_row_col

        char_row, char_dot_row = divmod(dot_row, _BC.DOTS_ROWS_IN_CHAR)
        char_col, char_dot_col = divmod(dot_col, _BC.DOTS_COLS_IN_CHAR)

        char_dot_row_col = (char_dot_row, char_dot_col)

        canvas_char_y = char_row * _BC.CHAR_HEIGHT
        canvas_char_x = char_col * _BC.CHAR_WIDTH

        start_y, start_x = _BC.CANVAS_ZERO_YX_COORDS

        char_y = canvas_char_y - start_y
        char_x = canvas_char_x - start_x

        char_yx = (char_y, char_x)

        return tuple(char_yx + _BC.CHAR_DOTS_COORDS[*char_dot_row_col])


_BC = BrailleCanvas


def rotate_vector_clockwise(v: tuple[int, int], radians: float) -> tuple[int, int]:
    z = (v[1] + 1j * v[0]) * (1j**(4/(2*math.pi)*radians))

    return (z.imag, z.real)


def rotate_vector_counterclockwise(v: tuple[int, int], radians: float) -> tuple[int, int]:
    return rotate_vector_clockwise(v, -radians)
