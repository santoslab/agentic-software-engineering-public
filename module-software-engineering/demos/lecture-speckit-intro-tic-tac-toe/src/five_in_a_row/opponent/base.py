"""The Opponent protocol (contracts/opponent.md)."""

from typing import Protocol, runtime_checkable

from five_in_a_row.engine import GameState, Square


@runtime_checkable
class Opponent(Protocol):
    def choose_move(self, state: GameState) -> Square:
        """An empty square for `state.turn` to play; `state` must be in progress."""
        ...
