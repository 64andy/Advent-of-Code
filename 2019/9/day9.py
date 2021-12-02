FILENAME = "day9.in"

def part1(nums: list) -> int:
    """
    Specifications: You view the numbers as a length-25 sliding window.
    Every number you find (excluding the first 25) must be the sum of 
    any 2 numbers in this window.
    ---
    Algorithm logic: if 4 + x = 6 then 6 - 4 = x.
    If we want to check 6, loop through each value in the window (i)
    to see if (6-i) is in the window.
    ---
    Efficiency: (Check each number) *  (For each in window) * (List contains)
    = O(n) * O(n) * O(n)
    = O(n^2), which is the same as an easier "try every combination" solution,
    but who cares I do what I want
    """
    WINDOW_SIZE = 25
    for i in range(WINDOW_SIZE, len(nums)):
        window = nums[i-WINDOW_SIZE:i]
        to_check = nums[i]
        for n in window:
            if (to_check - n) in window:
                break
        else:   # Didn't break
            return to_check


def part2(nums: list, broken_num: int) -> (int, int):
    """
    Specification: Find a continuous length of numbers which sum up to broken_num
    ---
    Algorithm logic: Starting at i, keeping adding consecutive numbers until either
    the sum equals broken_num (success & return nums), or the sum over-runs (start
    again from i+1)
    """
    for i in range(len(nums)):
        running_total = 0
        for j, num in enumerate(nums[i:], start=i):
            running_total += num
            if running_total == broken_num:
                return i, j
            if running_total > broken_num:
                break


def main():
    with open(FILENAME, 'r') as file:
        global nums
        nums = [int(line) for line in file]
    broken_num = part1(nums)
    print(broken_num)
    i, j =part2(nums, broken_num)
    window = nums[i:j+1]
    print(i, j)
    print(window)
    print(sum(window))
    print(min(window), max(window))

if __name__ == "__main__":
    main()