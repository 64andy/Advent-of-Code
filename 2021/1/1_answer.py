"""
Increment if the current value's
larger than the last
"""

from pathlib import Path
p = Path(__file__).with_name("input")

count = 0

with p.open('r') as file:
    prev = int(file.readline())
    for now in file:
        now = int(now)
        if now > prev:
            count += 1
        prev = now

print(count)