"""
Day 12.2: Passage Pathing

It's a graphing problem.
Connections are represented with 'abc-def', bi-directional
There is a start and end node
Lower case nodes can only be visited once*
- Part 2 new rule: At most, a single lower node can be visited
  twice. start and end can't be revisited twice.

Upper case nodes can be revisited many times

Part 2 question: How many unique paths from start->end are there?

In this, the paths are stored as tuples of nodes.
"""

from collections import defaultdict, deque, Counter
from pathlib import Path
p = Path(__file__).with_name("input")

def path_is_valid(path) -> bool:
    """
    Returns if the given path is valid.
    Current rules: A single lower node can be
    revisited twice.

    This function goes off the assumption that everything
    before the head is valid.
    """
    counter = Counter(path)
    # We can't revisit 'start'
    if counter['start'] > 1:
        return False
    # Now check for repeats
    has_repeat = False
    for c, n in counter.most_common():
        # Ignore uppers
        if c.isupper():
            continue
        # Can't visit more than twice
        if n > 2:
            return False
        # Check it's the only repeat
        if n == 2:
            if has_repeat:
                return False
            else:
                has_repeat = True
    # Passed all checks
    return True


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
    if not path_is_valid(path):
        continue
    for neighbour in layout[head]:
        frontier.append( path + (neighbour,) )

# for path in complete_paths:
#     print(path)
print(f"{len(complete_paths) = }")