"""
Day 3.2: Rucksack Reorganization
===
Input:
Each input line is a string, representing a single sack.
Every 3 sacks is a group

Logic:
In each group of three, there is one shared letter

Output:
Sum the total score of each group's
"""

from functools import reduce
from pathlib import Path
from string import ascii_letters
from typing import Iterable

p = Path(__file__).with_name("input")

# Vars
GROUP_SIZE = 3
LETTER_SCORE = dict(zip(ascii_letters,
                        range(1, len(ascii_letters)+1))
) # azAZ => 1..52

# Funcs
def shared_letter(lines: Iterable[str]) -> str:
    """
    Returns the shared character that's in all lines
    """
    # Reduce
    lines_as_sets = map(set, lines)
    shared_character = set(reduce(set.intersection, lines_as_sets))
    # Get common char
    assert len(shared_character) == 1
    return shared_character.pop()


total_score = 0
with p.open('r') as file:
    file_iter = iter(file)
    try:    # Loop until EOF
        while True:
            group = [next(file_iter).rstrip() for _ in range(GROUP_SIZE)]
            char = shared_letter(group)
            total_score += LETTER_SCORE[char]
    except StopIteration:
        pass

print("total_score =", total_score)
