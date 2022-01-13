"""
Day 17.2: Trick Shot

Ok so, you start at (0, 0), and are given a 2D target area
(target area: x=244..303, y=-91..-54)

You shoot a shot with an initial x and y velocity, and every tick
they move in that direction.
x: Each tick, x-velocity slows by 1 towards 0 (eventually stopping)
y: Each tick, y-velocity decreases by 1 (rises, stops, then drops)

A 'valid throw' is one where the shot is inside the target area
at any point of its arc.
Note: If a shot is too fast, it can be on one side of the target
in one tick, and the other in the next. IRL it would intersect,
but that's consider a miss here.

Part 2 question: How many throws are valid?
"""

import re
from math import inf
from pathlib import Path
from typing import Optional, Tuple
from time import perf_counter
p = Path(__file__).with_name("input")

# Awful code to read the numbers from the file
pattern = r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)"
with p.open('r') as file:
    m = re.match(pattern, file.read().strip())
    x_lo, x_hi, y_lo, y_hi = map(int, m.groups())
    x_lo, x_hi = (x_lo, x_hi) if x_lo < x_hi else (x_hi, x_lo)
    y_lo, y_hi = (y_lo, y_hi) if y_lo < y_hi else (y_hi, y_lo)


"""
Now we need to write actual code, oh joy.

So what can we do?
We can simulate all possible throws, as said in the last answer,
it's a finite list.
The furthest we can throw on the x-axis is the target's x limit,
any harder and we overshoot.
The highest we can throw on the y-axis is the target's y limit,
any harder it'll fall too fast and fly through it.
"""


def overshot_x(vel, pos, lo, hi) -> bool:
    """
    Returns True if we've overshot the target on the x-axis
    """
    # If we're moving left (-vel), are we beyond the boundary?
    if vel < 0:
        return pos < lo
    # If we're moving right (+vel)
    elif vel > 0:
        return pos > hi
    # If we've stopped moving, are we outside the box?
    else:
        return not (lo <= pos <= hi)


def overshot_y(vel, pos, lo, _hi) -> bool:
    """
    Returns True if we've overshot the target on the y-axis
    """
    # If we're moving down (-vel), are we beyond the box?
    if vel <= 0:
        return pos < lo
    # If we're moving up (+vel), do nothing, we might fall
    # down into the box in a few stepFs
    else:
        return False


def tend_towards_zero(n) -> int:
    """
    Adds/subtracts 1 from n to move it to zero
    e.g. -3 => -2;   3 => 2;   0 => 0
    """
    if abs(n) <= 1:     # In case of floats
        return 0
    elif n > 0:
        return n-1
    else:
        return n+1


def x_shot_intersects(x_vel, left, right) -> Optional[Tuple[int, int]]:
    """
    Returns a 2-tuple of the inclusive start-end ticks where
    a given x-velocity is inside the target box.

    2nd value can be math.inf if it loses momentum inside the area
    If it never intersects, returns None.
    """
    x = 0
    first = last = None
    tick = 0
    while x_vel != 0 and not overshot_x(x_vel, x, left, right):
        if left <= x <= right:
            if first is None:
                first = last = tick
            else:
                last = tick
        tick += 1
        x += x_vel
        x_vel = tend_towards_zero(x_vel)
    # Final check: If you're still inside the boundary, you'll
    # spend forever in it.
    if left <= x <= right:
        last = inf
    if first is None:
        return None
    else:
        return (first, last)


def y_shot_intersects(y_vel, low, high) -> list:
    """
    Returns a list of the tick times the y-value is inside
    the target area.
    If it doesn't intersect, returns an empty list.

    NOTE: This returns a list, while the x-axis version returns
    a 2-tuple range. This is because the parabolic nature of the
    y-axis throw means it can intersect on the way up, leave,
    then re-intersect on the way down i.e. it's not continuous.
    Whereas the x-axis version is continuous, and maybe infinite.
    """
    y = 0
    times = []
    tick = 0
    while not overshot_y(y_vel, y, low, high):
        if low <= y <= high:
            times.append(tick)
        tick += 1
        y += y_vel
        y_vel -= 1
    return times


def shot_intersects(x_vel, y_vel, left, right, low, high) -> bool:
    x = 0
    y = 0
    while not overshot_x(x_vel, x, left, right) \
            and not overshot_y(y_vel, y, low, high):
        if (left <= x <= right) and (low <= y <= high):
            return True
        x += x_vel
        y += y_vel
        x_vel = tend_towards_zero(x_vel)
        y_vel -= 1
    return False


print(shot_intersects(6, 0, 20, 30, -10, -5))


valid_shots = set()
# The leftmost shot hits the farleft if farleft < 0,
# or is simply dropped if farleft > 0
start_x = min(0, x_lo)
# The rightmost shot either hits the far right if farright > 0,
# or is dropped if < 0
end_x = max(x_hi+1, 0)
# Lowest you can throw is just above where it'd instantly
# fly below the lower boundary
start_y = y_lo
# Highest you can throw, as shown by part 1, is a speed
# where the ascent/descent doesn't instantly fly past it.
# a.k.a whichever boundary is furthest from 0.
# The abs-1 is because it speeds up by -1 when going
# from   +ve -> 0   to   0 -> -ve
end_y = 1 + max(
    y_hi if y_hi >= 0 else abs(y_hi) - 1,
    y_lo if y_lo >= 0 else abs(y_lo) - 1,
)

start_time = perf_counter()

for x in range(start_x, end_x):
    for y in range(start_y, end_y):
        if shot_intersects(x, y, x_lo, x_hi, y_lo, y_hi):
            valid_shots.add((x, y))

end_time = perf_counter()
# print(valid_shots)
print(f"{len(valid_shots) = }")
print(f"Took {end_time-start_time:.3f}s")


"""
Possible improvement:

This is really quick because the target is small and fairly close,
however doing a full simulation for every possible x,y combo is
very wasteful.

Alternative idea: Instead of doing O(x*y) simulations, do O(x+y).
We simulate every throw on the x-axis, and record what ticks it's
inside the target's x-boundary. Same thing with the y-axis.
If an x/y throw never reaches the target, we can prune it.

Because the x and y velocity are independent of each other,
we can do a much smaller and easier O(x*y) comparison of
pre-computed intersection times.

Example: Let's say an x=3 throw is inside the target between
ticks [3, inf), and a y=0 throw between ticks [5, 6].
Because x is inside the target at the same time as y, we can
say that they intersect.
"""

x_times = {}
y_times = {}
valid_shots.clear()

# Include the preprocessing
start_time = perf_counter()

for x in range(start_x, end_x):
    intersect_times = x_shot_intersects(x, x_lo, x_hi)
    if intersect_times is not None:
        x_times[x] = intersect_times

for y in range(start_y, end_y):
    intersect_times = y_shot_intersects(y, y_lo, y_hi)
    if len(intersect_times) > 0:
        y_times[y] = intersect_times

for x, (start, end) in x_times.items():
    for y, times in y_times.items():
        if any(start <= t <= end for t in times):
            valid_shots.add((x, y))

end_time = perf_counter()
print("x axis:")
print(f"- We've gone from {end_x-start_x-1} entries to {len(x_times)}")
print("y axis:")
print(f"- We've gone from {end_x-start_y-1} entries to {len(y_times)}")

print(f"{len(valid_shots) = }")
print(f"Took {end_time-start_time:.3f}s")