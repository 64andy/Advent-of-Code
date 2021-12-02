"""
Now a sliding window of size 3.
Is this sum of 3 larger than the last?

We can change this problem to a window
of size-4, and check [A, _, _, B]; B > A?
"""

from pathlib import Path
p = Path(__file__).with_name("input")

count = 0

with p.open('r') as file:
    nums = [int(file.readline()) for _ in range(3)]
    for now in file:
        nums.append(int(now))
        if nums[3] > nums[0]:
            count += 1
        del nums[0]

print(count)