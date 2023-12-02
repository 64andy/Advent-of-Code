"""
Day 8.1 - Treetop Tree House

Input:
A 2D grid of digits between 0-9

Logic:
Each digit represents the height that tree.
We want to know if a tree is "visible" from outside the grid.
- That is, all the numbers either above, below, left, or right of it are SMALLER than itself
Note: This means all the edge trees are visible from outside

Output:
How many trees are visible from the outside?
"""

from pathlib import Path
from typing import List
p = Path(__file__).with_name("input")

# Vars

DIRECTION = {
    'up': (-1, 0),
    'down': (1, 0),
    'left': (0, -1),
    'right': (0, 1),
}


class VisibleTree:
    def __init__(self, height: str):
        self.height = int(height)
        # Some trees have a height of 0, and they should still be visible from outside the tree if on the edge
        self.max_direction = {
            'up': -1,
            'down': -1,
            'left': -1,
            'right': -1,
        }

    def is_visible(self) -> bool:
        """
        A tree is 'visible' if it can be viewed from outside the grid.

        This means that from at least one direction (N,E,S,W), all the trees are shorter than itself.
        """
        return any(direction < self.height
                   for direction in self.max_direction.values()
                   )

    def __repr__(self):
        return f"T(height={self.height}, {', '.join(f'{a[0]}={b}' for a,b in self.max_direction.items())})"


# Funcs
def process_grid(grid: List[List[VisibleTree]]) -> None:
    """
    Processes the grid in-place, so every tree's largest neighbour is set.

    Logic: You ask your neighbours what the biggest tree on their side is. This height is either
    """
    # Pass #1, check the top and left.
    # We update as we go, each tree's maximum from a direction is
    # based on a previously processed tree's maximum.
    # Therefore, we can't use down & right, as we read top-left to bottom-right,
    # and we haven't read them yet.
    for (i, row) in enumerate(grid):
        for (j, tree) in enumerate(row):
            for direction in ("up", "left"):
                (di, dj) = DIRECTION[direction]
                ni = i+di
                nj = j+dj
                if (0 <= ni < len(grid)) and (0 <= nj < len(row)):
                    # The tallest tree in any direction is either your neighbour, or their tallest tree in a direction
                    other_tree = grid[ni][nj]
                    tree.max_direction[direction] = max(
                        other_tree.max_direction[direction], other_tree.height)
    
    # Pass #2, check the bottom and right.
    # This time around, we iterate backwards (bottom-right to top-left)
    for (i, row) in reversed(list(enumerate(grid))):
        for (j, tree) in reversed(list(enumerate(row))):
            for direction in ("down", "right"):
                (di, dj) = DIRECTION[direction]
                ni = i+di
                nj = j+dj
                if (0 <= ni < len(grid)) and (0 <= nj < len(row)):
                    # The tallest tree in any direction is either your neighbour, or their tallest tree in a direction
                    other_tree = grid[ni][nj]
                    tree.max_direction[direction] = max(
                        other_tree.max_direction[direction], other_tree.height)

def main():
    with p.open('r') as file:
        grid = [[VisibleTree(height) for height in line.strip()]
                for line in file]
    
    process_grid(grid)

    n_visible = sum(tree.is_visible() for row in grid for tree in row)
    print("n_visible:", n_visible)


if __name__ == "__main__":
    main()
