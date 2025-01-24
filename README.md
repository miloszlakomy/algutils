# algutils

# Run all unit tests
```
cd ~/github.com/miloszlakomy/algutils/
PYTHONPATH=.. python3 -m unittest discover
```

# Braille Canvas
```Python
$ PYTHONPATH=~/github.com/miloszlakomy/ ipython3
Python 3.13.0 (v3.13.0:60403a5409f, Oct  7 2024, 00:37:40) [Clang 15.0.0 (clang-1500.3.9.4)]
Type 'copyright', 'credits' or 'license' for more information
IPython 8.30.0 -- An enhanced Interactive Python. Type '?' for help.

In [1]: import random, string, typing; from random import randint; import numpy as np; from algutils.utils import *; from algutils.np_array_to_braille import np_array_to_braille; from algutils.braille_canvas import BrailleCanvas; scale=100; bc = BrailleCanvas(char_rows=2 + int(scale/4.4), char_columns=2 + scale//2); polygon_sides = 7; rotation = random.uniform(0, 2*math.pi); vertices = [[(z.real+1)*scale/2, (z.imag+1)*scale/2] for z in (1 * 1j**(rotation+4/polygon_sides*i) for i in range(polygon_sides))]; [bc.write_text(vertex, string.ascii_uppercase[i]) for i, vertex in enumerate(vertices)]; [bc.draw_line(u, v, offset=6.0) for ui, u in enumerate(vertices) for v in vertices[ui + 1 :]]; print(bc)
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡀⠀⠀C⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡠⠔⠒⠉⠁⢀⠎⢀⠄⡄⢰⠉⠉⠢⣀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⣀⡠⠔⠊⠉⠁⠀⠀⠀⠀⡠⠊⠁⠀⡇⠀⢱⠀⠑⡄⠀⠀⠉⠑⢄⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀D⠀⠀⣉⣁⣀⣀⣀⡀⠀⠀⠀⠀⡠⠊⠀⠀⠀⡜⠀⠀⢸⠀⠀⠈⢆⠀⠀⠀⠀⠈⠉⠢⣀⡀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⢀⢀⠀⡀⠢⢄⡀⠀⠀⠈⠉⠉⡩⠋⠉⠉⠑⠒⡲⠓⠤⠤⠤⣇⣀⣀⣀⣱⣀⣀⡀⠀⠀⠀⠀⠈⠑⢄⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⢀⠇⠀⡇⠈⢆⠀⠈⠑⠢⣀⠔⠉⠀⠀⠀⠀⠀⢀⠇⠀⠀⠀⠀⡇⠀⠀⠀⠀⠈⢆⠈⠉⠉⠉⠉⠉⠉⢂⠀⠀B⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⡇⠀⠀⡇⠀⠀⠱⡀⢀⠔⠁⠉⠑⢄⡀⠀⠀⠀⡇⠀⠀⠀⠀⠀⢸⠀⠀⠀⠀⠀⠀⠣⣀⣀⡠⠔⠊⠉⢁⠆⡀⢀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⡸⠀⠀⠀⢱⠀⠀⢀⠜⢅⠀⠀⠀⠀⠀⠈⠑⠢⣜⡀⠀⠀⠀⠀⠀⠸⡀⣀⣀⡠⠒⠊⠉⠑⡄⠀⠀⡠⠊⠁⢠⠃⠘⡄⠀⠀⠀⠀
⠀⠀⠀⡰⠁⠀⠀⠀⢸⡠⠊⠁⠀⠀⠣⡀⠀⠀⠀⠀⠀⡰⠁⠈⠑⣄⣀⠤⠒⠉⡏⠀⠀⠀⠀⠀⠀⠀⠈⣢⠊⠀⠀⢀⠇⠀⠀⡇⠀⠀⠀⠀
⠀⠀⢀⠇⠀⠀⠀⡠⠊⡇⠀⠀⠀⠀⠀⠑⡄⠀⠀⣀⣠⠧⠒⠉⠉⠀⠈⠉⠢⢄⡇⠀⠀⠀⠀⠀⠀⡠⠊⠀⠱⡀⠀⡎⠀⠀⠀⢇⠀⠀⠀⠀
⠀⠀⡇⠀⠀⡠⠊⠀⠀⡇⠀⠀⢀⣀⡠⠤⠊⢏⠉⠀⡇⠀⠀⠀⠀⠀⠀⠀⠀⠀⢸⠑⢄⣀⢀⠔⠉⠀⠀⠀⠀⠈⣞⠀⠀⠀⠀⢸⠀⠀⠀⠀
⠀⠜⢀⠔⠉⠀⢀⣀⡠⢼⠊⠉⠁⠀⠀⠀⠀⠀⠱⡜⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠸⡀⢀⠔⠉⠢⢄⡀⠀⠀⠀⢠⠃⠣⡀⠀⠀⠈⡆⠀⠀⠀
E⠀⠀⠒⠊⠉⠁⠀⠀⠸⡀⠀⠀⠀⠀⠀⠀⠀⡰⠙⢄⠀⠀⠀⠀⠀⠀⠀⠀⠀⢀⡏⠁⠀⠀⠀⠀⠈⠑⠢⣀⠇⠀⠀⠈⡆⠀⠀⡇⠀⠀⠀
⠀⠀⠀⢍⠉⠉⠉⠉⠑⠒⡗⠒⠤⠤⠤⢄⣀⣠⣃⣀⣀⣇⡀⠀⠀⠀⠀⠀⡠⠊⠁⢇⠀⠀⠀⠀⠀⠀⠀⠀⡎⠉⠑⢄⡀⠈⢢⠀⢣⠀⠀⠀
⠀⠀⠱⡀⠉⠑⢄⣀⠀⠀⡇⠀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⠙⡍⠉⠉⡩⠋⠉⠒⠒⢺⠒⠤⠤⠤⢄⣀⣀⣜⣀⣀⣀⡀⠈⠑⠄⠁⠀⠀⠀⠀
⠀⠀⠀⠈⢆⠀⠀⠀⠉⠢⣸⡀⠀⠀⠀⠀⡜⠀⠀⠀⠀⠀⠀⠈⣦⠊⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⠀⠀⢰⠁⠀⠀⠀⠈⢉⣉⡁⠀⠀A⠀⠀
⠀⠀⠀⠀⠀⠣⡀⠀⠀⠀⠘⡌⠑⢄⣀⡸⠀⠀⠀⠀⠀⢀⠔⠉⠀⠱⡀⠀⠀⠀⠀⠀⡇⠀⠀⠀⠀⢀⢇⣀⡠⠔⠊⠉⠁⢀⠎⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠘⡄⠀⠀⠀⡇⠀⠀⢠⠋⠢⣀⡀⢀⠔⠁⠀⠀⠀⠀⠘⢄⠀⠀⠀⠀⢇⣀⡠⠔⠊⡏⠁⠀⠀⠀⠀⡠⠊⠁⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠈⢆⠀⠀⢇⠀⠀⡇⠀⠀⣀⠎⠑⢄⣀⠀⠀⠀⠀⣀⣀⡣⡔⠊⠉⢹⠀⠀⠀⡜⠀⠀⠀⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠱⡀⢸⠀⡜⠀⡠⠊⠀⠀⠀⣀⣀⠭⠲⣊⡉⠀⠀⠀⠑⡄⠀⠀⡇⠀⢰⠁⠀⠀⡠⠊⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠀⠀⠀⠉⣀⠤⠒⠉⠉⠀⠀⠀⠀⠀⠈⠑⠤⣀⠀⠈⢆⠀⡇⢀⠇⢀⠔⠉⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀F⠀⠀⠒⠒⠤⠤⠤⢄⣀⣀⣀⣀⣀⣀⡀⠀⠉⠢⠄⠁⠀⠈⠐⠁⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠈⠉⠉⠉⠀⠀G⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀⠀
```
