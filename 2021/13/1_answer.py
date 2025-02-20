"""
Day 13.1: Transparent Origami

We are provided a list of dots on a 2D piece of paper (4,5)
We are also provided with folding instructions (fold along x=5)

When folding, we delete that line and look at either side.
When folding, dots can overlap.
We always fold left or up, never right or down.

e.g.
    4
    |
.....##               ..##
###..#.,  fold on  => ####
.....#.    x = 4      ...#
    ^
Part 1 question: How many dots remain after folding once?
"""

from pathlib import Path
from typing import Tuple
p = Path(__file__).with_name("input")

# Vars
dots = set()
instructions = []


def partition(dots: set, axis: str, pos: int) -> Tuple[set, set]:
    """
    Takes a set of co-ordinate pairs (x, y), an axis ('x' or 'y'), and a pos.
    Returns two sets: One of all the co-ords left/above the given line pos,
    and one to the right/below the line pos.
    Note: This function will destroy any items on a line
    """
    index = {'x': 0, 'y': 1}[axis]  # x is first index in tuple, y is second index
    lhs = {pair for pair in dots if pair[index] < pos}
    rhs = {pair for pair in dots if pair[index] > pos}
    return lhs, rhs


def fold(dots: set, axis: str, pos: int) -> set:
    lhs, rhs = partition(dots, axis, pos)
    for x, y in rhs:
        if axis == 'x':
            pair = (pos - (x - pos), y)
        else:
            pair = (x, pos - (y - pos))
        lhs.add(pair)
    return lhs


with p.open('r') as file:
    # Parse dots
    for line in file:
        # Instructions separated by blank line
        if line.isspace():
            break
        x, _, y = line.partition(',')
        dots.add((int(x), int(y)))
    # Remaining lines are instructions
    for line in file:
        axis, _, pos = line.partition('=')
        axis = axis.lstrip('fold along ')
        pos = int(pos)
        instructions.append((axis, pos))

axis, pos = instructions[0]
lhs, rhs = partition(dots, axis, pos)
folded = fold(dots, axis, pos)
print(sorted(lhs), sorted(rhs))
print()
print(sorted(folded), '=', len(folded))