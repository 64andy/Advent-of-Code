from pathlib import Path
p = Path(__file__).with_name("input")

# Funcs

def calculate_score(their_move: str, expected_outcome: str) -> int:
    their_move = CHAR_TO_MOVE[their_move]
    expected_outcome = CHAR_TO_OUTCOME[expected_outcome]
    # Step 1: Part of your score is your move
    if expected_outcome == OUTCOME.DRAW:
        your_move = their_move
    elif expected_outcome == OUTCOME.WIN:
        your_move = WINNING_MOVE[their_move]
    elif expected_outcome == OUTCOME.LOSS:
        your_move = LOSING_MOVE[their_move]
    else:
        raise ValueError()
    # Step 2: The other part is the outcome
    print(your_move, "+", expected_outcome)
    
    return your_move + expected_outcome

# Vars
class OUTCOME:
    """Each outcome has an associated 'score'"""
    LOSS = 0
    DRAW = 3
    WIN = 6

class MOVES:
    """Each move has an associated 'score'"""
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

LOSING_MOVE = {
    MOVES.ROCK: MOVES.SCISSORS,
    MOVES.PAPER: MOVES.ROCK,
    MOVES.SCISSORS: MOVES.PAPER
}

WINNING_MOVE = dict(reversed(x) for x in LOSING_MOVE.items())

CHAR_TO_MOVE = {
    'A': MOVES.ROCK,
    'B': MOVES.PAPER,
    'C': MOVES.SCISSORS,
}

CHAR_TO_OUTCOME = {
    'X': OUTCOME.LOSS,
    'Y': OUTCOME.DRAW,
    'Z': OUTCOME.WIN,
}

total_score = 0

with p.open('r') as file:
    for line in file:
        lhs, rhs = line[0], line[2]
        print(lhs, rhs, "=> ", end='')
        score = calculate_score(lhs, rhs)
        total_score += score

print(total_score)