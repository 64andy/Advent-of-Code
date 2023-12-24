"""
Day 10.2 - Pipe Maze

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

We also consider some tiles to be inside the loop.
  A tile is inside the loop if:
  - It's a ground tile
  - It can't be reached from outside the loop (We can snake in-between touching tiles)
  Example:
    ..........
    .S------7.      # Here, the 'I' tiles are inside the loop, and
    .|F----7|.      # the 'O' and '.' tiles are outside of it.
    .||OOOO||.      # This is because you could snake in-between the pipes
    .|L-7F-J|.      # at the bottom in the middle, even though they're touching.
    .|II||II|.
    .L--JL--J.
    ..........
  
Output:
  How many tiles are inside the loop?
"""

import dataclasses
from collections import deque
from pathlib import Path
from typing import Optional

p = Path(__file__).with_name("input")

# Vars
STARTING_CHAR = 'S'
# Coloured rendering
ANSI_GREEN = '\033[92m'
ANSI_RESET = '\033[0m'

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

    def fix_starting_pos(self):
        """
        The starting position is duplicated, and represented by a placeholder "S".

        This replaces it with an appropriate pipe
        """
        del self.path[0]    # Delete the duplicate staring position
        starting_pos, char = self.path.pop()
        assert char == STARTING_CHAR, "The format changed, something's wrong..."

        in_direction = self.current_direction   # Direction entering the start
        after_start = self.path[0][0]
        (i1, j1) = starting_pos
        (i2, j2) = after_start
        out_direction = (i2-i1, j2-j1)

        # Check every pipe to see which one maps in_direction -> out_direction 
        pipe = None
        for char, mapping in PIPE_DIRECTION_MAPPING.items():
            if in_direction in mapping and mapping[in_direction] == out_direction:
                pipe = char
                break
        assert pipe is not None, "Failed to fix the starting position"
        # Add the fixed pipe
        self.path.append((starting_pos, pipe))

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
            route.fix_starting_pos()
            return True
        valid_next_step = route.to_next_position(grid)
        if not valid_next_step: # dead ends are dropped
            return False

def render_loop_and_count_internal_tiles(route: Route) -> int:
    """
    This is a two-fold function.
    It renders the shape of the loop, and counts all of its internal tiles
    """
    EMPTY = '█'
    CORNER_TO_SLANT = {
        'F': '╱',
        'J': '╱',
        '7': '╲',
        'L': '╲',
    }
    RENDERED_CHAR = {
        'F':'┌',
        'J':'┘',
        '7':'┐',
        'L':'└',
        '|':'│',
        '-':'─',
        EMPTY: EMPTY,
        "internal": ANSI_GREEN+EMPTY+ANSI_RESET,
        'S': 'S'    # Shouldn't be reachable, but for testing...
    }

    path = route.path
    n_internal_tiles = 0
    # We record the loop's dimensions, so we don't have to consider
    # as many tiles beyond the loop
    top_most = max(t[0][0] for t in path)
    bottom_most = min(t[0][0] for t in path)
    left_most = min(t[0][1] for t in path)
    right_most = max(t[0][1] for t in path)
    # Record each pipe's position
    pos_to_char = {pos: char
                   for pos, char in path}
    
    # To count this, we use the even-odd rule algorithm.
    # Horizontally, if you've crossed an odd number of lines
    #   to get to your current spot, you're inside the loop.
    # https://en.wikipedia.org/wiki/Point_in_polygon
    # https://en.wikipedia.org/wiki/Even%E2%80%93odd_rule
    #
    # !!! HOWEVER !!!
    # Even-odd struggles to handle lines perpendicular to the original cast.
    # Because we're on a grid, the hard 90deg turns (which are 50% horizontal by weight)
    #   cause problems.
    # To handle this, we reduce turn pipes into diagonals.
    #   (F and J => ┌ and ┘ => ╱ and ╱)
    #   (7 and F => ┐ and └ => ╲ and ╲)
    # The logic:
    #   If we come across a slant, we act as if we crossed a line.
    #   If we come across another slant:
    #     If the slant's the same, it's part of the same line
    #     If the slant's different, we crossed a new line
    #     In either case, we forget the last slant
    #
    # For example: F-7 => ┌─┐ => /-\ => /\ => Two lines
    #              F-J => ┌─┘ => /-/ => /  => One continous upward slant line
    for i in range(bottom_most, top_most+1):
        n_crossed_lines = 0
        current_slant = None
        for j in range(left_most, right_most+1):
            # Logic
            current_pipe = pos_to_char.get((i,j), EMPTY)
            # We don't consider horizontal pipes, because we haven't crossed any lines.
            if current_pipe == '-':
                pass
            # Vertical pipes are an easy "yes"
            elif current_pipe == '|':
                n_crossed_lines += 1
            # Turn pieces are more complex
            elif current_pipe in CORNER_TO_SLANT:
                slant = CORNER_TO_SLANT[current_pipe]
                if current_slant is None:
                    n_crossed_lines += 1
                    current_slant = slant
                else:
                    if slant == current_slant:  # One continous line, do nothing
                        pass
                    else:                       # Two crossed lines
                        n_crossed_lines += 1
                    current_slant = None 

            elif current_pipe == EMPTY and n_crossed_lines%2 == 1:
                current_pipe = 'internal'
                n_internal_tiles += 1
            
            # Rendering
            rendered_char = RENDERED_CHAR[current_pipe]
            print(rendered_char, end='')
        print()
    
    return n_internal_tiles


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
            n_internal_tiles = render_loop_and_count_internal_tiles(path)
            print("Took", len(path.path), "steps")
            print("Number of internal tiles:", n_internal_tiles)
            break
        else:
            print("Couldn't continue path:", path)
            print("---")


if __name__ == "__main__":
    main()
