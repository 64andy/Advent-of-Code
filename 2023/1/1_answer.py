"""
Day 1.1 - Trebuchet?!

Input:
  Each line is a string of alphanumeric characters

Logic:
  Combine the first digit, and the last digit,
  to form a two-digit number.
  e.g. `2B loves 9S` -> 29


Output:
  The sum of every line's 2-digit number
"""

from pathlib import Path
p = Path(__file__).with_name("test_input")

# Vars
total = 0

# Funcs
def extract_number(s: str) -> int:
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
