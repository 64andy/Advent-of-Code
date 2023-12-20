"""
Day 8.1 - Haunted Wasteland

Python 3.9+

Input:
  You are given a list of Left/Right instructions (LRLRLRLRLR),
    and a graph from parent->2-children "ABC = (DEF, GHI)".
  Each node has 2 children, however they may be the same child "AAA = (AAA, AAA)"

Logic:
  You start at the node "AAA", and must reach the node "ZZZ".
  The instructions represent each move you must make (L=LeftChild, R=RightChild).
  For each instruction, move from your current node to the given child node.
  If you exhaust your instructions, repeat them (e.g. "LR" means "LRLRLRLR..." forever).

Output:
  Print how many moves it takes to reach the end
"""

import dataclasses
from pathlib import Path
import re
from typing import TextIO
from itertools import cycle


p = Path(__file__).with_name("input")

# Vars
NODE_REGEX = r"(...) = \((...), (...)\)"
GOAL = "ZZZ"     
DIRECTION = {
    "L": 0,
    "R": 1,
}       

# Classes
@dataclasses.dataclass
class ParsedFile:
    instructions: str
    nodes: dict[str, tuple[str, str]]

    @staticmethod
    def parse(file: TextIO) -> 'ParsedFile':
        nodes = {}
        instructions = next(file).strip()
        next(file)  # Skip the blank line
        for line in file:
            m = re.match(NODE_REGEX, line)
            assert m is not None, f"Couldn't parse the line {line!r} using the regex {NODE_REGEX!r}"
            base, lhs, rhs = m.groups()
            nodes[base] = (lhs, rhs)
        
        return ParsedFile(
            instructions=instructions,
            nodes=nodes
        )


# Funcs
...


# =====

def main():
    with p.open('r') as file:
        parsed_file = ParsedFile.parse(file)
    
    graph = parsed_file.nodes
    n_steps_taken = 0
    current_node = "AAA"    # We start at AAA
    for direction in cycle(parsed_file.instructions):
        if current_node == GOAL:
            break
        current_node = graph[current_node][DIRECTION[direction]]
        n_steps_taken += 1
    
    print("Number of steps to reach 'ZZZ':", n_steps_taken)



if __name__ == "__main__":
    main()
