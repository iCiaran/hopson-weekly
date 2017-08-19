Maze generator and solver using image masks.

Generation modes:

0 - Random maze
1 - Maze with image mask
2 - Modulus maze

Inspired by [https://medium.com/@G3Kappa/generating-mazes-from-pictures-or-masking-entropy-4d050d148539](this) article.

Album of demo outputs [https://imgur.com/a/lHqFq](here).


Config options:

width = maze width in cells
height = maze height in cells
border = border around maze in pixels
length = length of gap between walls in pixels
difficulty = difficulty of maze (1-100)
solve = Only generate maze - 0, Generate and solve - 1
gen = Generation mode used
mask = filename of image mask
background = background colour
wall = wall colour
path = path colour
