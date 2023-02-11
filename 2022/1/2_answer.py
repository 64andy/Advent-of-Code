"""
Day 1.2 - Calorie Counting

You are given a list of numbers, with blank lines between each 'group'.

Now, return the sum of the three highest calorie groups
"""

from pathlib import Path
p = Path(__file__).with_name("input")

# Vars
MAX_LEN = 3
highest_calories = []
current_run = 0

def insert_if_large_enough(sorted_array: list, max_len: int, item: int):
    if len(sorted_array) < max_len:
        sorted_array.append(item)
    else:
        if sorted_array[0] < item:
            sorted_array[0] = item
    sorted_array.sort()


with p.open('r') as file:
    for line in file:
        if line == '\n': # Blank line, end of group
            insert_if_large_enough(highest_calories, MAX_LEN, current_run)
            current_run = 0
        else:
            current_run += int(line)

print(sum(highest_calories))