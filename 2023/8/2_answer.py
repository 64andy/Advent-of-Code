"""
Day 8.2 - Haunted Wasteland

Python 3.9+

Input:
  You are given a list of Left/Right instructions (LRLRLRLRLR),
    and a graph from parent->2-children "ABC = (DEF, GHI)".
  Each node has 2 children, however they may be the same child "AAA = (AAA, AAA)"

Logic:
  You start with a *list* of nodes, containing *each* node ending with "A"
    e.g. [AAA, BCA, ...].
  The instructions represent each move you must make (L=LeftChild, R=RightChild).
  For each instruction, move every current node to its given child node *at the same time*.
  If you exhaust your instructions, repeat them (e.g. "LR" means "LRLRLRLR..." forever).
  You terminate when all your current nodes end with "Z".

  Moving all of your nodes at once counts as a single step

Output:
  Count and print how many steps it takes to reach the end

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
def is_start(node: str) -> bool:
    return node.endswith('A')

def is_goal(nodes: list[str]) -> bool:
    return all(node.endswith('Z') for node in nodes)


# =====

def main():
    with p.open('r') as file:
        parsed_file = ParsedFile.parse(file)
    
    graph = parsed_file.nodes
    n_steps_taken = 0
    current_nodes = list(filter(is_start, graph.keys()))    # We start at every node ending in 'A'
    for direction in cycle(parsed_file.instructions):
        if is_goal(nodes=current_nodes): # Stop once we've run out of nodes
            break
        n_steps_taken += 1
        if n_steps_taken%100_000 == 0:
            print(n_steps_taken)
        new_nodes = []
        for node in current_nodes:
            new_nodes.append(graph[node][DIRECTION[direction]])
        current_nodes = new_nodes
    
    print("Number of steps to reach 'ZZZ':", n_steps_taken)



if __name__ == "__main__":
    main()
