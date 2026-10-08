"""Evidence for User Story 1 through the CLI: two players at one keyboard.

Each script ends at the result line: what follows a finished game changes in US3.
"""

import pytest

from tests.cli.conftest import moves_as_lines
from tests.positions import DRAW_MOVES, O_WINS_MOVES, X_WINS_MOVES

req = pytest.mark.req


def prompts(text):
    return [line for line in text.splitlines() if " to move" in line]


@req("FR-002", "FR-003", "FR-006", "FR-007", "FR-009", "FR-011",
     "US1-1", "US1-2", "US1-3")
def test_x_wins(session):
    s = session(["2"] + moves_as_lines(X_WINS_MOVES))
    assert s.code == 0
    assert s.boards_drawn() == len(X_WINS_MOVES) + 1     # before the first move, after each
    assert [p.lstrip()[0] for p in prompts(s.text)] == ["X", "O"] * 4 + ["X"]
    assert "X wins!" in s.text
    assert "O wins!" not in s.text


@req("FR-009", "SC-003")
def test_o_wins(session):
    s = session(["2"] + moves_as_lines(O_WINS_MOVES))
    assert "O wins!" in s.text
    assert "X wins!" not in s.text


@req("FR-010", "US1-7", "SC-003")
def test_draw(session):
    s = session(["2"] + moves_as_lines(DRAW_MOVES))
    after_last_move = s.text.rsplit(" to move", 1)[1]
    assert "draw" in after_last_move.lower()
    assert "wins!" not in s.text
    assert s.boards_drawn() == 82


@req("FR-005", "SC-006", "EDGE-occupied-square")
def test_occupied_square_is_rejected(session):
    s = session(["2", "5 5", "5 5"])
    assert "occupied" in s.text.lower()
    assert s.boards_drawn() == 2                          # start, after 5 5 only
    assert [p.lstrip()[0] for p in prompts(s.text)] == ["X", "O", "O"]


@req("FR-005", "SC-006", "EDGE-out-of-range-square")
def test_out_of_range_is_rejected(session):
    s = session(["2", "0 3"])
    assert "range" in s.text.lower()
    assert s.boards_drawn() == 1
    assert [p.lstrip()[0] for p in prompts(s.text)] == ["X", "X"]


@req("FR-005", "SC-006", "EDGE-unreadable-input")
def test_unreadable_entry_is_rejected(session):
    s = session(["2", "abc"])
    assert "not understood" in s.text.lower()
    assert s.boards_drawn() == 1
    assert [p.lstrip()[0] for p in prompts(s.text)] == ["X", "X"]


@req("FR-020", "US3-6", "EDGE-end-of-input-or-interrupt")
def test_end_of_input_mid_game(session):
    s = session(["2", "5 5", "1 1"])
    assert s.code == 0
    assert "goodbye" in s.text.lower()
    assert "Traceback" not in s.text
