"""
Day 9.1 - Mirage Maintenance

Python 3.9+

Input:
  Each line contains a sequence of integer number

Logic:
  You need to calculate the next number in the sequence.
  This value can be found by calculating the difference between
    adjacent numbers, then repeating the process on the differences
    until every value is 0, then working back up.

  Example:
    Original: 1   3   6   10  15
    Delta(1):   2   3   4   5
    Delta(2):     1   1   1
    Delta(3):       0   0   # All zeroes, stop

    Calculate the new numbers:
    Delta(3):       0   0  *0*          # Add a 0 to the end
    Delta(2):     1   1   1  *1*        # 0 + 1 = 1
    Delta(1):   2   3   4   5  *6*      # 1 + 5 = 6
    Original: 1   3   6   10  15 *21*   # 6 + 15 = *21* !!!
      Therefore, the next number in the sequence is 21

Output:
  Print the sum of every sequence's "next" value.
"""

import dataclasses
from pathlib import Path
from typing import TextIO


p = Path(__file__).with_name("input")

# Vars
...

# Classes
@dataclasses.dataclass
class ParsedFile:
    sequences: list[list[int]]
    
    @staticmethod
    def parse(file: TextIO) -> 'ParsedFile':
        sequences = [[int(num) for num in line.strip().split()]
                     for line in file]
        return ParsedFile(sequences)

# Funcs
def sliding_window(seq: list[int]):
    for i in range(len(seq)-1):
        yield (seq[i], seq[i+1])

def calculate_difference(seq: list[int]) -> list[int]:
    return [b-a for a,b in sliding_window(seq)]

def predict_next_number(seq: list[int]) -> int:
    """
    Recursively tries to guess the next number
    """
    # Base Case
    print(seq)
    if all(num == 0 for num in seq):
        return 0
    # Calculate the differences
    differences = calculate_difference(seq)
    return seq[-1] + predict_next_number(differences)


# =====

def main():
    with p.open('r') as file:
        parsed_file = ParsedFile.parse(file)

    total = 0
    for line in parsed_file.sequences:
        val = predict_next_number(line)
        total += val
        print("Next value:", line, "=>", val)
    
    print()
    print("Total:", total)
    

if __name__ == "__main__":
    main()
