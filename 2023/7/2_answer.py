"""
Day 7.2 - Camel Cards

Python 3.9+

Input:
  Each line contains a deck of 5 cards, and its bet.
  e.g. "32T3K 765"

Logic:
  Each deck can have different 'types' according to poker rules.
  In order from most-to-least powerful:
  - Five of a Kind  (Every card is identical : 11111)
  - Four of a Kind  (4 cards are identical   : 1111K)
  - Full House      (3+2 are identical       : 555QQ)
  - Three of a Kind (3 are identical         : 111KQ)
  - Two Pair        (2+2 are identical       : KKQQ1)
  - One Pair        (2 are identical         : KK123)
  - High Card       (Every card is different : 2468T)
  However, 'J' is a wildcard. They can be used to create the
  most powerful type given the other cards

  In additions, decks are powerful depending on its cards.
  In order from least-to-most powerful:
    J, 2, 3, 4, 5, 6, 7, 8, 9, T, Q, K, A
    Part 2 specifies that Jokers are now the weakest

  To compare two decks, you first compare their 'type'.
    If it has a lower type then it's less than the other.
  If they're the same type, you compare its cards in-order.
    You check if your first card is less than their first card,
    if they're the same compare the second, repeat.
  
  Example:
    66223 < 23232, because TwoPair < FullHouse
    2AAAA < 33332, because they're both FourOfAKind, but on
      the first card, 3 is stronger than 2
    3333T < 3333K, same as above, however T < K (ten < king)

Output:
  Out of every deck, the weakest has a rank=1, next has rank=2,
    and so on.
  Print the sum of each deck's bet*ranking 
"""

import enum
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

p = Path(__file__).with_name("input")

# Vars
# All the cards of the deck, ordered from least-to-most powerful
WILDCARD = 'J'

ALL_CARDS = {
    WILDCARD: -1,    # Part 2, Jokers are now the weakest card
    '2': 2,
    '3': 3,
    '4': 4,
    '5': 5,
    '6': 6,
    '7': 7,
    '8': 8,
    '9': 9,
    'T': 10,
    'Q': 12,
    'K': 13,
    'A': 99,    # The highest card because aces trump all
}

# Classes
class Hand(enum.IntEnum):
    """
    Represents the different hands in this card game,
    ordered by their strength
    """
    FIVE_OF_A_KIND = 6
    FOUR_OF_A_KIND = 5
    FULL_HOUSE = 4
    THREE_OF_A_KIND = 3
    TWO_PAIR = 2
    ONE_PAIR = 1
    HIGH_CARD = 0
    
    @staticmethod
    def from_deck(deck: str) -> 'Hand':
        assert len(deck) == 5, "Only works if given 5 cards"
        # Look at the deck without wildcards
        n_wildcards = deck.count(WILDCARD)
        deck = deck.replace(WILDCARD, '')
        # Reduce the deck into how many duplicates there are.
        # e.g. JJJQQ => [3,2], JJQQ3 => [2,2,1]
        card_counts = sorted(Counter(deck).values(), reverse=True)

        # If there's 5 or 4 wildcards, you can always make 5-of-a-kind
        if n_wildcards in (5, 4):       # JJJJJ or JJJJQ
            return Hand.FIVE_OF_A_KIND
        # If there's 3 wildcards, you can make either 4-of-a-kind or 5-of-a-kind
        if n_wildcards == 3:
            if card_counts[0] == 2:     # JJJ55
                return Hand.FIVE_OF_A_KIND
            return Hand.FOUR_OF_A_KIND  # JJJ78
        # If there's 2 wildcards, you can make 3-of-a-kind or higher
        # (No Full House since any situation where one's possible is one where
        #  you're better off doing a 4-of-a-kind)
        if n_wildcards == 2:
            if card_counts[0] == 3:     # JJ999
                return Hand.FIVE_OF_A_KIND
            if card_counts[0] == 2:     # JJ993
                return Hand.FOUR_OF_A_KIND
            if card_counts[0] == 1:     # JJ234
                return Hand.THREE_OF_A_KIND
        # If there's 1 wildcard, simply brute-force every combination
        if n_wildcards == 1:
            best = Hand.HIGH_CARD
            for n in range(len(card_counts)):
                new_counts = card_counts.copy()
                new_counts[n] += 1  # Act as if you put the wildcard into that count
                new_counts.sort(reverse=True)
                best = max(best, Hand._calculate_from_deck(new_counts))
            return best
        
        # If there's no wildcards, calculate it as-is
        return Hand._calculate_from_deck(card_counts)

    @staticmethod
    def _calculate_from_deck(card_counts: list[int]) -> 'Hand':
        # All the same => Five of a kind
        if card_counts[0] == 5:
            return Hand.FIVE_OF_A_KIND
        # Four the same => Four of a kind
        elif card_counts[0] == 4:
            return Hand.FOUR_OF_A_KIND
        # 3 the same & 2 the same => Full House
        elif card_counts[0] == 3 and card_counts[1] == 2:
            return Hand.FULL_HOUSE
        # Just 3 the same => 3 of a kind
        elif card_counts[0] == 3:
            return Hand.THREE_OF_A_KIND
        # Two 2-pairs => Two pair
        elif card_counts[0] == 2 and card_counts[1] == 2:
            return Hand.TWO_PAIR
        # A single pair => One
        elif card_counts[0] == 2:
            return Hand.ONE_PAIR
        # All cards are different
        else:
            return Hand.HIGH_CARD


        

@dataclass
class Play:
    # The 'type' of the hand (pair, full house, etc.)
    win_type: Hand
    # The "strength" of each card
    deck: tuple[int, ...]
    bet: int

    def __lt__(self, other: 'Play') -> bool:
        """
        Lets us compare plays against each other, so
        we know their strength
        """
        # Firstly, compare on win_type
        if self.win_type != other.win_type:
            return self.win_type < other.win_type
        # If they're the same type, by their card
        # strength in-order
        return self.deck < other.deck
    
    @staticmethod
    def parse(line: str) -> 'Play':
        cards, bet = line.split(maxsplit=1)
        return Play(
            win_type=Hand.from_deck(cards),
            deck=tuple(ALL_CARDS[card] for card in cards),
            bet=int(bet),
        )

# Funcs
...


# =====

def main():
    with p.open('r') as file:
        all_plays = sorted(Play.parse(line) for line in file)
    total_winnings = sum(
        play.bet * rank
        for rank, play in enumerate(all_plays, start=1)
    )
    print(total_winnings)

if __name__ == "__main__":
    main()
