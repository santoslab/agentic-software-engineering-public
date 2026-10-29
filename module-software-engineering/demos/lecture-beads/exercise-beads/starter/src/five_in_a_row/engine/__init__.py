"""Game rules: board, turns, legal moves, win and draw (contracts/engine.md).

This is the engine's public API; other modules import only from here.
"""

from .board import SIZE, Board, Mark, Square
from .state import WIN_LENGTH, GameState, IllegalMove, IllegalMoveReason, Result

__all__ = [
    "SIZE",
    "WIN_LENGTH",
    "Board",
    "GameState",
    "IllegalMove",
    "IllegalMoveReason",
    "Mark",
    "Result",
    "Square",
]
