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
    for num in line:   # It's timed so `num` is only ever a number
        if num == "no":
            break
        bag = ' '.join((next(line), next(line)))
        can_hold.append((int(num), bag))
        next(line)      # skips the "bag(s)[,|.]"
    return this_bag, can_hold


def number_of_bags(tree: dict, node: str) -> int:
    """
    Descends the ""tree"", adding up & multiplying the bags to give
    the total number of bags contained in `node`
    ---
    ## Example:
    ```python
    node == "red"
    tree["red"] == [(1, 'green'), (4, 'blue')]
    tree["green"] == []
    tree["blue"] == [(3, "pink")]
    tree["pink"] == []
    ```
    Working backwards (because recursion's easier to understand this way):
    - Pink holds no bags, return 0.
    - Blue contains 3 pink bags, each pink bag contains nothing, return 3.
    - Green holds no bags, return 0.
    - Red contains 5 + 1(green=0) + 4(blue=3) == 5+0+12 = 17 bags
    """
    can_hold = tree[node]       # Its children
    total_bags = 0              # The direct 1st level
    for n_bags, bag in can_hold:
        total_bags += n_bags + (n_bags * number_of_bags(tree, bag))  # If red holds 10 bags, and we have 3 reds...
    return total_bags


all_bags = dict()       # <ThisBag : Bags it directly contains>
with open(INPUT_FILE, 'r') as file:
    for line in file:
        this_bag, can_hold = parse_bag_instructions(line)
        all_bags[this_bag] = (can_hold)

# from pprint import pprint; pprint(all_bags);

print(number_of_bags(all_bags, ROOT_BAG))