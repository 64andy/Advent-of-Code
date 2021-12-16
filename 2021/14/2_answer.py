"""
Day 14.2: Extended Polymerization

Given a starting template, and a list of pair rules,
each cycle you insert new characters according to the rules.

Example: The template "ABC", and the rules AB -> X, BC -> Y.
You read the template as a 2-len sliding window.
The first pair 'AB' matches the rule AB -> X, so put X in the middle
= AXBC
The second pair, 'BC', matches BC -> Y, so put Y in the middle
= AXBYC
This is the new template.
Note: You don't evaluate recently added chars. If there were a XB -> Z rule,
it wouldn't apply until the next cycle.

Part 2: After 40 cycles, what is the most common char's count, minus the
least common char's count?

Just like Day 6, 40 cycles takes too long to calculate as a string.
This is done by having two Counters: One tracking the count of each character,
and another tracking the count of each pair.

If there are 10 'AA' pairs, with an 'AA -> B' rule, then those 10 'AA's are
destroyed, and replaced by the same number of 'AB' and 'BC' pairs, with
10 new 'B' chars
"""

from pathlib import Path
from collections import Counter

p = Path(__file__).with_name("input")

# Vars
N_CYCLES = 40
rules = {}

with p.open('r') as file:
    template = file.readline().strip()
    file.readline()  # Skip past the blank line
    for line in file:
        lhs, _, rhs = line.partition(' -> ')
        lhs = lhs.strip()
        rhs = rhs.strip()
        rules[lhs] = rhs


char_counts = Counter(template)
pair_counts = Counter(template[i:i+2] for i in range(len(template) - 1))
for _ in range(N_CYCLES):
    new_pair_counts = pair_counts.copy()
    for pair in pair_counts:
        if pair in rules:
            # Split it up
            n_occurences = pair_counts[pair]
            middle = rules[pair]        # .B.
            l_pair = pair[0] + middle   # AB.
            r_pair = middle + pair[1]   # .BC
            # First, destroy all the pair's occurences, because
            # turning AC -> ABC means AC is no longer a pair
            new_pair_counts[pair] -= n_occurences
            # Turn them into an equal amount of AB and AC pairs
            new_pair_counts[l_pair] += n_occurences
            new_pair_counts[r_pair] += n_occurences
            # Track the middle character we just added
            char_counts[middle] += n_occurences
    pair_counts = new_pair_counts

c = Counter(char_counts).most_common()

mc_c, mc_n = c[0]
lc_c, lc_n = c[-1]

print(f"Most common char: {mc_c} with {mc_n} occurences.")
print(f"Least common char: {lc_c} with {lc_n} occurences.")
print("Difference:", mc_n - lc_n)