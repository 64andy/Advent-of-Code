"""
Day 2.1 - Cube Conundrum

Input:
  Each line has a list of 'views' into a bag of coloured cubes.
    Every line starts with "Game {id}:"
    Each view is separated by a semi-colon
    Every colour count inside a view is comma-separated
  Example: "Game 1: 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
    "Game 1:" - The row has an ID of 1
    "3 blue, 4 red;" - The first 'view' reveals 3 blues, 4 reds
    "1 red, 2 green, 6 blue;" - The second 'view'
    "2 green" - The final view


Logic:
  You have a bag containing an unknown number of red, green, and blue cubes.
  Each 'view' shows a subset of your bag's content.
  - 'Views' inform us that the bag contains *at least* those number of cubes
  The target number of colours are: 12 red, 13 green, 14 blue.
  A game is valid if your bag COULD contain EXACTLY that number of cubes.
  - This means no single view should show us MORE than these numbers

  Example:
    "Game 4: 14 blue, 4 red; 5 blue, 13 green" is valid, because no colour exceeds the targets
    "Game 5: 8 green, 22 red" is invalid, because "22 red" exceed the max of 12 reds

Output:
  The sum of every valid game's ID

"""

import dataclasses
from pathlib import Path
import re
from typing import Dict, List

p = Path(__file__).with_name("input")

# Vars
COLOUR_MAXIMUMS = {
    'red': 12,
    'green': 13,
    'blue': 14
}

GAME_REGEX = r"Game (\d+): (.*)"

@dataclasses.dataclass
class Game:
    id: int
    views: List[Dict[str, int]]

    @staticmethod
    def parse(game_str: str):
        game_id, view = re.match(GAME_REGEX, game_str.strip()).groups()
        # view is the full unparsed RHS e.g. "3 red, 4 blue; 5 green"
        views = list()
        views_str_list = view.split(';') # ["3 red, 4 blue", "5 green"]
        for view_str in views_str_list:
            pairs = dict()
            cube_pairs = view_str.split(', ') # ["3 red", "4 blue"]
            for pair_str in cube_pairs:
                count, colour = pair_str.split(maxsplit=1) # ("3", "red")
                pairs[colour] = int(count)
            views.append(pairs)
        
        return Game(id=int(game_id), views=views)

    def is_valid(self) -> bool:
        """
        A view is valid if no colour exceeds the limit.
        A game is valid if all views are valid.
        """
        return all(count <= COLOUR_MAXIMUMS[colour]             # The count is small enough
                        for view in self.views                  # Ensure every view is valid
                            for (colour, count) in view.items())# Ensure this view is valid
# Funcs
...


def main():
    total = 0
    with p.open('r') as file:
        for line in file:
            game = Game.parse(line)
            if game.is_valid():
                total += game.id
        print("Total:", total)

if __name__ == "__main__":
    main()
