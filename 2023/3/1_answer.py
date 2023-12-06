"""
Day 3.1 - Gear Ratios

Input:
  A 2D grid of numbers and symbols.
  If multiple digits are sequential, then it's one number
    e.g. "$.123+..4" has the numbers [123, 4]

Logic:
  A 'symbol' is any charater that's not a period, and not a number
    e.g. "$.123+..4" has the symbols [$, +]
  If a number is adjacent (vertically, horizontally, even diagonally)
    to a symbol, it's a 'part number'

Output:
  Sum up every part number
    (That is, every number adjacent to a symbol)
"""

import dataclasses
from pathlib import Path

p = Path(__file__).with_name("input")

# Vars
NON_SYMBOL_CHAR = '.'

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

def is_symbol(char: str) -> bool:
    """
    If it's not a number, and it's not a dot, it's a symbol
    """
    return (char != NON_SYMBOL_CHAR and not char.isdigit())

def is_symbol_at_position(grid: list[str], i: int, j: int) -> bool:
    if 0 <= i < len(grid):
        if 0 <= j < len(grid[i]):
            char = grid[i][j]
            return is_symbol(char)
    return False

def number_is_adjacent_to_symbol(num: Number, grid: list[str]) -> bool:
    # We return numbers in the following order:
    # (Where * is `num`)
    # 3111114
    # 7*****8
    # 5222226
    
    # Step 1. Numbers above
    row = num.line_num - 1
    for col in range(num.start_pos-1, num.end_pos+1):
        if is_symbol_at_position(grid, row, col):
            return True
    # Step 2. Numbers below
    row = num.line_num + 1
    for col in range(num.start_pos-1, num.end_pos+1):
        if is_symbol_at_position(grid, row, col):
            return True
    # Step 3: Diagonals & sides
    return (
        is_symbol_at_position(grid, num.line_num-1, num.start_pos-1)    # Top-left
        or is_symbol_at_position(grid, num.line_num-1, num.end_pos+1)   # Top-right
        or is_symbol_at_position(grid, num.line_num+1, num.start_pos-1) # Bottom-left
        or is_symbol_at_position(grid, num.line_num+1, num.end_pos+1)   # Bottom-right
        or is_symbol_at_position(grid, num.line_num, num.start_pos-1)   # Left
        or is_symbol_at_position(grid, num.line_num, num.end_pos+1)     # Right
    )


def main():
    with p.open('r') as file:       # We have to read the file multiple times, so save it
        grid = [line.rstrip() for line in file]
    all_numbers: list[Number] = []

    for line_num, line in enumerate(grid):  # Extract numbers from it
        nums_in_line = extract_nums_from_line(line, line_num)
        all_numbers.extend(nums_in_line)

    total = 0
    for number in all_numbers:
        if number_is_adjacent_to_symbol(number, grid):
            print(number, "is a part!")
            total += number.num
    print("Total:", total)

if __name__ == "__main__":
    main()
