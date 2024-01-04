"""
Day 12.2 - Hot Springs
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
  
  HOWEVER, for part 2, you repeat the springs 5 times (separated by an unknown), and repeat the numbers 5 times
    e.g. ".#. 1" becomes ".#.?.#.?.#.?.#.?.#. 1,1,1,1,1"

Output:
  Print the sum of each line's number of valid combinations
"""

import dataclasses
from pathlib import Path


p = Path(__file__).with_name("input")

# Vars
DEBUG_PRINT = False

UNFOLD_SIZE = 5
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

    def unfold(self, n_times=UNFOLD_SIZE) -> 'UnknownHotSprings':
        springs = '?'.join(self.springs for _ in range(n_times))
        layout = self.layout * n_times

        return UnknownHotSprings(springs, layout)

# Funcs
def debug_print(*args, **kwargs):
    if DEBUG_PRINT:
        print(*args, **kwargs)    

def springs_to_layout(springs: str, block_chars: list[str]) -> list[int]:
    """
    Converts a springs string into the layout formation.
    """
    layout = []
    current_count = 0
    in_damaged = False
    for char in springs:
        # If we're in a 'run', continue counting it
        if char in block_chars:
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

def _evaluate_locked_in_springs_for_pruning(springs: str, target_layout: list[int]) -> bool:
    """
    Runs a pruning check on everything to the left of the next unknown tile.

    Checks if what we've chosen so far matches the target layout
    """
    locked_in_springs = springs.split('?', 1)[0]
    if len(locked_in_springs) == 0: # Don't bother evaluating nothing
        return True
    layout = springs_to_layout(locked_in_springs, block_chars=[DAMAGED])
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
            if our_run != target_run:
                return False

    return True

def _evaluate_unknown_future_for_pruning(springs: str, target_layout: list[int]) -> bool:
    """
    Checks if what
    """
    return True
    locked_in_springs, _, future_springs = springs.partition('?')
    if len(future_springs) == 0:
        return True
    # Our layout is overly zealous
    layout = springs_to_layout(future_springs, block_chars=[DAMAGED, UNKNOWN])
    

def incomplete_springs_could_match_layout(springs: str, target_layout: list[int]) -> bool:
    """
    Checks if this incomplete springs view could be valid, for pruning.
    Note that these checks are conservative on what they allow.
    
    This means that if it returns True, it might be valid,
    however if it return False, it's *DEFINITELY INVALID*
    """
    return (
        _evaluate_locked_in_springs_for_pruning(springs, target_layout)
        and _evaluate_unknown_future_for_pruning(springs, target_layout)
    )

def springs_match_layout(springs: str, target_layout: list[int]) -> bool:
    """
    Checks if a completed springs matches the target *exactly*.
    """
    layout = springs_to_layout(springs, block_chars=[DAMAGED])
    return layout == target_layout

def get_all_valid_combinations(hot_spring: UnknownHotSprings) -> int:
    layout = hot_spring.layout
    
    all_combinations = [hot_spring.springs]
    total_valid_combinations = 0
    while all_combinations:
        springs = all_combinations.pop()
        # Base case: We've built a complete springs, add it if valid
        if UNKNOWN not in springs:
            if springs_match_layout(springs, layout):
                total_valid_combinations += 1
            else:
                debug_print("Invalid", springs)
            continue
        # If our springs could never match the layout, prune this branch
        if not incomplete_springs_could_match_layout(springs, layout):
            debug_print("Pruned ", springs)
            continue
        # Check the next two possible springs
        all_combinations.append(springs.replace(UNKNOWN, DAMAGED, 1))
        all_combinations.append(springs.replace(UNKNOWN, OPERATIONAL, 1))
    
    return total_valid_combinations

# =====

def main():
    with p.open('r') as file:
        all_springs = [UnknownHotSprings.parse(line).unfold() for line in file]
    
    total = 0
    for i, hot_springs in enumerate(all_springs):
        print(i)
        all_combinations = get_all_valid_combinations(hot_springs)
        total += all_combinations
    
    print("Total sum of combinations:", total)

if __name__ == "__main__":
    main()
