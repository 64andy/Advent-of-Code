"""
Commands change our horizontal & vertical position.
Output is the product of these two.
up/down will decrease/increase (respectively) our depth (y),
forward increases our x.
"""

from pathlib import Path
p = Path(__file__).with_name("input")

# Vars
x = y = 0

with p.open('r') as file:
    for line in file:
        cmd, units = line.split(' ')
        units = int(units)
        if cmd == 'forward':
            x += units
        elif cmd == 'down':
            y += units
        elif cmd == 'up':
            y -= units
        else:
            raise ValueError(f'Oh no help {cmd=}, {units=}')


print(x * y)