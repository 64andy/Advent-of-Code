"""
Fish population simulation.

Oh god this will not scale, have to do smart brain stuff
"""

from pathlib import Path
from math import ceil, floor
p = Path(__file__).with_name("input")


# Vars
N_ITERATIONS = 256+1
REPEAT_EVERY = 6    # A fish spawns one new fish after this many days
FRESH_SPAWN = 8     # A fish's first cycle takes this long


def calc_new_fish(all_fish: list, n_days: int) -> int:
    """
    Calculates the number of children fish generated by
    a group of fish
    """
    # A list whose index is the amount of fish with the current timer.
    # Shifts left to represent a day passing
    fish = [0] * (FRESH_SPAWN + 1)
    for f in all_fish:
        fish[f+1] += 1
    for day in range(n_days):
        gave_birth = fish.pop(0)    # Fish who gave birth
        fish.append(gave_birth)     # Spawn their children
        fish[REPEAT_EVERY] += gave_birth # Reset the parent's timer
        print(day, ':', sum(fish))
    return sum(fish)



fish = []

with p.open('r') as file:
    for n in file.read().split(','):
        fish.append(int(n))
print(calc_new_fish(fish, N_ITERATIONS))
exit()



print(_+1, ':', len(fish))