"""
Given a list of lines from a -> b, in how many places
do the lines overlap?

All lines are perfectly vertical, horizontal, or diagonal,
so I'm representing it as a grid of numbers. For each point
that the line passes over, increment by 1. Then count every
point that's greater than 1.

We now consider diagonals which is ez because I already built it
to consider them
"""


from pathlib import Path
from itertools import repeat

p = Path(__file__).with_name("input")


def inclusive_range(a, b) -> range:
    """
    Returns a range object from a -> b, b inclusive, even
    if you need to count backwards.
    e.g. (1, 4) -> 1,2,3,4;
    (4,0) -> 4,3,2,1,0
    """
    if a <= b:
        return range(a, b+1)
    else:
        return range(a, b-1, -1)


# Vars
lines = []
max_x = 0
max_y = 0


with p.open('r') as file:
    for line in file:
        lhs, rhs = line.split(' -> ')
        # Convert to ints
        x1, y1 = map(int, lhs.split(','))
        x2, y2 = map(int, rhs.split(','))
        # Learn the max x-y range to build the
        # grid size from
        max_x = max(x1, x2, max_x)
        max_y = max(y1, y2, max_y)
        lines.append((x1, x2, y1, y2))

grid = [[0 for _ in range(max_x+1)] for _ in range(max_y+1)]
n_overlaps = 0

for (x1, x2, y1, y2) in lines:
    # Turn into iterators
    # Account for vertical/horzontal lines, where nums on that axis won't change
    length = max(abs(x1-x2), abs(y1-y2)) + 1
    x_iter = inclusive_range(x1, x2) if x1 != x2 else repeat(x1, times=length)
    y_iter = inclusive_range(y1, y2) if y1 != y2 else repeat(y1, times=length)
    for x, y in zip(x_iter, y_iter):
        grid[y][x] += 1
        if grid[y][x] == 2:
            n_overlaps += 1

# for row in grid:
#     print(''.join(str(n) if n > 0 else '.' for n in row))
print(n_overlaps)
