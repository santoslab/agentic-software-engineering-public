"""A computer opponent that picks uniformly among empty squares (FR-012; research.md R6)."""

import random

from five_in_a_row.engine import GameState, Result, Square


class RandomOpponent:
    def __init__(self, rng: random.Random | None = None) -> None:
        self._rng = rng if rng is not None else random.Random()

    def choose_move(self, state: GameState) -> Square:
        if state.result is not Result.IN_PROGRESS:
            raise ValueError("the game is over; there is no move to choose")
        return self._rng.choice(state.board.empty_squares())
