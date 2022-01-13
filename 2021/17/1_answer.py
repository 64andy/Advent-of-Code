"""
Day 17.1: Trick Shot

THIS IS MOSTLY AN EXPLANATION, NOT A PROGRAM

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

Part 1 question: There is a throw with the highest possible
y-velocity. What's the highest point in this throw's arc?
"""

import re
from pathlib import Path
p = Path(__file__).with_name("input")

# Awful code to read the numbers from the file
pattern = r"target area: x=(-?\d+)\.\.(-?\d+), y=(-?\d+)\.\.(-?\d+)"
with p.open('r') as file:
    m = re.match(pattern, file.read().strip())
    x_lo, x_hi, y_lo, y_hi = map(int, m.groups())
    x_lo, x_hi = (x_lo, x_hi) if x_lo < x_hi else (x_hi, x_lo)
    y_lo, y_hi = (y_lo, y_hi) if y_lo < y_hi else (y_hi, y_lo)


"""
OK so: We need to find the highest possible throw, that's inside
the target's y-boundary at the same moment it's in the x-boundary.

There are ways of doing this, like simulating all possible throws,
or perhaps something a bit smarter. However, we can maybe
simplify by considering drag.

On the x-axis, a throw will slow down until drag stops it.
If we can get it to stop right as it's above the target, we don't
need to throw precisely so it intersects at just the right time,
we'll have all the time in the world.
"""

# A throw's distance is a triangle number (4+3+2+1+0)
# So the good ol' n(n+1)/2 will give it to us
for i in range(x_hi+1):   # If we throw any harder we overshoot
    distance = i * (i+1) // 2
    if x_lo <= distance <= x_hi:
        print(f"{i} stops right on top at x={distance}")
        break
else:
    print("ERROR: No throw can stop above the target")
    print("This trick doesn't apply")
    exit()


"""
Now we no longer need to worry about when both axis line up.
On the y-axis, the velocity will slowly move negative.

If you throw upwards with y=3 velocity, the velocity & position:
y-vel: 3   2   1   0  -1  -2  -3  -4
y-pos: 3   5   6   6   5   3   0  -4

Any vertical velocity will cause it to re-intersect with y=0
Above the line the closest point to 0 is +n
Below the line the closest point to 0 is -n - 1
Also, note how the y-pos is mirrored.

Here's a premise: The higher you throw, the faster it falls.
The fastest we can throw is a speed where it's instantly at the
boundary of the target area's y-area, because the y-positions are
mirrored.
If the target's at y=3, the fastest you can throw is y=3, because
any higher and it'll be moving too fast on the way up/down.
"""

# The point furthest away from y=0 is our target.
# Because higher throws means the gap on the way down is larger,
# we want to hit the point furthest from 0 i.e. the biggest gap
# we can make.

# Don't forget: It's 1 faster when below 0
y_bound_1 = y_hi if y_hi >= 0 else abs(y_hi) - 1
y_bound_2 = y_lo if y_lo >= 0 else abs(y_lo) - 1

highest_speed = max(y_bound_1, y_bound_2)
highest_point = highest_speed * (highest_speed+1) // 2
print("The best vertical velocity is", highest_speed)
print("The highest point reached is", highest_point)