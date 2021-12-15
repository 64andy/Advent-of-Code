"""
Day 11.1: Dumbo Octopus

Each tile is an octopus. Every cycle, their timer increases by 1.
When their number exceeds 9, they flash (blink), and increase their
neighbours timer by 1. This can cause a cascade of flashes.

Tricky part, a tile can be incremented by all its neighbours,
but once it blinks it must reset to 0 and ignore all further
blinks until next turn.

Part 1 question: How many flashes happen in 100 cycles?
"""

from collections import deque
from heapq import heappop, heappush
from pathlib import Path
p = Path(__file__).with_name("input")

N_CYCLES = 100

def neighbours(grid, i, j):
    """
    Generator.
    Returns the co-ords of all 8 neighbours
    """
    for di in (-1, 0, 1):
        for dj in (-1, 0, 1):
            if di == dj == 0:
                continue
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

    frontier = deque()
    height = len(grid)
    width = len(grid[0])
    n_flashes = 0
    for _ in range(N_CYCLES):
        # Step 1: Increment all by 1, tracking what's blinked
        for i in range(height):
            for j in range(width):
                grid[i][j] += 1
                if grid[i][j] > 9:
                    frontier.append((i, j))
        # Step 2: Use BFS to cascade the blinks
        while len(frontier) > 0:
            i, j = frontier.popleft()
            if grid[i][j] == 0: # It's already blinked
                continue
            grid[i][j] += 1
            if grid[i][j] > 9:
                # Blink, mark as blinked, and cascade
                grid[i][j] = 0
                n_flashes += 1
                frontier.extend(neighbours(grid, i, j))
    
    print(n_flashes)

if __name__ == "__main__":
    main()
