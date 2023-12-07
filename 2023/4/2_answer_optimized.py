"""
Day 4.2 - Scratchcards

Python 3.9+

Input:
  Each line represents a "card". It contains:
    - The word "Card" and its ID followed by a colon ("Card 11:")
    - n space-separated "winning numbers", followed by a pipe
    - m space-separated "your numbers"
  e.g. "Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53"

Logic:
  Your card is worth 1 point for each of your numbers that appears in the "winning numbers"
  For every point your card wins, you gain that amount of proceeding cards
    e.g. If card #4 has 3 points, you gain cards [#5, #6, #7]
  Notes:
  - The input won't make you win cards with invalid IDs
  - Cards WILL be calculated multiple times

Output:
  How many cards were processed in total?
    (This includes your original deck, plus each card they spawned)
"""

import dataclasses
from pathlib import Path


p = Path(__file__).with_name("input")

# Vars
@dataclasses.dataclass
class Card:
    id: int
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
        return Card(card_id, frozenset(winning_nums), frozenset(your_nums))

    def winning_ticket_ids(self) -> list[int]:
        """
        Returns the IDs of the cards you win
        e.g. If this card 12, and 3 of your numbers are winners, then
        you win cards [13, 14, 15]
        """
        n_winning_tickets = len(self.winning_nums & self.your_nums)
        return list(range(self.id+1, self.id+1+n_winning_tickets))


# Funcs
def calculate_number_of_children(deck: list[Card]) -> dict[int, int]:
    """
    Returns pairs of each card's ID to how many children the card has.
    """
    card_id_to_n_children = {}
    # Lets us index our results
    indexed = {card.id: card for card in deck}
    # We work backwards, more on this later...
    deck = sorted(deck, key=lambda c: c.id, reverse=True)

    # The total number of cards any given card will spawn is recursive.
    # e.g. card #1 spawns [card #2, card #3], and card #3 [spawns card #4], total=3.
    # Recursively, children_spawned(card) = sum(children_spawned(child) for child of card).
    # HOWEVER, if we remember how many children some card spawns, we can use that instead
    # of recalculating every time.
    # AND if we read the cards backwards, then each child spawned will be cards we've already
    # calculated.
    for card in deck:
        winning_cards = card.winning_ticket_ids()
        n_children = (
            len(winning_cards)
            + sum(card_id_to_n_children[winning_id]
                    for winning_id in winning_cards)
        )
        card_id_to_n_children[card.id] = n_children
    
    return card_id_to_n_children


def main():
    with p.open('r') as file:
        deck = [Card.parse(line) for line in file]
    
    # Lets the cards be indexed
    all_cards = calculate_number_of_children(deck)

    # We need to account for the original deck
    n_cards_read = len(deck)
    # Add up the number of children every card has
    n_cards_read += sum(all_cards.values())

    print("Total number of cards read:", n_cards_read)

if __name__ == "__main__":
    main()
