import unittest

import math
import re
import string

from algutils import utils
from algutils.braille_canvas import BrailleCanvas


class BaseBrailleCanvasTestCase(unittest.TestCase):
    def assertCanvasesEqual(self, first, second, *args, **kwargs):
        first = str(first)
        second = str(second)

        first = utils.remove_trailing_whitespace(string=first)
        first = re.sub(pattern=r"^\n*", repl=r"", string=first, flags=re.MULTILINE)
        first = first.rstrip()

        second = utils.remove_trailing_whitespace(string=second)
        second = re.sub(pattern=r"^\n*", repl=r"", string=second, flags=re.MULTILINE)
        second = second.rstrip()

        got = first
        want = second

        try:
            super().assertEqual(first=first, second=second, *args, **kwargs)
        except AssertionError as e:
            e.add_note(
                f"""
assertCanvasesEqual(self, first=got, second=want, *args={args}, **kwargs={kwargs}):
+++ got == first
{got}
--- want == second
{want}
___
                """.rstrip()
            )

            raise


class TestBrailleCanvas(BaseBrailleCanvasTestCase):
    def test_braille_canvas(self) -> None:
        scale = 100
        bc = BrailleCanvas(
            char_rows=2 + int(scale / 4.4),
            char_columns=2 + scale // 2,
        )
        polygon_sides = 7
        rotation = math.pi * 0.3124  # Random number
        vertices = [
            [
                (z.real + 1) * scale / 2,
                (z.imag + 1) * scale / 2,
            ]
            for z in (
                1 * 1j ** (rotation + 4 / polygon_sides * i)
                for i in range(polygon_sides)
            )
        ]
        for i, vertex in enumerate(vertices):
            bc.write_text(vertex, string.ascii_uppercase[i])
        for ui, u in enumerate(vertices):
            for v in vertices[ui + 1 :]:
                bc.draw_line(u, v, offset=6.0)
        self.assertCanvasesEqual(
            str(bc).rstrip(),
            r"""
                    C  ⣀⣀⡀
                ⣀⠔⢁⠄⡀⢀⠐⠢⡀⠈⠉⠉⠒⠢⠤⣀⣀⡀
             ⣀⠔⠉ ⢀⠇ ⡇ ⢣ ⠈⠑⢄⡀     ⠈⠉⠉⠑⠒⠤  B
          ⢀⠔⠉   ⡠⠃  ⡇  ⠣⡀  ⠈⠢⣀⣀⣀⣀⡠⠤⠔⠒⠊⢉⡀
       ⢀⠔⠊⠁    ⡰⠁ ⢀⣀⣇⣀⠤⠤⢳⠒⠉⠉⠉⠉⠑⢄⡀  ⢀⡠⠊⠁⡰⠁⡇⠘⡄
     ⠠⠊⢁⣀⣀⣀⠤⠤⠒⡲⠉⠉⠉⠁ ⡇    ⢣      ⢈⡢⣊⠁  ⡜  ⡇ ⠘⡄
   D  ⣉⣁⡀    ⡜      ⡇     ⢇  ⢀⡠⠊⠁  ⠉⢢⡎   ⡇  ⠑⡄
   ⡀⢄⠑⢄ ⠈⠉⠉⠑⡞⠤⢄⣀⣀   ⡇     ⢀⣧⠊⠁     ⢀⠎⠈⠑⢄⡀⡇   ⠘⡄
   ⡇ ⢇ ⠉⠢⣀⢀⠎     ⠉⠉⢉⠗⠢⢄⣀⣠⡊⠁ ⢣     ⢀⠇    ⠈⡧⣀   ⠘⡄
  ⢰⠁  ⢇  ⢀⠏⠢⡀      ⢸ ⣀⠔⠉ ⠈⠉⠉⠑⢧⠤⢄⣀⣠⠃      ⡇ ⠑⢄⡀ ⠑⡄
  ⢸    ⢇⡠⠃  ⠈⠒⢄   ⣀⢼⠉         ⢇ ⡰⠁⠉⠉⠉⠒⠢⢄⣀⣇⡀  ⠈⠢⣀⠑⡄
  ⢸    ⡨⢇      ⣉⠶⡉ ⢸           ⣿        ⢰⠁⠈⠉⠉⠑⠢⠄⠁ A
  ⢸   ⡰⠁ ⢇  ⣀⠔⠉  ⠈⠑⢼          ⡜ ⢇     ⢀⣀⣸⣀⡠⠤⠔⠒⠉⢁
  ⢸  ⡜   ⣈⢖⠉       ⢸⠉⠢⣀    ⢀⣀⣎⣀⡠⠤⢗⠒⠉⠉⠉⠁ ⢸   ⢀⡠⠊⠁⡔⠁
  ⢸⢀⠎ ⢀⠔⠉ ⠈⢆    ⢀⣀⣀⣸⠤⠤⠒⠓⢍⡉⠉⢁⠎     ⢇     ⢸⢀⡠⠊⠁ ⢀⠎
   ⠈⠐⣊⣁⣀⣀⠤⠤⠚⡖⠉⠉⠉⠁  ⡎     ⠈⢒⢇       ⢇  ⢀⡠⢺⠁   ⢀⠎
  E  ⠤⣀⣀⣀   ⠈⡆     ⡇     ⡠⠃ ⠉⠢⡀    ⢀⣧⠊⠁ ⢸   ⢀⠇
    ⠈⠢⣀  ⠉⠉⠉⠒⠬⢆⣀⣀⡀ ⡇    ⡰⠁    ⠈⠑⢄⡠⠊⠁ ⢇  ⡸  ⡠⠃
       ⠉⠢⡀    ⠈⡆ ⠈⠉⡏⠒⠢⠤⣰⣁⣀    ⡠⠒⠉⠉⠢⣀  ⢇ ⡇ ⡰⠁
         ⠈⠑⢄   ⠈⡆  ⡇  ⡜   ⠉⣉⠕⠛⠤⢄⣀⣀⡀ ⠑⢄⡈⠂⠃⠘
            ⠉⠢⡀ ⠈⡆ ⡇⢀⠎  ⣀⠔⠉       ⠈⠉⠉⡂  G
              ⠈⠑⢄⠘ ⠁⠊⣀⠔⠉ ⢀⣀⣀⣀⡠⠤⠔⠒⠊⠉⠉⠉
                   F  ⠊⠉⠉⠁
            """,
        )
