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

Because the numbers 1,4,7,8 light up a
unique number of segments, we only look
for those first
"""

from pathlib import Path
p = Path(__file__).with_name("input")

# Vars
VALID_LENGTHS = {
    2,  # '1' lights up 2 segments
    4,  # '4' lights up 4
    3,  # '7' lights up 3
    7,  # '8' light up 7
}

everything = []

with p.open('r') as file:
    for line in file:
        _lhs, rhs = line.split('|')
        everything.extend(rhs.split())

wanted_numbers_found = 0
for segment in everything:
    segment = segment.strip()
    if segment == '|':
        continue
    if len(segment) in VALID_LENGTHS:
        wanted_numbers_found += 1

print(wanted_numbers_found)
