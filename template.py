"""
Day <x.y> - <title>

Python 3.9+

Input:
...

Logic:
...

Output:
...
"""

import dataclasses
from pathlib import Path


p = Path(__file__).with_name("test_input")

# Vars
...

# Classes
@dataclasses.dataclass
class ParsedFile:
    pass

# Funcs
...


# =====

def main():
    with p.open('r') as file:
        ...

if __name__ == "__main__":
    main()
