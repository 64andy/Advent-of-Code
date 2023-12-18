"""
Day 6.1 - Wait For It

Python 3.9+

Input:
  Two lines, with each column representing a race.
  1. Time: how much time you have to beat the race
  2. Distance: how far you must travel to win
    Example:
    Time:      7  15   30
    Distance:  9  40  200
  (Time is in seconds, distance is in metres. This deviates from the
   original 'ms' and 'mm' units but it's easier this way)

Logic:
  To win, you must travel the given distance in the given time.
  Each race has two stages:
    1. Charging up. For every second at the start of the race you
       spend "charging up", you store 1 m/s
    2. Letting go. You move at your stored velocity for the remaining time.
       The trick is balancing the speed. Charge too little and you're not fast enough.
       Too much and you won't have enough remaining time to pass the line.
  Example:
    You have 7s to move further than 9m.
      If you charge for 0s, you'll move [0m*(7-0)s] = 0m, not far enough
      If you charge for 1s, you'll move [1m*(7-1)s] = 6m, not far enough
      If you charge for 2s, you'll move [2m*(7-2)s] = 10m, you win!
      If you charge for 3s, you'll move [3m*(7-3)s] = 12m, you win!
      If you charge for 4s, you'll move [4m*(7-4)s] = 12m, you win!
      If you charge for 5s, you'll move [5m*(7-5)s] = 10m, you win!
      If you charge for 6s, you'll move [6m*(7-6)s] = 6m, not far enough
      If you charge for 7s, you'll move [7m*(7-7)s] = 0m, not far enough
    
Output:
  For each race, count up how many ways there are to win.
  Print the product of every race's "win count"
"""

import math
from dataclasses import dataclass
from pathlib import Path

p = Path(__file__).with_name("input")

# Vars
...

# Classes
@dataclass
class RaceData:
    time: int
    distance: int

# Funcs
def parse_file(file_content: str) -> list[RaceData]:
    time_str, dist_str = file_content.split("\n", maxsplit=1)
    time_str = time_str.split(":")[1]
    dist_str = dist_str.split(":")[1]
    times = [int(n) for n in time_str.strip().split()]
    dists = [int(n) for n in dist_str.strip().split()]
    return [RaceData(t, d) for (t,d) in zip(times, dists)]

def number_of_ways_to_win(race: RaceData) -> int:
    # To maximise distance, you'll need to release in the
    # middle of your time frame
    mid_time = race.time / 2
    max_dist = mid_time * mid_time
    # If your maximum possible is 25, but you need to beat 20,
    # you have 4m of leeway
    # (25-20-1 = 4, the -1 is because you need to go at least 1m further to win)
    # So, you have sqrt(4)=2s of give before & after the midpoint to get fast enough
    leeway = max_dist - race.distance - 1
    leeway = math.sqrt(leeway)
    # Round towards the midpoint
    lower_end = math.ceil(mid_time-leeway)
    upper_end = math.floor(mid_time+leeway)
    return upper_end-lower_end + 1  # +1 because upper_end is inclusive
    


# =====

def main():
    with p.open('r') as file:
        all_races = parse_file(file.read())
    
    product = 1
    for race in all_races:
        ret = number_of_ways_to_win(race)
        print(ret)
        product *= ret
    
    print("Product:", product)
    

if __name__ == "__main__":
    main()
