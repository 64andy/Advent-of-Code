"""
Day 2.2 - Cube Conundrum

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
  We want to know what the minimum possible number of each colour is in each bag

  Example:
    "Game 4: 14 blue, 4 red; 5 blue, 13 green" contains at minimum 14 blues, 13 greens, and 4 reds

Output:
  The sum of every game's (min_red * min_green * min_blue)

"""

import dataclasses
from pathlib import Path
import re
from typing import Dict

p = Path(__file__).with_name("input")

# Vars
GAME_REGEX = r"Game (\d+): (.*)"

@dataclasses.dataclass
class Game:
    id: int
    min_colours: Dict[str, int]

    @staticmethod
    def parse(game_str: str):
        game_id, view = re.match(GAME_REGEX, game_str.strip()).groups()
        # view is the full unparsed RHS e.g. "3 red, 4 blue; 5 green"
        min_colours = {
            'red': 0,
            'green': 0,
            'blue': 0
        }
        views_str_list = view.split(';') # ["3 red, 4 blue", "5 green"]
        for view_str in views_str_list:
            cube_pairs = view_str.split(', ') # ["3 red", "4 blue"]
            for pair_str in cube_pairs:
                count, colour = pair_str.split(maxsplit=1) # ("3", "red")
                count = int(count)
                min_colours[colour] = max(count, min_colours[colour])
        
        return Game(id=int(game_id), min_colours=min_colours)

    def product_of_mins(self) -> int:
        return (
            self.min_colours['red']
            * self.min_colours['green']
            * self.min_colours['blue']
        )
    
# Funcs
...


def main():
    total = 0
    with p.open('r') as file:
        for line in file:
            game = Game.parse(line)
            total += game.product_of_mins()
        print("Total:", total)

if __name__ == "__main__":
    main()
