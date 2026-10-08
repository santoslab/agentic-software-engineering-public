"""Board drawing and message text (contracts/cli.md C-5, C-6, C-8, C-12, C-13)."""

from five_in_a_row.engine import SIZE, Board, GameState, IllegalMoveReason, Mark, Result, Square

EMPTY = "."


def render_board(board: Board) -> str:
    """Column numbers across the top, row numbers down the left, row 1 first (C-5)."""
    lines = ["    " + " ".join(str(col) for col in range(1, SIZE + 1))]
    for row in range(1, SIZE + 1):
        cells = (board.at(Square(row, col)) for col in range(1, SIZE + 1))
        lines.append(f"{row:>2}  " + " ".join(m.value if m else EMPTY for m in cells))
    return "\n".join(lines)


def move_prompt(mark: Mark) -> str:
    return f"{mark.value} to move — type row and column (e.g. 4 7):"


def rejection(reason: IllegalMoveReason, square: Square) -> str:
    where = f"Row {square.row}, column {square.col}"
    if reason is IllegalMoveReason.OCCUPIED:
        return f"{where} is occupied. Choose an empty square."
    if reason is IllegalMoveReason.OUT_OF_RANGE:
        return f"{where} is out of range: rows and columns are 1 to {SIZE}."
    return "The game is over."


def unreadable(entry: str) -> str:
    return f"'{entry}' was not understood. Type a row and a column, e.g. 4 7."


def result_line(state: GameState) -> str:
    """Two-player result (C-12, C-13)."""
    if state.result is Result.DRAW:
        return "It's a draw."
    return f"{state.winner.value} wins!"
