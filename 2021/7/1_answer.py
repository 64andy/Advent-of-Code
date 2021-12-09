"""
Distance calculation. What whole number has the
shortest distance from all the other numbers?

Note: I misunderstood. I thought the 'centre' had to
be from the number list, but it's any whole number.
It still worked with this case however
"""

from pathlib import Path
from math import inf
p = Path(__file__).with_name("input")

# Vars
current_best = inf
best_spot = -1


with p.open('r') as file:
    nums = sorted(map(int, file.read().strip().split(',')))


for align in nums:
    dist = sum(abs(align-n) for n in nums)
    if dist < current_best:
        current_best = dist
        best_spot = align

print(f"{current_best=}, {best_spot=}")