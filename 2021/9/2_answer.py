"""
Day 9.2 - Given a grid of nums, find 'basins'.

A basin is all locations that eventually flow downward
to a single low point. Therefore, every low point has a basin,
although some basins are very small.
Locations of height 9 do not count as being in any basin,
and all other locations will always be part of exactly one basin.

The size of a basin is the number of locations within the basin,
including the low point.

Logic: BFS Flood fill
"""

from collections import deque
from heapq import heappop, heappush
from pathlib import Path
p = Path(__file__).with_name("input")


def neighbours(grid, i, j):
    """
    Generator.
    Returns the co-ords above, below, left, and right of
    the given position, if it's in range
    """
    COORDS = ((-1, 0), (0, 1), (1, 0), (0, -1))
    for di, dj in COORDS:
        ni = i + di
        nj = j + dj
        if 0 <= ni < len(grid) and 0 <= nj < len(grid[ni]):
            yield (ni, nj)




def main():
    with p.open('r') as file:
        grid = [[int(i) for i in line.strip()]
                for line in file
                if line.strip()
                ]
    # Placing 'visited' down here because each tile is part of
    # only 1 basin (unless it's above the waterline).
    visited = [[False for _ in line] for line in grid]
    highest = max(n for line in grid for n in line)

    basins = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            basin_size = 0
            frontier = deque()
            frontier.append( (i, j) )
            while len(frontier) > 0:
                i, j = frontier.popleft()
                if not visited[i][j]:
                    visited[i][j] = True
                    if grid[i][j] < highest:
                        frontier.extend(neighbours(grid, i, j))
                        basin_size += 1
            if basin_size > 0:
                # Negative basin_size because `heapq` is a min-heap
                heappush(basins, -basin_size)
    
    print("3 largest basins:")
    best = [heappop(basins) for _ in range(3)]
    # Correct the negatives
    print(f"{-best[0]} * {-best[1]} * {-best[2]} =", -best[0]*-best[1]*-best[2])


if __name__ == "__main__":
    main()
