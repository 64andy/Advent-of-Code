"""
Fish population simulation.

Oh god this will not scale, have to do smart brain stuff
"""

from pathlib import Path
p = Path(__file__).with_name("input")

# class Fish:
#     def __init__(self, timer, orig_fish=False):
#         self.timer = timer
#         self.orig_fish = orig_fish

# Vars
N_ITERATIONS = 256
FRESH_CAP = 8       # Freshly spawned fish start at this
REPEAT_CAP = 6      # After creating a new fish, it's set to this 
fish = []

with p.open('r') as file:
    for n in file.read().split(','):
        fish.append(int(n))

fish = [3]

for _ in range(N_ITERATIONS):
    print(_, ':', len(fish))
    for i in range(len(fish)):
        if fish[i] == 0:
            fish[i] = REPEAT_CAP
            fish.append(FRESH_CAP)
        else:
            fish[i] -= 1

print(len(fish))