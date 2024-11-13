"""
Day 13.1 - Point of Incidence

Python 3.9+

Input:
  A series of 2D grids, containing

Logic:
...

Output:
...
"""

from pathlib import Path


p = Path(__file__).with_name("input")

# Vars
VERTICAL = "VERTICAL"
HORIZONTAL = "HORIZONTAL"

Grid = list[str]

# Classes
...

# Funcs
def rotate(grid: Grid) -> Grid:
    """
    Rotates the given grid
    """
    return list(zip(*grid))

def find_reflection(grid: Grid) -> int | None:
    reflection_index = None
    for i in range(len(grid) - 1):  # minus-one because otherwise our 
        current = grid[i]
        next = grid[i+1]
        if current == next:
            if is_reflection(grid, i):
                assert reflection_index is None, "There should be only one valid reflection"
                reflection_index = i
    
    return reflection_index

def is_reflection(grid: Grid, index: int) -> bool:
    # Iterate forwards and backwards from the split
    back_of_grid = range(index, -1, -1)
    front_of_grid = range(index+1, len(grid), 1)
    assert len(back_of_grid) > 0 and len(front_of_grid) > 0, \
                "You can't reflect if one side is empty"
    return all(grid[i] == grid[j] for i, j in zip(back_of_grid, front_of_grid))

def calculate_output(index: int, axis: str) -> int:
    if axis == VERTICAL:
        return index + 1
    elif axis == HORIZONTAL:
        return 100 * (index + 1)
    else:
        raise Exception("Unknown axis value:", axis)


# =====

def main():
    with p.open('r') as file:
        all_grids = [grid.split() for grid in file.read().split("\n\n")]
    
    total = 0
    for grid in all_grids:
        axis = HORIZONTAL
        idx = find_reflection(grid)
        if idx is None:
            axis = VERTICAL
            idx = find_reflection(rotate(grid))
        if idx is None:
            raise LookupError("Couldn't find reflection point of grid", grid)
        output = calculate_output(idx, axis)
        print(idx + 1, axis, "=", output)
        total += output

    print("Total:", total)


if __name__ == "__main__":
    main()
