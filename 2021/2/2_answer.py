"""
Ok now it's aim we're worried about.
up/down decreases/increases (respectively) our aim
forward increases our x-pos, AND increases depth by (aim * units)
"""

from pathlib import Path
p = Path(__file__).with_name("input")

# Vars
x = y = aim = 0

with p.open('r') as file:
    for line in file:
        cmd, units = line.split(' ')
        units = int(units)
        if cmd == 'forward':
            x += units
            y += aim * units
        elif cmd == 'down':
            aim += units
        elif cmd == 'up':
            aim -= units
        else:
            raise ValueError(f'Oh no help {cmd=}, {units=}')


print(x * y)