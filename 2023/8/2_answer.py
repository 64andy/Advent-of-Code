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
import math
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

def is_goal(node: str) -> bool:
    return node.endswith('Z')


# =====

def testing_the_data(parsed_file):
    """
    Testing the data to see if there's any patterns we can exploit
    """
    print("===")
    graph = parsed_file.nodes
    nodes = list(filter(is_start, graph.keys()))    # We start at every node ending in 'A'
    print("Starting nodes:", nodes)
    for i, node in enumerate(nodes):
        n_steps_taken = 0
        n_times_hit = 0
        for direction in cycle(parsed_file.instructions):
            if n_times_hit >= 5:
                print("---")
                break
            if is_goal(node): # Stop once we've run out of nodes
                print(f"node[{i}] hit {node!r} on turning {direction!r} after {n_steps_taken} steps")
                n_times_hit += 1
            n_steps_taken += 1
            node = graph[node][DIRECTION[direction]]
    print()
    print("As we can see, each starting node will only hit a single terminal node.")
    print("It hits the same ones every time, so we can just need to calculate when they overlap...")
    print("We can do this with the lowest common multiple")
    print("===")

def main():
    with p.open('r') as file:
        parsed_file = ParsedFile.parse(file)
    
    testing_the_data(parsed_file)
    
    graph = parsed_file.nodes
    nodes = list(filter(is_start, graph.keys()))    # We start at every node ending in 'A'
    print("Starting nodes:", nodes)
    n_steps_per_node = []
    for i, node in enumerate(nodes):
        n_steps_taken = 0
        for direction in cycle(parsed_file.instructions):
            if is_goal(node): # Stop once we've run out of nodes
                print(f"n_steps_per_node[{i}] = {n_steps_taken}")
                n_steps_per_node.append(n_steps_taken)
                break
            else:
                n_steps_taken += 1
                node = graph[node][DIRECTION[direction]]
    
    print(f"They all terminate after (lcm({n_steps_per_node}) = {math.lcm(*n_steps_per_node)}) runs")
        



if __name__ == "__main__":
    main()
