"""
It's a bingo solver. No diagonals
"""

from pathlib import Path
p = Path(__file__).with_name("input")


class Space:
    def __init__(self, num: str):
        self.num = int(num)
        self.marked = False

    def mark(self, num):
        if self.num == num:
            self.marked = True
            return True
        else:
            return False

    def __repr__(self):
        return ('O' if self.marked else 'X') + str(self.num)

    def __bool__(self):
        return self.marked


def to_board(board: str) -> list:
    rows = board.split('\n')
    return [[Space(n) for n in row.split()] for row in rows]


def mark_number(board, num):
    for row in board:
        for space in row:
            space.mark(num)


def check_complete_board(board) -> bool:
    for row in board:
        if all(row):
            return True
    for col in zip(*board):
        if all(col):
            return True
    return False


def apply_num(boards, num):
    for board in boards:
        mark_number(board, num)
        if check_complete_board(board):
            return board
    return None

# Vars
SIZE = 5    # 5x5 boards


with p.open('r') as file:
    nums, *boards = file.read().strip().split('\n\n')

nums = map(int, nums.strip().split(','))
boards = [to_board(board.strip()) for board in boards]

for num in nums:
    board = apply_num(boards, num)
    if board is not None:
        print("Ding")
        break

sum_of_unmarked = sum(n.num
                        for row in board for n in row 
                        if not n.marked
)
print(num * sum_of_unmarked)