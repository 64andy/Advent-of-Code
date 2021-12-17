"""
Day 15.2: Chiton

Path-finding problem. We are given a grid of numbers (costs).
The total cost is the sum of each node entered (ignore start).
We start from the top-left, and end at the top right.

Part 2 new rule: The provided grid is just one part of
a 5x5 grid. The remaining x24 are a repeat, except with
one higher value than the grid left/above it. Any overflowing
digits wrap back to 1.

Part 2 question: What's the shortest path?

Achieving this with the LCFS frontier I learned 4 months ago, it takes around 14s
"""

from pathlib import Path
from dataclasses import dataclass, field
from heapq import heappop, heappush
from itertools import product
from time import perf_counter
p = Path(__file__).with_name("input")


@dataclass(order=True)
class WeightedPath:
    cost: int
    path: tuple = field(compare=False)

    def __iter__(self):
        return iter((self.cost, self.path))


class LCFSFrontier:
    def __init__(self, pruning: bool = True):
        self.paths = []
        self.pruning = pruning
        self.discard = set()

    def __iter__(self):
        return self

    def add(self, path: WeightedPath) -> None:
        head = path.path[-1]
        # Prune so we don't double-back
        if self.pruning and head in self.discard:
            return
        heappush(self.paths, path)

    def __next__(self) -> WeightedPath:
        if len(self.paths) == 0:
            raise StopIteration
        path = heappop(self.paths)
        head = path.path[-1]
        if self.pruning:
            if head not in self.discard:
                self.discard.add(head)
            else:
                return next(self)
        return path


def neighbours(grid, path: WeightedPath):
    """
    Generator.
    Returns the WeightedPaths of the neighbours
    """
    cost, old_path = path
    head = old_path[-1]
    i, j = head
    COORDS = ((-1, 0), (0, 1), (1, 0), (0, -1))
    for di, dj in COORDS:
        ni = i + di
        nj = j + dj
        if 0 <= ni < len(grid) and 0 <= nj < len(grid[ni]):
            new_cost = cost + grid[ni][nj]
            yield WeightedPath(cost=new_cost,
                               path=old_path+((ni, nj),)
                               )


def expand_grid(grid, i_scale, j_scale) -> list:
    i_size = len(grid)
    j_size = len(grid[0])
    new_grid = [[0 for x in range(j_size*j_scale)]
                for y in range(i_size*i_scale)]
    for i_offset, j_offset in product(range(i_scale), range(j_scale)):
        pos_cost = i_offset + j_offset
        for i, row in enumerate(grid):
            for j, val in enumerate(row):
                # Funky equation to cycle from [1, 9]
                new_cost = val + pos_cost
                new_cost -= 1
                new_cost %= 9
                new_cost += 1
                i_pos = i + i_size*i_offset
                j_pos = j + j_size*j_offset
                new_grid[i_pos][j_pos] = new_cost
    return new_grid


with p.open('r') as file:
    grid = [[int(n) for n in line.strip()] for line in file]
grid = expand_grid(grid, i_scale=5, j_scale=5)

end_point = (len(grid)-1, len(grid[-1])-1)  # Bottom left of grid

frontier = LCFSFrontier(pruning=True)
start_node = WeightedPath(cost=0, path=((0, 0),))
frontier.add(start_node)

start = perf_counter()
for path in frontier:
    head = path.path[-1]
    if head == end_point:
        print("Path found!")
        break
    for new_path in neighbours(grid, path):
        frontier.add(new_path)
end = perf_counter()

print(f"Time: {end-start:.3f}s")
print(f"{path.cost = }")
