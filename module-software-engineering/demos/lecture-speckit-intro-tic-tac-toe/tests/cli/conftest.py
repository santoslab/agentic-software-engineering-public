"""Helpers for CLI transcript tests (tasks.md T020)."""

import io

import pytest

from five_in_a_row.cli import run
from five_in_a_row.engine import Square

BOARD_HEADER = "    1 2 3 4 5 6 7 8 9"


class ScriptedOpponent:
    """Plays the given (row, col) squares in order.

    One instance serves a whole vs-computer series (contracts/cli.md §1), so the list
    covers every game a test plays before returning to the start menu.
    """

    def __init__(self, moves):
        self._moves = iter(moves)
        self.calls = 0

    def choose_move(self, state):
        self.calls += 1
        row, col = next(self._moves)
        return Square(row, col)


class Session:
    """The result of one scripted run: exit code, transcript, opponents created."""

    def __init__(self, lines, opponent_moves=()):
        self.opponents = []

        def factory():
            opponent = ScriptedOpponent(opponent_moves)
            self.opponents.append(opponent)
            return opponent

        out = io.StringIO()
        script = "".join(f"{line}\n" for line in lines)
        self.code = run(io.StringIO(script), out, opponent_factory=factory)
        self.text = out.getvalue()

    def boards_drawn(self):
        return self.text.count(BOARD_HEADER)


def moves_as_lines(moves):
    return [f"{row} {col}" for row, col in moves]


@pytest.fixture
def session():
    return Session
