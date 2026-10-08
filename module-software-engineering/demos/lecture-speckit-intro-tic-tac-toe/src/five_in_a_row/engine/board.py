"""Marks, squares and the board (contracts/engine.md; data-model.md, Engine entities)."""

from dataclasses import dataclass
from enum import Enum

SIZE = 9


class Mark(Enum):
    X = "X"
    O = "O"

    def other(self) -> "Mark":
        return Mark.O if self is Mark.X else Mark.X


@dataclass(frozen=True, slots=True)
class Square:
    """A position by row and column, 1..SIZE; row 1 is the top, column 1 the left.

    Any integers are accepted so that an out-of-range entry can be described;
    GameState.play rejects it.
    """

    row: int
    col: int

    def on_board(self) -> bool:
        return 1 <= self.row <= SIZE and 1 <= self.col <= SIZE


class Board:
    """An immutable SIZE x SIZE board; each square is empty or holds one mark."""

    __slots__ = ("_cells",)

    def __init__(self, cells: tuple[Mark | None, ...] | None = None) -> None:
        self._cells = cells if cells is not None else (None,) * (SIZE * SIZE)

    @staticmethod
    def _index(square: Square) -> int:
        if not square.on_board():
            raise ValueError(f"square off the board: {square}")
        return (square.row - 1) * SIZE + (square.col - 1)

    def at(self, square: Square) -> Mark | None:
        return self._cells[self._index(square)]

    def empty_squares(self) -> tuple[Square, ...]:
        return tuple(
            Square(i // SIZE + 1, i % SIZE + 1) for i, cell in enumerate(self._cells) if cell is None
        )

    def is_full(self) -> bool:
        return None not in self._cells

    def with_mark(self, square: Square, mark: Mark) -> "Board":
        """A copy with `mark` at `square`. For the engine's use; callers use GameState.play."""
        i = self._index(square)
        return Board(self._cells[:i] + (mark,) + self._cells[i + 1 :])

    def __eq__(self, other: object) -> bool:
        return isinstance(other, Board) and self._cells == other._cells

    def __hash__(self) -> int:
        return hash(self._cells)
