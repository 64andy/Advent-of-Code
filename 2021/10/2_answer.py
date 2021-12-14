"""
Day 10.2: Incomplete Chunk Syntax
Chunks start/end with the brackets "(){}<>[]"
Each start bracket must have an appropriate corresponding
end bracket, e.g. <([])> and [()<>()], not {(]} or {(

We consider a 'corrupted' chunk to end with the wrong character.
We consider it 'incomplete' if a chunk doesn't end.

For part 2: We only look at incomplete chunks, and ignore corrupted

We score depending on the missing character:
- ')': 1,
- ']': 2,
- '}': 3,
- '>': 4

Start each line with a score of 0
For every missing character, score *= 5; score += char's score

Each incomplete line is assigned this score, the question's answer
is the median of these scores
"""

from pathlib import Path
from statistics import median
p = Path(__file__).with_name("input")

# Vars
STARTS = {
    '(': 1,
    '[': 2,
    '{': 3,
    '<': 4
}
ENDS = ")]}>"
PAIRS = dict(("()", "<>", "{}", "[]"))


def parsed_line_score(line: str) -> int:
    """
    Interprets the given 'chunks'.
    Returns the 'score' needed to 
    """
    stack = []
    # Firstly, filter out line if corrupted
    for c in line:
        if c in STARTS:
            # If you're starting a bracket, don't think just add
            stack.append(c)
        elif c in ENDS:
            # Check if a corresponding start exists
            if len(stack) == 0:
                return -1
            head = stack[-1]
            if head in STARTS and PAIRS[head] == c:
                stack.pop()
            else:
                return -1
        else:
            raise ValueError(f"I can't handle {c!r} !!!")
    # Now, figure out the scores
    score = 0
    for c in reversed(stack):
        score *= 5
        score += STARTS[c]
    return score


with p.open('r') as file:
    lines = [line.strip() for line in file]


scores = []
for line in lines:
    score = parsed_line_score(line)
    if score != -1:
        scores.append(score)

print(median(scores))