"""
Day 18.1: Snailfish.

'Snailfish numbers' are just binary trees, with ints as leafs

We 'add' these trees by making a new tree,
where the LHS is the old tree, and the RHS is what
we're adding.
e.g. `[3,4] + [6,7] => [[3,4], [6,7]]

However, after each add, it needs to be 'reduced':
- If any pair is @ depth=4, make it `explode`
- If any leaf >= 10, the leftmost number `splits`

They happen with this priority
(All explosions must happen before a split can)
Repeat until no changes can occur, then add the next number & go again.

What do these mean?
- Explode: Add its leafs to neighbours, then nullify itself:
  Add LHS to the nearest left num
  Add RHS to the nearest right num
  Then replace the exploded pair with `0`
  Example: `[[3, *[4, 5]*], 6] => [[7, 0], 11]`
  Note: If there's no number to its left/right
  (i.e. it's off the edge), don't add it.
  Also, trust that all exploded pairs have both leaf children.

- Split: Turn a too-large number into a pair:
  Divide it by 2, the LHS is round down, the RHS is round UP
  e.g. `12 => [6,6];   13 => [6,7];   14 => [7,7]`


After all this is done, you calculate the `magnitude` of the
final snailfish number, which is 3x the LHS + 2x the RHS recursively

Part 1 question: After adding all the numbers together
"""
from math import floor, ceil
from pathlib import Path
from typing import Optional
p = Path(__file__).with_name("input")


EXPLODE_THRESHOLD = 4
SPLIT_THRESHOLD = 10

DEBUG = False


class Direction(int):
    def __new__(cls, num):
        return super(Direction, cls).__new__(cls, num)

    def __repr__(self):
        return 'L' if self == 0 else 'R'

    def __invert__(self):
        return L if self == 1 else R


L = Direction(0)
R = Direction(1)


def log(*args, **kwargs):
    if DEBUG:
        print(*args, **kwargs)

# ===   Operations   ===


def reverse_enumerate(thing):
    num_iter = reversed(range(len(thing)))
    item_iter = reversed(thing)
    return zip(num_iter, item_iter)


def item_at_path(nums: list, path: tuple) -> "int | list":
    """
    Returns the item (tree or leaf) at the given path.
    """
    for direction in path:
        nums = nums[direction]
    return nums


def nearest_neighbour(nums: list, path: tuple, direction: int) -> Optional[tuple]:
    # Logic: If you want, say, the left neighbour; backtrack to the last
    # right turn you made, replace it with a left, then go hard right.
    # Vice versa for right turns, undo the last left, then go hard left.
    # 1. Backtrack
    for i, turn in reverse_enumerate(path):
        if turn != direction:
            # Undo the turn
            path = path[:i]
            path += (direction,)
            break
    else:
        # Reached the end of iteration, there is no neighbour number.
        return None

    # 2. Go hard in the other direction
    nums = item_at_path(nums, path)
    while not isinstance(nums, int):
        path += (~direction,)
        nums = nums[~direction]
    return path


def explode(nums: list, path: tuple):
    pair = item_at_path(nums, path)
    left_path = nearest_neighbour(nums, path, L)
    right_path = nearest_neighbour(nums, path, R)
    if left_path is not None:
        # Cut off the final step, because we need the parent
        # to actually change the value I love Python :)
        which_kid = left_path[-1]
        parent = item_at_path(nums, left_path[:-1])
        parent[which_kid] += pair[L]
    if right_path is not None:
        which_kid = right_path[-1]
        parent = item_at_path(nums, right_path[:-1])
        parent[which_kid] += pair[R]
    # Then replace with 0
    pair_parent = item_at_path(nums, path[:-1])
    which_kid = path[-1]
    pair_parent[which_kid] = 0


def split(nums: list, path: tuple):
    num = item_at_path(nums, path)
    lhs = floor(num/2)
    rhs = ceil(num/2)
    # Get parent because immutable references :)
    which_kid = path[-1]
    parent = item_at_path(nums, path[:-1])
    parent[which_kid] = [lhs, rhs]


# ===   Functions for trying and repeating operations   ===

def try_explode(nums: list, path: tuple = ()) -> bool:
    """
    Recursively creeps through the tree in-order,
    trying to do an explode action.

    If it succeeds to do any action, it'll
    immediately halt and return True.
    If it creeps the entire tree without doing
    anything, return False.
    """
    pair = item_at_path(nums, path)
    # Recusive basecase - Can't explode a leaf
    if isinstance(pair, int):
        return False
    if len(path) == EXPLODE_THRESHOLD:
        explode(nums, path)
        log("After explode:", nums)
        return True
    # Recursion baybeeee
    go_left = path + (L,)
    go_right = path + (R,)
    if try_explode(nums, go_left):
        return True
    if try_explode(nums, go_right):
        return True
    return False


def try_split(nums: list, path: tuple = ()) -> bool:
    """
    Recursively creeps through the tree in-order,
    trying to do a split actions.

    If it succeeds, it immediately returns True,
    if it fails, it returns False.
    """
    item = item_at_path(nums, path)
    if isinstance(item, int):
        if item >= SPLIT_THRESHOLD:
            split(nums, path)
            log("After split:", nums)
            return True
        else:
            return False
    go_left = path + (L,)
    go_right = path + (R,)
    if try_split(nums, go_left):
        return True
    if try_split(nums, go_right):
        return True
    return False


def snailfish_reduce(pair: list):
    """
    Reduces a snailfish tree by repeatedly exploding and
    splitting. Halts when no more changes are possible.
    """
    while try_explode(pair) or try_split(pair):
        pass


def magnitude(pair) -> int:
    """
    Returns the 'magnitude' of a snailfish number.
    The magnitude is 3x the LHS + 2x the RHS, recusively.
    """
    if isinstance(pair, int):
        return pair
    return 3*magnitude(pair[L]) + 2*magnitude(pair[R])


if __name__ == "__main__":
    with p.open('r') as file:
        snailfish_numbers = [eval(line) for line in file]
    fish_it = iter(snailfish_numbers)

    current_pair = next(fish_it)
    for to_add in fish_it:
        log("Adding", to_add, ...)
        current_pair = [current_pair, to_add]
        snailfish_reduce(current_pair)
        log("===")

    print("Final snailfish number:", current_pair)
    print("Magnitude:", magnitude(current_pair))
