"""
Day 11.1 - Cosmic Expansion

Python 3.9+

Input:
  A universe grid, consisting of empty spaces (dots)
    and galaxies (hash/poundtags)
  Example:
    ..#
    ...
    #..

Logic:
  The input is not the true state of the universe,
    because *the universe has expanded*.
  You can model this by doubling the rows and column with only
    empty space
  Example:
    ..#
    ... < Empty row
    #..
     ^ Empty column
    
    Repeat the empty rows
    ..#
    ...  < Doubled up
    ...  < Doubled up
    #..

    Then repeat the empty columns
    ...#
    ....
    ....
    #...
     ^^ Doubled up
  
  After this, we also need the distances between each
    pair of galaxies.
  The distance is the shortest path using only up, down, left, right moves.
  
Output:
  Print the sum of each galaxy pair's distance
"""

from itertools import combinations
from pathlib import Path


p = Path(__file__).with_name("input")

# Vars
EMPTY = '.'
GALAXY = '#'
Pos2D = tuple[int, int]
Grid = list[str]

# Classes
...

# Funcs
def rotate_grid(grid: Grid) -> Grid:
    return [''.join(column) for column in zip(*grid)]

def cosmic_expansion_1d(grid: Grid) -> Grid:
    """
    Expands the universe across a single axis.
    Don't forget to rotate and call me again :)
    """
    output = []
    for line in grid:
        output.append(line)
        if all(char == EMPTY for char in line):
            output.append(line)
    return output

def cosmic_expansion(grid: Grid) -> Grid:
    """
    Returns the input grid after "cosmic expansion".
    i.e. any repeated rows & columns are repeated
    """
    output = cosmic_expansion_1d(grid)
    # rotate
    output = rotate_grid(output)
    output = cosmic_expansion_1d(output)
    # rotate back
    return rotate_grid(output)

def get_all_galaxy_positions(universe: Grid, needle: str = GALAXY) -> list[Pos2D]:
    """
    Returns the (i,j) positions of all galaxies in the given universe
    """
    galaxy_positions = []
    for i, row in enumerate(universe):
        for j, char in enumerate(row):
            if char == needle:
                galaxy_positions.append((i, j))
    
    return galaxy_positions

def manhatten_distance(start: Pos2D, end: Pos2D) -> int:
    """
    I really like the term "Manhatten Distance".
    Anyway uhhhh returns the distance as if you had to
      traverse a grid
    """
    i_dist = abs(start[0] - end[0])
    j_dist = abs(start[1] - end[1])
    return i_dist + j_dist

# =====

def main():
    with p.open('r') as file:
        grid = [line.strip() for line in file]
    
    expanded_universe = cosmic_expansion(grid)
    all_galaxies = get_all_galaxy_positions(expanded_universe)

    total = sum(
        manhatten_distance(a, b)
        for a, b in combinations(all_galaxies, 2)
    )
    
    print("Sum of all galaxy pair distances:", total)

    

if __name__ == "__main__":
    main()
