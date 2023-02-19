"""
Day 6.1 - Tuning Trouble

Input:
A line of varying letters (test_input has multiple for testing)

Logic:
The data has a `start-of-packet marker`, which is the first point
  where the 4 previous letters all have different letters
  e.g. mjqjpqmgbljsphdztnvjfqwrcgsmlb
          ---^ = 7th character

Output:
Return the index of said marker
"""

from pathlib import Path
p = Path(__file__).with_name("input")

# Vars
WINDOW_SIZE = 4

# Funcs
def contains_repeat_elements(s):
    return len(s) != len(set(s))

def main():
    with p.open('r') as file:
        for (line_num, line) in enumerate(file, start=1):
            for i in range(WINDOW_SIZE, len(line)):
                window = line[i-WINDOW_SIZE:i]
                if not contains_repeat_elements(window):
                    break
            print("Line num:", line_num, "| Marker location:", i)

if __name__ == "__main__":
    main()
