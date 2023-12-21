"""
Day 9.1 - Mirage Maintenance

Python 3.9+

Input:
  Each line contains a sequence of integer number

Logic:
  You need to calculate the preceeding number in the sequence.
  This value can be found by calculating the difference between
    adjacent numbers, then repeating the process on the differences
    until every value is 0, then working back up.

  Example:
    Original: 10  13  16  21  30  45
    Delta(1):   3   3   5   9  15
    Delta(2):     0   2   4   6
    Delta(3):       2   2   2
    Delta(4):         0   0

    Calculate the new numbers:
    Delta(4):        *0*   0   0            # Add a 0
    Delta(3):      *2*  2   2   2           # 2 - 0 = 2
    Delta(2):   *-2*  0   2   4   6         # 0 - 2 = -2
    Delta(1):  *5*   3   3   5   9  15      # 3 - (-2) = 5
    Original:*5*  10  13  16  21  30  45    # 10 - 5 = *5* !!!
      Therefore, the preceeding number in the sequence is 5

Output:
  Print the sum of every sequence's "preceeding" value.
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

def predict_previous_number(seq: list[int]) -> int:
    """
    Recursively tries to guess the preceeding number
    """
    # Base Case
    print(seq)
    if all(num == 0 for num in seq):
        return 0
    # Calculate the differences
    differences = calculate_difference(seq)
    return seq[0] - predict_previous_number(differences)


# =====

def main():
    with p.open('r') as file:
        parsed_file = ParsedFile.parse(file)

    total = 0
    for line in parsed_file.sequences:
        val = predict_previous_number(line)
        total += val
        print("Previous value:", val, "=>", line)
    
    print()
    print("Total:", total)
    

if __name__ == "__main__":
    main()
