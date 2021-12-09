"""
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

LHS is the hints to what each number means, RHS is the number.
Gotta be smart
"""

from pathlib import Path
from typing import List, FrozenSet, DefaultDict
from collections import defaultdict
p = Path(__file__).with_name("input")

# Vars
NUM_SEGS = [ # In a 7-segment display
    6,  # 0
    2,  # 1
    5,  # 2
    5,  # 3
    4,  # 4
    5,  # 5
    6,  # 6
    3,  # 7
    7,  # 8
    6,  # 9
]


def associate_nums(_codes: List[FrozenSet[str]]) -> List[FrozenSet[str]]:
    """
    Takes a list of unknown 7-segment codes, and maps them to their
    correct numbers.
    """
    # The only distinguishing factor is each code's length
    unknown: DefaultDict[int, List[FrozenSet]] = defaultdict(list)
    for code in _codes:
        unknown[len(code)].append(code)
    known: List[FrozenSet] = [None] * 10
    # 1, 4, 7, and 8 have unique lengths
    known[1] = unknown[NUM_SEGS[1]].pop()
    known[4] = unknown[NUM_SEGS[4]].pop()
    known[7] = unknown[NUM_SEGS[7]].pop()
    known[8] = unknown[NUM_SEGS[8]].pop()
    # 0, 6, 9 are all 6-len
    # Whatever *doesn't* superset 1 is 6
    six_lens = unknown[6]
    for i in range(len(six_lens)):
        if not six_lens[i].issuperset(known[1]):
            known[6] = six_lens.pop(i)
            break
    # Whatever supersets 4 is 9
    for i in range(len(six_lens)):
        if six_lens[i].issuperset(known[4]):
            known[9] = six_lens.pop(i)
            break
    # Whatever remains must be 0
    known[0] = six_lens.pop()
    # 2, 3, 5 are all 5-len.
    # Of them, only 3 supersets 1.
    five_lens = unknown[5]
    for i in range(len(five_lens)):
        if five_lens[i].issuperset(known[1]):
            known[3] = five_lens.pop(i)
            break
    # Out of 2, 5, only 5 subsets 6
    for i in range(len(five_lens)):
        if five_lens[i].issubset(known[6]):
            known[5] = five_lens.pop(i)
            break
    # Whatever remains must be 2
    known[2] = five_lens.pop()

    return known


def decode_numbers(lhs: List[FrozenSet[str]], rhs: List[FrozenSet[str]]) -> int:
    """
    Give a lhs of the 7-segment representation of all numbers,
    and a rhs of the numbers we want to know,
    returns the numbers decoded.
    """
    s_num = 0
    e = 0
    mapping = associate_nums(lhs)
    for to_know in reversed(rhs):
        for i, code in enumerate(mapping):
            if code == to_know:
                s_num += i * 10**e
                e += 1
                break
    return s_num


total = 0
with p.open('r') as file:
    for line in file:
        lhs, rhs = line.split('|')
        # Prep into sets to do set operations
        lhs = [frozenset(s.strip()) for s in lhs.split()]
        rhs = [frozenset(s.strip()) for s in rhs.split()]
        # Decode them
        number = decode_numbers(lhs, rhs)
        total += number
print(total)
