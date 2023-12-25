"""
Day 11.2 - Cosmic Expansion

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
  You can model this by taking the rows and column with only
    empty space, and replacing them with 1 million (1'000'000) empty lines
  
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
EXPANSION_SIZE = 1_000_000 - 1
EMPTY = '.'
GALAXY = '#'
Pos2D = tuple[int, int]
Grid = list[str]

# Classes
...

# Funcs
def sliding_window(items: list[Pos2D]):
    for i in range(len(items)-1):
        yield (items[i], items[i+1])

def empty_spaces_between(a: int, b: int) -> int:
    delta = abs(b - a)
    dist = max(0, delta-1)
    return dist

def cosmic_expansion_1d(galaxies: list[Pos2D], index: int) -> list[Pos2D]:
    print("index = ", index)
    galaxies = sorted(galaxies, key=lambda g: g[index])
    print(galaxies)
    galaxies.insert(0, (0, 0))      # Insert a galaxy at the very beginning to make
                                    # our calculations easier
    n_empty_spots = 0
    output = []
    for a,b in sliding_window(galaxies):        # Only look at `b`
        n_empty_spots += empty_spaces_between(a[index], b[index])
        expansion_dist = n_empty_spots * EXPANSION_SIZE
        new_galaxy = tuple(                     # Add the expansion distance to the appropriate index
            n + (expansion_dist * (idx == index))
            for idx, n in enumerate(b)
        )
        output.append(new_galaxy)

    print("Out:", output)
    return output





def cosmic_expansion(galaxies: list[Pos2D]) -> list[Pos2D]:
    # Get by i-axis
    galaxies_expansion_i_axis = cosmic_expansion_1d(galaxies, index=0)
    # Get by j-axis
    return cosmic_expansion_1d(galaxies_expansion_i_axis, index=1)


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
    
    all_galaxies = get_all_galaxy_positions(grid)
    expanded_universe = cosmic_expansion(all_galaxies)

    total = sum(
        manhatten_distance(a, b)
        for a, b in combinations(expanded_universe, 2)
    )
    
    print("Sum of all galaxy pair distances:", total)

    

if __name__ == "__main__":
    main()
