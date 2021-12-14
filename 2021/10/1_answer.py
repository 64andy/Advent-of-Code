"""
Day 10.1: Corrupted Chunk Syntax
Chunks start/end with the brackets "(){}<>[]"
Each start bracket must have an appropriate corresponding
end bracket, e.g. <([])> and [()<>()], not {(]}

We consider a 'corrupted' chunk to end with the wrong character.

We score depending on the character, with the first wrong
character having a score of:
- ')': 3,
- ']': 57,
- '}': 1197,
- '>': 25137
"""

from pathlib import Path
p = Path(__file__).with_name("input")

# Vars
STARTS = "([{<"
PAIRS = dict(("()", "<>", "{}", "[]"))
ENDS = {
    ')': 3,
    ']': 57,
    '}': 1197,
    '>': 25137
}


def parsed_corrupted_score(line: str) -> int:
    """
    Interprets the given 'chunks'.
    Returns the first illegal character's score,
    or 0 if the syntax is right
    """
    stack = []
    for c in line:
        if c in STARTS:
            # If you're starting a bracket, don't think just add
            stack.append(c)
        elif c in ENDS:
            # Check if a corresponding start exists
            if len(stack) == 0:
                return ENDS[c]
            head = stack[-1]
            if head in STARTS and PAIRS[head] == c:
                stack.pop()
            else:
                return ENDS[c]
        else:
            raise ValueError(f"I can't handle {c!r} !!!")
    return 0



with p.open('r') as file:
    lines = [line.strip() for line in file]

total = 0

for line in lines:
    score = parsed_corrupted_score(line)
    total += score
print(f"{total = }")