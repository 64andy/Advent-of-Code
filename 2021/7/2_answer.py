"""
Distance calculation. What whole number has the
shortest distance from all the other numbers?
"""

from pathlib import Path
from math import inf
p = Path(__file__).with_name("input")


def triangle_number(n):
	return (n * (n+1)) // 2


def calc_dist(nums, pivot):
    return sum(triangle_number(abs(pivot-n)) for n in nums)



# Vars
current_best = inf
best_spot = -1

with p.open('r') as file:
    nums = [int(n) for n in file.read().strip().split(',')]

left = min(nums)
right = max(nums)
current_best = inf
best_spot = -1
for pivot in range(left, right):
    dist = calc_dist(nums, pivot)
    if dist < current_best:
        current_best = dist
        best_spot = pivot
    print(f"{pivot} : {dist}")


print(f"{current_best=}, {best_spot=}")