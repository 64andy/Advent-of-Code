"""
Day 4.2: Camp Cleanup

Input:
4 numbers representing two ranges "a-b,x-y"

Logic:
Each range is inclusive on both sides.
Now, we care about if the ranges overlap in any way
- e.g. "1-3,2-4"; have shared numbers [2, 3]
 |- 1 2 3 -|
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
def ranges_overlap(a_1: int, a_2: int, b_1: int, b_2: int) -> bool:
    """
    `a_1 .. a_2` and `b_1 .. b_2` are two inclusive ranges.
    Returns true if the ranges have overlapping elements
    """
    return (a_1 <= b_1 <= a_2) or (b_1 <= a_1 <= b_2)


def main():
    total_overlaps = 0
    with p.open('r') as file:
        for line in file:
            nums = re.match(PATTERN, line).groups()
            a_1, a_2, b_1, b_2 = (int(d) for d in nums)
            total_overlaps += ranges_overlap(a_1, a_2, b_1, b_2)
    
    print("total_overlaps =", total_overlaps)

        

if __name__ == "__main__":
    main()
