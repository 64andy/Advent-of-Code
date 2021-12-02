from collections import defaultdict

INPUT_FILE = "day7.in"
ROOT_BAG = 'shiny gold'

def parse_bag_instructions(line: str) -> (str, list):
    """
    Example line:
    'light red bags contain 1 bright white bag, 2 muted yellow bags.'

    Returns:
    2-Tuple - (This line's bag colour, list(bags contained in this bag))
    """
    can_hold = []
    line = line.split()
    this_bag = ' '.join((line[0], line[1]))
    line = line[4:]     # cut off "{colour} {colour} bags contain "
    line = iter(line)
    for word in line:   # Skips the useless number
        if word == "no":
            break
        bag = ' '.join((next(line), next(line)))  # Skip the useless nu
        can_hold.append(bag)
        next(line)      # skips the "bag(s)[,|.]"
    return this_bag, can_hold


all_bags = defaultdict(list)    # <ThisBag : Bags that can hold ThisBag>
with open(INPUT_FILE, 'r') as file:
    for line in file:
        this_bag, can_hold = parse_bag_instructions(line)
        for bag in can_hold:
            all_bags[bag].append(this_bag)

# Plan: Add every bag that can hold shiny gold to a set
# Add every bag that can hold *those* bags to the set
# Repeat until the set stops updating
orig_valid_len = 0
valid_bags = set(all_bags[ROOT_BAG])
while orig_valid_len != len(valid_bags):
    orig_valid_len = len(valid_bags)
    to_add = set()
    for bag in valid_bags:
        to_add.update(all_bags[bag])
    valid_bags.update(to_add)

print(valid_bags)
print(len(valid_bags))