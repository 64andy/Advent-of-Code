N_ROWS = 128    # 128 rows
N_COLS = 8      # 8 seats per row

def bsp(code: str, lower: int, upper: int) -> int:
    for move in code:
        halfway = (lower+upper) // 2
        if move in "FL":
            upper = halfway
        elif move in "BR":
            lower = halfway
        else:
            raise ValueError(f"{code!r} contains invalid char not in 'BFLR'")
    return lower


def get_seat_id(code: str) -> int:
    """
    Essentially, this is a binary search, bar the search.
    First 7 chars of `code` are either 'B'ack or 'F'orward,
    representing which of the 128 rows the seat's on.
    Last 3 chars are either 'L'eft or 'R'ight,
    as each row has 8 seats
    """
    code = code.strip()
    assert len(code) == 10
    row = bsp(code[:7], 0, N_ROWS)
    col = bsp(code[7:], 0, N_COLS)
    seat_id = (row * N_COLS) + col
    print(f"{row} * {N_COLS} + {col} = {seat_id}")
    return seat_id

with open("day5.in", "r") as file:
    used_seats = sorted(get_seat_id(line) for line in file)
    for i in range(len(used_seats)):
        print(used_seats[i], end=',')
        assert used_seats[i] == used_seats[i+1] - 1
        


