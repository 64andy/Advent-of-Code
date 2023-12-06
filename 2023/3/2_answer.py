"""
Day 3.2 - Gear Ratios

Python 3.9+

Input:
  A 2D grid of numbers and symbols.
  If multiple digits are sequential, then it's one number
    e.g. "$.123+..4" has the numbers [123, 4]

Logic:
  A 'gear' is an asterisk symbol (*)
  If a gear is adjacent (vertically, horizontally, even diagonally)
    to *exactly two part numbers*, multiply those numbers together
    for their 'gear ratio'
  Note: Every number adjacent to a gear is already a 'part number',
    because asterisks are symbols
   

Output:
  Sum up every gear ratio
"""

import dataclasses
from pathlib import Path

p = Path(__file__).with_name("input")

# Vars
GEAR_SYMBOL_CHAR = '*'

@dataclasses.dataclass
class Number:
    num: int
    line_num: int
    start_pos: int
    end_pos: int

# Funcs
def extract_nums_from_line(line: str, line_num: int) -> list[Number]:
    numbers_in_line = []

    current_number_str = ''
    start_pos = 0
    is_reading_number = False  # True if we're currently reading a number
    for i, char in enumerate(line.strip()):
        is_digit = char.isdigit()
        if is_reading_number and is_digit:          # Continue reading
            current_number_str += char
        elif is_reading_number and not is_digit:    # Reached the end of current number
            num = Number(
                num=int(current_number_str),
                line_num=line_num,
                start_pos=start_pos,
                end_pos=i-1
            )
            numbers_in_line.append(num)
            current_number_str = ''
            is_reading_number = False
        elif not is_reading_number and is_digit:    # New number, start reading
            start_pos = i
            current_number_str += char
            is_reading_number = True
        elif not is_reading_number and not is_digit:# Flying over empty space
            pass
    
    # If we were reading a number when we ended, save it
    if is_reading_number:
        num = Number(
            num=int(current_number_str),
            line_num=line_num,
            start_pos=start_pos,
            end_pos=i
        )
        numbers_in_line.append(num)

    return numbers_in_line

def is_gear(char: str) -> bool:
    """
    Part 2 - We only care about numbers adjacent to gears
    """
    return (char == GEAR_SYMBOL_CHAR)

def is_gear_at_position(grid: list[str], i: int, j: int) -> bool:
    if 0 <= i < len(grid):
        if 0 <= j < len(grid[i]):
            char = grid[i][j]
            return is_gear(char)
    return False

def number_is_adjacent_to_gear(num: Number, grid: list[str]) -> bool:
    # We return numbers in the following order:
    # (Where * is `num`)
    # 3111114
    # 7*****8
    # 5222226
    
    # Step 1. Numbers above
    row = num.line_num - 1
    for col in range(num.start_pos-1, num.end_pos+1):
        if is_gear_at_position(grid, row, col):
            return True
    # Step 2. Numbers below
    row = num.line_num + 1
    for col in range(num.start_pos-1, num.end_pos+1):
        if is_gear_at_position(grid, row, col):
            return True
    # Step 3: Diagonals & sides
    return (
        is_gear_at_position(grid, num.line_num-1, num.start_pos-1)    # Top-left
        or is_gear_at_position(grid, num.line_num-1, num.end_pos+1)   # Top-right
        or is_gear_at_position(grid, num.line_num+1, num.start_pos-1) # Bottom-left
        or is_gear_at_position(grid, num.line_num+1, num.end_pos+1)   # Bottom-right
        or is_gear_at_position(grid, num.line_num, num.start_pos-1)   # Left
        or is_gear_at_position(grid, num.line_num, num.end_pos+1)     # Right
    )

def ranges_overlap(start_a, end_a, start_b, end_b) -> bool:
    return start_a <= end_b and end_a >= start_b

def find_adjacent_numbers(part_numbers: list[Number], i: int, j: int) -> list[Number]:
    return [num
            for num in part_numbers
            # Vertical check: Only numbers at most one row away are valid
            if (i-1 <= num.line_num <= i+1)
            # Horizontal check: Only numbers that overlap with the gear's boundary are valid
            and ranges_overlap(j-1, j+1, num.start_pos, num.end_pos)
            ]


def main():
    # We have to read the file multiple times, so save it
    with p.open('r') as file:
        grid = [line.rstrip() for line in file]
    
    # Extract all numbers from the grid
    all_numbers: list[Number] = []
    for line_num, line in enumerate(grid):
        nums_in_line = extract_nums_from_line(line, line_num)
        all_numbers.extend(nums_in_line)

    # Only keep the numbers adjacent to gears
    part_numbers = [number
                    for number in all_numbers
                    if number_is_adjacent_to_gear(number, grid)
                    ]
    
    # Remember all the gear positions
    gear_positions = [(i, j)
                      for i, row in enumerate(grid)
                        for j, char in enumerate(row)
                      if is_gear(char)]
    print("Gear positions:", gear_positions)

    # Check the gear ratios, and calculate the total
    total = 0
    for i, j in gear_positions:
        adjacent_nums = find_adjacent_numbers(part_numbers, i, j)
        if len(adjacent_nums) == 2:     # Ratios only work on exactly 2 numbers
            one, two = adjacent_nums
            total += (one.num * two.num)
    print("Total:", total)

if __name__ == "__main__":
    main()
