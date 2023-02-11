from pathlib import Path
p = Path(__file__).with_name("input")

# Funcs
def check_outcome(their_move: int, your_move: int) -> int:
    # Did you draw
    if their_move == your_move:
        return OUTCOME.DRAW
    # Did you win
    winning_move = WINNING_MOVE[their_move]
    if winning_move == your_move:
        return OUTCOME.WIN
    else:
        return OUTCOME.LOSS

def calculate_score(their_move: str, your_move: str) -> int:
    # Step 1: Part of your score is your move
    move_score = CHAR_TO_MOVE[your_move]
    # Step 2: The other part is the outcome
    outcome_score = check_outcome(CHAR_TO_MOVE[your_move], CHAR_TO_MOVE[their_move])
    print(move_score, "+", outcome_score)
    
    return move_score + outcome_score

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

WINNING_MOVE = {
    MOVES.ROCK: MOVES.SCISSORS,
    MOVES.PAPER: MOVES.ROCK,
    MOVES.SCISSORS: MOVES.PAPER
}

CHAR_TO_MOVE = {
    'A': MOVES.ROCK,
    'B': MOVES.PAPER,
    'C': MOVES.SCISSORS,
    'X': MOVES.ROCK,
    'Y': MOVES.PAPER,
    'Z': MOVES.SCISSORS,
}

total_score = 0

with p.open('r') as file:
    for line in file:
        lhs, rhs = line[0], line[2]
        print(lhs, rhs, "=> ", end='')
        score = calculate_score(lhs, rhs)
        total_score += score

print(total_score)