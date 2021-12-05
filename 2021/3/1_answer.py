"""
For each number, check the most common bit in a position.
That bit becomes x's bit in that position. Convert to an int, 
multiply by its complement (e.g. 0110 -> 1001), and that's the answer.
"""

from pathlib import Path
p = Path(__file__).with_name("input")

# Vars
most_common = []

with p.open('r') as file:
    for column in zip(*file):
        most_common.append(max(column, key=column.count))

most_common = ''.join(most_common).strip()
inverse = ''.join('1' if c == '0' else '0' for c in most_common)

most_common = int(most_common, base=2)
inverse = int(inverse, base=2)
print(most_common * inverse)