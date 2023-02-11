"""
Day 3.1: Rucksack Reorganization
===
Input:
Each input line is a string, represents two sacks (left-half and right-half)
- e.g. "abccde" => "abc", "cde"

Logic:
In each half, there's only one shared letter in both halves (case-sensitive).
That letter has a score [a-z => 1-26, A-Z => 27-52]

Output:
Sum the total score of each line's shared letter
"""

from pathlib import Path
from string import ascii_letters    # Its score is its index in this list + 1

p = Path(__file__).with_name("input")

# Vars
letter_score = dict(zip(ascii_letters, range(1, len(ascii_letters)+1)))

# Funcs
def shared_letter(line: str) -> str:
    """
    Returns the shared character that's in both the left-half
    and right-half of the string
    """
    # Split in half
    halfway = len(line) // 2
    lhs = set(line[:halfway])
    rhs = set(line[halfway:])
    # Get common char
    shared_character = lhs & rhs
    assert len(shared_character) == 1
    return shared_character.pop()


total_score = 0
with p.open('r') as file:
    for line in file:
        line = line.rstrip()    # Remove newline
        char = shared_letter(line)
        total_score += letter_score[char]

print("total_score =", total_score)
