"""
Now you filter numbers down.
'Oxygen' is found by finding the most common bit in a
position, and removing numbers that don't have that bit.
On a tie, '1' wins, repeat until one number remains.
'CO2' is the same, but filtering the *most* common.
"""

from pathlib import Path
from collections import Counter
p = Path(__file__).with_name("input")

def most_common_bit(nums, at_pos):
    count = {'0': 0, '1': 0}
    for num in nums:
        count[num[at_pos]] += 1
    
    return '1' if count['1'] >= count['0'] else '0'

# Vars
with p.open('r') as file:
    nums = [line.strip() for line in file]
num_len = len(nums[0])

# Find oxygen
oxygen_nums = nums.copy()
for j in range(num_len):
    most_common = most_common_bit(oxygen_nums, at_pos=j)
    oxygen_nums = [n for n in oxygen_nums if n[j] == most_common]
    if len(oxygen_nums) == 1:
        break
else:
    print("Error: The list is", len(oxygen_nums), "long:", oxygen_nums)

o2 = oxygen_nums[0]
print("Oxygen number is", o2, '|', int(o2, base=2))

# Find CO2
co2_nums = nums.copy()
for j in range(num_len):
    most_common = most_common_bit(co2_nums, at_pos=j)
    co2_nums = [n for n in co2_nums if n[j] != most_common]
    if len(co2_nums) == 1:
        break
else:
    print("Error: The list is", len(co2_nums), "long:", co2_nums)

co2 = co2_nums[0]
print("CO2 number is", co2, '|', int(co2, base=2))