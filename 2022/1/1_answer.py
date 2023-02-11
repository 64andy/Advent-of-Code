"""
Day 1.1 - Calorie Counting

You are given a list of numbers, with blank lines between each 'group'.

Simply return the highest calorie count in any group

e.g.
```
1
2

5
```
First group is (1+2=) 3 calories
Second group is (5=) 5 calories
So, return 5
"""

from pathlib import Path
p = Path(__file__).with_name("input")

# Vars
highest_calories = 0
current_run = 0

with p.open('r') as file:
    for line in file:
        if line == '\n': # Blank line, end of group
            highest_calories = max(highest_calories, current_run)
            current_run = 0
        else:
            current_run += int(line)

print(highest_calories)