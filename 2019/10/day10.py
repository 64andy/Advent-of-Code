FILENAME = "day10test.in"

from collections import defaultdict

def part1(nums: list) -> int:
    diff = defaultdict(int)
    for i in range(0, len(nums)-1):
        delta = nums[i+1] - nums[i]
        diff[delta] += 1
    return diff[3] * diff[1]


def part2(nums: list) -> int:
    #! NOT WORKING
    """
    Problem: How many possible combinations are there of numbers, given
    that any number must be either 1, 2, or 3 greater than the one
    preceeding it e.g. [1, 2, 4, 6, 7, 10]
    ---
    Algorithm: nums is already sorted, so just recurse through every
    possible combination where the next number's within 3 of your current
    number. Once you reach the end of the list, that counts as 1, total the 1s
    and that's the number of paths
    """
    def _n_possible_combos(i: int) -> int:
        j = 0
        n_combos = 0
        if i >= len(nums):  # End of the line
            return 1
        while (i+j) < len(nums) and (nums[i+j] - nums[i]) <= 3:
            n_combos += _n_possible_combos(i+1)
            j += 1
        return n_combos
    return _n_possible_combos(0)


def main():
    with open(FILENAME) as file:
        nums = [int(line) for line in file]
        nums.append(0)  # Voltage starts at 0
        nums.sort()
        nums.append(nums[-1]+3) # Ends at the highest voltage + 3
    print("Part 1:", part1(nums))
    print("Part 2:", part2(nums))

if __name__ == "__main__":
    main()
    