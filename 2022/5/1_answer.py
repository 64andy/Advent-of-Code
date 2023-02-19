"""
Day 5.1 - Supply Stacks

Input:
There are TWO data types in the file, separated by a newline:
1. A quasai-visual representation of stacked crates, in separate stacks,
     with a letter value in square brackets
2. A series of move instructions "move <num_values> from <src> to <dest>"
e.g. ```
    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2
```
---
Logic:
Each crate column is a stack (pop from the top), and each instruction tells you to 
move x number of crates from stack #src to stack #dest, one at a time
e.g. 'move 2 from 2 to 3' => Stack 2 = [M], Stack 3 = [P, D, C]

Output:
From left-to-right, print the top value of each stack
"""

from collections import defaultdict
from pathlib import Path
import re
from typing import Dict, List, TextIO, Tuple
p = Path(__file__).with_name("input")

# Vars
MOVE_PATTERN = r"move (\d+) from (\d+) to (\d+)"

# Funcs


def split_crates_and_instructions(file: TextIO) -> Tuple[List[str], List[str]]:
    """
    The two sections (Crates and instruction) are separated by a newline
    """
    crates_lines = []
    instruction_lines = []
    iter_file = iter(file)
    for container in [crates_lines, instruction_lines]:
        for line in iter_file:
            line = line.rstrip('\n')
            if line == '':
                break
            container.append(line)

    return (crates_lines, instruction_lines)


def parse_crates(crate_lines: List[str]) -> Dict[int, List[str]]:
    """
    Parses the crate text into a list of stacks.

    NOTE: This only works if there's upto 9 separate stacks.
    If it's double digit, it won't work.

    ### Example
    ```
    >>> input = [
    "    [D]    ",
    "[N] [C]    ",
    "[Z] [M] [P]",
    " 1   2   3 "
    ]
    # turns into
    >>> parse_crates(input)
    {1: ['Z', 'N'],
     2: ['M', 'C', 'D'],
     3: ['P']
    }
    """
    rev_lines = reversed(crate_lines)
    crates = defaultdict(list)
    # The final line is the key
    number_line = next(rev_lines)
    # The index of the number, and each crate's value, is the same.
    num_to_index = {idx: int(char) for (
        idx, char) in enumerate(number_line) if char.isdigit()}
    for line in rev_lines:
        for (idx, crate_num) in num_to_index.items():
            # If there's no whitespace, there's something there
            if not line[idx].isspace():
                crates[crate_num].append(line[idx])

    return dict(crates)


def main():
    with p.open('r') as file:
        crates_lines, instruction_lines = split_crates_and_instructions(file)
    # Parse the crate text into a dict
    crates = parse_crates(crates_lines)
    for line in instruction_lines:
        # Extract the nums from instructions. Parse into ints for ease
        count, src, dest = map(int, re.match(MOVE_PATTERN, line).groups())
        for _ in range(count):
            moving_value = crates[src].pop()
            crates[dest].append(moving_value)

    print(crates)
    print("Final char of each stack:", ''.join(stack[-1] for stack in crates.values()))


if __name__ == "__main__":
    main()
