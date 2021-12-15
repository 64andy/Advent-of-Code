"""
Day 12.1: Passage Pathing

It's a graphing problem.
Connections are represented with 'abc-def', bi-directional
There is a start and end node
Lower case nodes can only be visited once
Upper case nodes can be revisited many times

Part 1 question: How many unique paths from start->end are there?

In this, the paths are stored as tuples of nodes.
"""

from collections import defaultdict, deque
from pathlib import Path
p = Path(__file__).with_name("input")

# Vars
layout = defaultdict(list)
frontier = deque()
complete_paths = []

# Build the connections
with p.open('r') as file:
    for line in file:
        lhs, _, rhs = line.partition('-')
        lhs = lhs.strip()
        rhs = rhs.strip()
        layout[lhs].append(rhs)
        layout[rhs].append(lhs)

# Now BFS
frontier.append( ('start',) )
while len(frontier) > 0:
    path = frontier.popleft()
    head = path[-1]
    # Have we reached the end?
    if head == 'end':
        complete_paths.append( ','.join(path) )
        continue
    # Prune if a lowercase node repeats
    if head.islower() and path.count(head) >= 2:
        continue
    for neighbour in layout[head]:
        frontier.append( path + (neighbour,) )

for path in complete_paths:
    print(path)
print(f"{len(complete_paths) = }")