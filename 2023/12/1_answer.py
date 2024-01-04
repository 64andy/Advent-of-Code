"""
Day 12.1 - Hot Springs
(hell yeah I love picross)

Python 3.9+

Input:
  Each line represents an unknown hot springs layout.
  It has two space-separated parts:
  1. The textual represention of the springs, made up of:
    - '.': A known empty spot (Operational)
    - '#': A known filled spot (Damaged)
    - '?': An unknown spot (Could be empty or filled)
    e.g. ".###.?#.#.??"
  2. A comma separated list of numbers, representing the damaged runs in the springs.
    e.g. "1,2,3"

Logic:
  This is Picross. The "springs" are a row, and the numbers show all the runs and their lengths.
    e.g. ..###.##.#. is 3,2,1
  However, the question marks could either be filled or empty.
    e.g. .???#??#?#. can still be 3,2,1
  We want to count the amount of valid springs, which conform to the layout, are
    possible if we change the unknowns.
  Examples:
    1. ???.##. 1,1,2
        There is only one valid combination:
        - #.#.##.
    2. .??.??.?##. 1,1,3
        There are 4 possible combinations:
        - .#..#..###
        - ..#.#..###
        - .#...#.###
        - ..#..#.###

Output:
  Print the sum of each line's number of valid combinations
"""

import dataclasses
from pathlib import Path


p = Path(__file__).with_name("input")

# Vars
DEBUG_PRINT = False

OPERATIONAL = '.'
DAMAGED = '#'
UNKNOWN = '?'

# Classes
@dataclasses.dataclass
class UnknownHotSprings:
    springs: str
    layout: list[int]

    @staticmethod
    def parse(line: str) -> 'UnknownHotSprings':
        # Layout of string: ".###.??.#.? 3,1,1"
        springs, layout_s = line.split(' ', maxsplit=1)
        layout = [int(n) for n in layout_s.split(',')]
        return UnknownHotSprings(springs, layout)

# Funcs
def debug_print(*args, **kwargs):
    if DEBUG_PRINT:
        print(*args, **kwargs)    

def springs_to_layout(springs: str) -> list[int]:
    """
    Converts a springs string into the layout formation.
    Note that this *only* looks at damaged tiles, treating
      unknowns as operational.
    We're being conservative so we can parse incomplete springs
      to see if it's possible to prune one.
    """
    layout = []
    current_count = 0
    in_damaged = False
    for char in springs:
        # If we're in a 'run', continue counting it
        if char == DAMAGED:
            in_damaged = True
            current_count += 1
        # If we're not in a run, but we were in one, that means it just ended
        elif in_damaged:
            layout.append(current_count)
            current_count = 0
            in_damaged = False
        # If we're not in a run, and we didn't read a damaged tile, do nothing
        else:
            pass
    # If we ended on a line, don't forget to add it
    if in_damaged:
        layout.append(current_count)
    
    return layout


def incomplete_springs_could_match_layout(springs: str, target_layout: list[int]) -> bool:
    """
    Checks if this incomplete springs view could be valid, for pruning.
    Note that these checks are conservative on what they allow.
    
    This means that if it returns True, it might be valid,
    however if it return False, it's *DEFINITELY INVALID*
    """
    # We only look at the part of the springs whose values are determined.
    # Evaluating anything not "locked in" complicates things
    locked_in_springs = springs.split(UNKNOWN, maxsplit=1)[0]
    if len(locked_in_springs) == 0: # Don't bother evaluating nothing
        return True
    layout = springs_to_layout(locked_in_springs)
    # If we have more runs than the target, despite being a
    #   subset of the target, we're definitely wrong
    if len(layout) > len(target_layout):
        return False
    # Check if our final run could still be getting built.
    # This is because ".###" COULD be proceeded by anything,
    #   however ".###." is a finalised 3-long run
    last_run_is_finalised = (locked_in_springs[-1] == OPERATIONAL)

    for i, (our_run, target_run) in enumerate(zip(layout, target_layout)):
        is_final_element = (i == len(layout)-1)
        # If a run is longer than theirs, we've added too many blocks.
        # Even the final element must pass this check.
        if our_run > target_run:
            return False
        # If a run is shorter than theirs, we've added too few blocks.
        # The exception is the final element, because we could still be building it
        if not is_final_element and our_run < target_run:
            return False
        # If this is the final element, and we're not in the middle of building a run,
        #    it's fine to do an equality check.
        if is_final_element and last_run_is_finalised:
            return our_run == target_run

    return True

def springs_match_layout(springs: str, target_layout: list[int]) -> bool:
    """
    Checks if a completed springs matches the target *exactly*.
    """
    layout = springs_to_layout(springs)
    return layout == target_layout

def recursive_get_combination(springs: str, layout: list[int], output: list[str]):
    # Base case: We've built a complete springs, add it if valid
    if UNKNOWN not in springs:
        if springs_match_layout(springs, layout):
            output.append(springs)
        else:
            debug_print("Invalid", springs)
        return
    # If our springs could never match the layout, prune this branch
    if not incomplete_springs_could_match_layout(springs, layout):
        debug_print("Pruned ", springs)
        return
    # Check the next two possible springs
    for symbol in (DAMAGED, OPERATIONAL):
        next_springs = springs.replace(UNKNOWN, symbol, 1)
        recursive_get_combination(next_springs, layout, output)


def get_all_valid_combinations(hot_spring: UnknownHotSprings) -> list[str]:
    valid_combinations = []
    recursive_get_combination(hot_spring.springs, hot_spring.layout, valid_combinations)
    return valid_combinations

# =====

def main():
    with p.open('r') as file:
        all_springs = [UnknownHotSprings.parse(line) for line in file]
    
    total = 0
    for hot_springs in all_springs:
        debug_print(hot_springs.layout)
        all_combinations = get_all_valid_combinations(hot_springs)
        total += len(all_combinations)
        debug_print("All combinations:", len(all_combinations), '|', all_combinations)
        debug_print("=====")
    
    print("Total sum of combinations:", total)

if __name__ == "__main__":
    main()
