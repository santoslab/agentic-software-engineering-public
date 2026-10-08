"""Game state, legal moves, win and draw (contracts/engine.md §Behavior)."""

from dataclasses import dataclass
from enum import Enum

from .board import Board, Mark, Square

WIN_LENGTH = 5

# Row, column, diagonal, anti-diagonal (data-model.md, Line).
_DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


class Result(Enum):
    IN_PROGRESS = "in progress"
    X_WON = "X won"
    O_WON = "O won"
    DRAW = "draw"


class IllegalMoveReason(Enum):
    GAME_OVER = "game over"
    OUT_OF_RANGE = "out of range"
    OCCUPIED = "occupied"


class IllegalMove(Exception):
    def __init__(self, reason: IllegalMoveReason, square: Square) -> None:
        super().__init__(f"{reason.value}: row {square.row}, column {square.col}")
        self.reason = reason
        self.square = square


@dataclass(frozen=True, slots=True)
class GameState:
    board: Board
    turn: Mark
    result: Result
    last_move: Square | None

    @classmethod
    def new(cls) -> "GameState":
        return cls(Board(), Mark.X, Result.IN_PROGRESS, None)

    @property
    def winner(self) -> Mark | None:
        return {Result.X_WON: Mark.X, Result.O_WON: Mark.O}.get(self.result)

    def play(self, square: Square) -> "GameState":
        if self.result is not Result.IN_PROGRESS:
            raise IllegalMove(IllegalMoveReason.GAME_OVER, square)
        if not square.on_board():
            raise IllegalMove(IllegalMoveReason.OUT_OF_RANGE, square)
        if self.board.at(square) is not None:
            raise IllegalMove(IllegalMoveReason.OCCUPIED, square)

        board = self.board.with_mark(square, self.turn)
        # A win is checked before fullness: a win on the last square is a win.
        if _completes_line(board, square, self.turn):
            result = Result.X_WON if self.turn is Mark.X else Result.O_WON
        elif board.is_full():
            result = Result.DRAW
        else:
            result = Result.IN_PROGRESS
        return GameState(board, self.turn.other(), result, square)


def _completes_line(board: Board, square: Square, mark: Mark) -> bool:
    """True if `square` lies on WIN_LENGTH or more consecutive `mark`s (research.md R5)."""
    for dr, dc in _DIRECTIONS:
        count = 1
        for sign in (1, -1):
            step = 1
            while True:
                nxt = Square(square.row + sign * step * dr, square.col + sign * step * dc)
                if not nxt.on_board() or board.at(nxt) is not mark:
                    break
                count += 1
                step += 1
        if count >= WIN_LENGTH:
            return True
    return False
