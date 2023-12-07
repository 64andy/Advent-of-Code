"""
Day 4.1 - Scratchcards

Python 3.9+

Input:
  Each line represents a "card". It contains:
    - The word "Card" and its ID followed by a colon ("Card 11:")
    - n space-separated "winning numbers", followed by a pipe
    - m space-separated "your numbers"
  e.g. "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"

Logic:
  Having one of your numbers be a "winning number" is worth
  1 point. For every other matching number, double your points.
    e.g. 1 match => 1pt, 2 matches => 2pt, 3 matches => 4pt...

Output:
  Sum the point value of every card
"""

import dataclasses
from pathlib import Path


p = Path(__file__).with_name("input")

# Vars
@dataclasses.dataclass
class Card:
    card_id: int
    winning_nums: set[int]
    your_nums: set[int]

    @staticmethod
    def parse(line: str) -> 'Card':
        id_str, nums_str = line.strip().split(':') # ["Card (id)", "1 2 3 | 4 5 6"]
        card_id = int(id_str.removeprefix("Card "))

        winning_nums_str, your_nums_str = nums_str.split('|')
        winning_nums = [int(n) for n in winning_nums_str.split()]
        your_nums = [int(n) for n in your_nums_str.split()]

        assert len(winning_nums) == len(set(winning_nums)), f"{line!r} has duplicate elements"
        assert len(your_nums) == len(set(your_nums)), f"{line!r} has duplicate elements"
        return Card(card_id, set(winning_nums), set(your_nums))

    def calc_points(self) -> int:
        n_matching_numbers = len(self.winning_nums & self.your_nums)
        return point_value(n_matching_numbers)

# Funcs
def point_value(n_matches: int) -> int:
    if n_matches == 0:
        return 0
    return 2**(n_matches-1)

def main():
    with p.open('r') as file:
        cards = [Card.parse(line) for line in file]
    
    total = sum(card.calc_points() for card in cards)
    print("Total:", total)

if __name__ == "__main__":
    main()
