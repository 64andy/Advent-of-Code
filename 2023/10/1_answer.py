"""
Day 10.1 - Pipe Maze

Python 3.9+

Input:
  A grid of "pipes"; characters that represent bends and lines
    - is a horizontal pipe connecting east and west.
    | is a vertical pipe connecting north and south.
    L is a 90-degree bend connecting north and east.
    J is a 90-degree bend connecting north and west.
    7 is a 90-degree bend connecting south and west.
    F is a 90-degree bend connecting south and east.
    . is ground; there is no pipe in this tile.
    S is the starting position of the animal;
      there is a pipe on this tile, but your sketch doesn't
      show what shape the pipe has.


Logic:
  In this grid there is one large continuous loop.
  Example (without the starting position showing):
    .....
    .F-7. 
    .|.|.
    .L-J.
    .....
  The 'S' starting position is part of this loop, and should
    be considered a pipe of unknown shape.
    
  
Output:
  How many steps along the loop does it take to get
    from the starting position to the point
    farthest from the starting position?
  
  (Hint: This isn't a euclid/manhatten distance check.
    If the loop is 20 tiles long, then the furthest you
    can walk is simply 10 tiles away)
"""

import dataclasses
from collections import deque
from pathlib import Path
from typing import Optional

p = Path(__file__).with_name("input")

# Vars
STARTING_CHAR = 'S'

## Maps input directions to output directions
Grid = list[str]

Pos2D = tuple[int, int]
NORTH: Pos2D    = (-1,0)
SOUTH: Pos2D    = (1, 0)
EAST: Pos2D     = (0, 1)
WEST: Pos2D     = (0,-1)

PIPE_DIRECTION_MAPPING: dict[str, dict[Pos2D, Pos2D]] = {
    '|': {  # │ Vertical pipe: North and South
        NORTH: NORTH,       # Come in facing north, you'll come out facing north
        SOUTH: SOUTH
    },
    '-': {  # ─ Horizontal pipe: East and West
        EAST: EAST,         # Come in facing east, you'll come out facing east 
        WEST: WEST,
    },
    'L': {  # └ 90-degree bend: North and East
        SOUTH: EAST,        # Come in facing south, you'll come out facing east
        WEST: NORTH
    },
    'J': {  # ┘ 90-degree bend: North and West
        SOUTH: WEST,
        EAST: NORTH
    },
    '7': {  # ┐ 90-degree bend: South and West
        NORTH: WEST,
        EAST: SOUTH
    },
    'F': {  # ┌ 90-degree bend: South and East
        NORTH: EAST,
        WEST: SOUTH
    },
    '.': {  # Ground: not a pipe
    },
    'S': {  # Once you reach 'S', immediately stop.
            # These values are only here so it doesn't think the loop's broken
        WEST: WEST,
        EAST: EAST,
        NORTH: NORTH,
        SOUTH: SOUTH,
    }
}


# Classes
@dataclasses.dataclass
class Route:
    path: list[tuple[Pos2D, str]]
    current_direction: Pos2D

    @staticmethod
    def create_starting_positions(pos: Pos2D) -> 'deque[Route]':
        return deque(Route([(pos, STARTING_CHAR)], direction)
                for direction in (NORTH, SOUTH, WEST, EAST))

    @property
    def head(self) -> tuple[Pos2D, str]:
        return self.path[-1]
    
    def to_next_position(self, grid: Grid) -> bool:
        """
        Moves to the current position along the grid, mutating Route in-place.

        Returns true if there is a valid next pipe
        """
        new_i = self.head[0][0] + self.current_direction[0]
        new_j = self.head[0][1] + self.current_direction[1]
        # Bounds check: Ensure we're not lead out of bounds
        if not( 0 <= new_i < len(grid) and 0 <= new_j < len(grid[new_i]) ):
            print(f"Reason: {(new_i, new_j)} is out of bounds")
            return False
        next_pipe = grid[new_i][new_j]

        # Check if you can reach the pipe from your current direction
        new_direction = PIPE_DIRECTION_MAPPING[next_pipe].get(self.current_direction)
        if new_direction is None:
            print(f"Reason: Can't enter {next_pipe!r} from {self.current_direction}")
            return False
        
        self.current_direction = new_direction
        self.path.append(((new_i, new_j), next_pipe))
        return True
    
    def at_terminal(self) -> bool:
        return len(self.path) > 1 and self.head[1] == STARTING_CHAR


# Funcs
def find_starting_point(grid: Grid, needle: str) -> Optional[Pos2D]:
    for i, line in enumerate(grid):
        for j, char in enumerate(line):
            if char == needle:
                return (i, j)

def run_through_path(route: Route, grid: Grid) -> bool:
    """
    Follows the pipes from the starting route, updating it in-place.

    Returns true if it successfully returned to starting_point
    """
    while True:
        if route.at_terminal():
            return True
        valid_next_step = route.to_next_position(grid)
        if not valid_next_step: # dead ends are dropped
            return False

def render_loop(route: Route):
    path = route.path
    # We record the loop's dimensions, so we don't have to consider
    # as many tiles beyond the loop
    top_most = min(t[0][0] for t in path)
    bottom_most = max(t[0][0] for t in path)
    left_most = min(t[0][1] for t in path)
    right_most = max(t[0][1] for t in path)
    pos_to_char = {pos: char
                   for pos, char in path}
    
    for i in range(top_most, bottom_most+1):
        for j in range(left_most, right_most+1):
            print(pos_to_char.get((i,j), '.'), end='')
        print() 


# =====

def main():
    with p.open('r') as file:
        grid: Grid = [line.strip() for line in file]
    starting_point = find_starting_point(grid, STARTING_CHAR)
    assert starting_point is not None, f"Character {STARTING_CHAR!r} not in grid"
    print("Starting point:", starting_point)
    print("\n===\n")

    paths = Route.create_starting_positions(starting_point)

    for path in paths:
        if run_through_path(path, grid):
            render_loop(path)
            print("Took", len(path.path), "steps")
            print("Furthest point is:", len(path.path) // 2, "steps away")
            break
        else:
            print("Couldn't continue path:", path)
            print("---")


if __name__ == "__main__":
    main()
