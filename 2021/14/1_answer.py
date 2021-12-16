"""
Day 14.1: Extended Polymerization

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

Part 1: After 10 cycles, what is the most common char's count, minus the
least common char's count?
"""

from pathlib import Path
from collections import Counter

p = Path(__file__).with_name("input")

# Vars
N_CYCLES = 10
rules = {}

with p.open('r') as file:
    template = file.readline().strip()
    file.readline() # Skip past the blank line
    for line in file:
        lhs, _, rhs = line.partition(' -> ')
        lhs = lhs.strip()
        rhs = rhs.strip()
        rules[lhs] = rhs

for _ in range(N_CYCLES):
    new_template = [template[0]]
    for i in range(len(template) - 1):
        pair = template[i] + template[i+1]
        if pair in rules:
            new_template.append(rules[pair])
        new_template.append(pair[1])
    template = new_template


c = Counter(template).most_common()

mc_c, mc_n = c[0]
lc_c, lc_n = c[-1]

print(f"Most common char: {mc_c} with {mc_n} occurences.")
print(f"Least common char: {lc_c} with {lc_n} occurences.")
print("Difference:", mc_n - lc_n)

