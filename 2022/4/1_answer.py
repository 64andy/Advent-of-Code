"""
Day 4.1: Camp Cleanup

Input:
4 numbers representing two ranges "a-b,x-y"

Logic:
Each range is inclusive on both sides.
Right now, we care about if either range *fully contains* the other
- e.g. "1-5,2-4"; 2-4 is contained within 1-5

|- 1 2 3 4 5 -|
  |- 2 3 4 -|

Output:
How many pairs have one range containing the other?
"""

from pathlib import Path
import re

p = Path(__file__).with_name("input")

# Vars
PATTERN = r"(\d+)-(\d+),(\d+)-(\d+)"

# Funcs
def either_range_is_subset(a_1: int, a_2: int, b_1: int, b_2: int) -> bool:
    """
    `a_1 .. a_2` and `b_1 .. b_2` are two inclusive ranges.
    Returns true if either range is a subset of the other.
    """
    return (a_1 >= b_1 and a_2 <= b_2) or (b_1 >= a_1 and b_2 <= a_2)


def main():
    total_overlaps = 0
    with p.open('r') as file:
        for line in file:
            nums = re.match(PATTERN, line).groups()
            a_1, a_2, b_1, b_2 = (int(d) for d in nums)
            total_overlaps += either_range_is_subset(a_1, a_2, b_1, b_2)
    
    print("total_overlaps =", total_overlaps)

        

if __name__ == "__main__":
    main()
