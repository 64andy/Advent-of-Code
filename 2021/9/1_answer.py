"""
Day 9 - Given a grid of nums, find the 'low points',
as in spots smaller than its direct NESW neighbours.
Out-of-bounds neighbours are ignored, print the sum of all
'low points' values + the number of low points
"""

from pathlib import Path
p = Path(__file__).with_name("input")


def neighbours(grid, i, j):
    """
    Generator.
    Returns the values above, below, left, and right of
    the given position, if it's in range
    """
    COORDS = ((-1, 0), (0, 1), (1, 0), (0, -1))
    for di, dj in COORDS:
        ni = i + di
        nj = j + dj
        if 0 <= ni < len(grid) and 0 <= nj < len(grid[ni]):
            yield grid[ni][nj]

# Vars
...

def main():
    with p.open('r') as file:
        grid = [[int(i) for i in line.strip()]
                for line in file
                if line.strip()
        ]
    
    total = 0
    n_lows = 0
    for i, line in enumerate(grid):
        for j, val in enumerate(line):
            if all(n > val for n in neighbours(grid, i, j)):
                print(f"{i=}, {j=}, {val=}")
                total += val
                n_lows += 1
    print(f"{total+n_lows=}")


if __name__ == "__main__":
    main()

