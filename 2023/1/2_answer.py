"""
Day 1.2 - Trebuchet?!

Input:
  Each line is a string of alphanumeric characters

Logic:
  Combine the first digit, and the last digit,
  to form a two-digit number.
  e.g. `2B loves 9S` -> 29
        ^        ^
  
  PART 2 UPDATE: The spelled out digits now count as digits
  e.g. "2B loves nines"
        ^        ^^^^


Output:
  The sum of every line's 2-digit number
"""

from pathlib import Path
from operator import lt, gt
p = Path(__file__).with_name("input")

# Vars
total = 0

DIGIT_NAMES = [
    ("one",    '1'),
    ("two",    '2'),
    ("three",  '3'),
    ("four",   '4'),
    ("five",   '5'),
    ("six",    '6'),
    ("seven",  '7'),
    ("eight",  '8'),
    ("nine",   '9'),
]



# Funcs
def convert_spelt_number_to_digit(s: str) -> str:
    """
    This converts the first and last spelt digits into their numerical form
    """
    # Instead of duplicating the code, just change the required methods.
    # Note from future self: Why didn't you just duplicate the first/last code
    # :(
    funcs = [
        (str.find, lt),   # Check for the first occurance
        (str.rfind, gt)   # Check for the last occurance
    ]
    for search_func, cmp_func in funcs:
        target_digit = None
        target_digit_pos = None
        for spelt, digit in DIGIT_NAMES:
            pos = search_func(s, spelt)
            if pos == -1: continue
            # Earlier if first, later if last
            if target_digit is None or cmp_func(pos, target_digit_pos):
                target_digit_pos = pos
                target_digit = digit
        # If there is no spelt digit, just return
        if target_digit is None: return s
        # Insert substring
        s = s[:target_digit_pos] + target_digit + s[target_digit_pos:]

    return s

def extract_number(s: str) -> int:
    s = convert_spelt_number_to_digit(s)
    all_nums = [num
                for num in s
                if num.isdigit()]
    first_number = all_nums[0]
    last_number = all_nums[-1]
    return int(first_number + last_number)

    


def main():
    global total
    with p.open('r') as file:
        for line in file:
            calibration_number = extract_number(line)
            print(calibration_number)
            total += calibration_number
    
    print("Total:", total)

if __name__ == "__main__":
    main()
