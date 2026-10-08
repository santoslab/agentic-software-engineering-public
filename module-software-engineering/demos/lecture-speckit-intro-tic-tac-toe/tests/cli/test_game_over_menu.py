"""Evidence for contracts/cli.md C-14 to C-16: after a game."""

import pytest

from tests.cli.conftest import moves_as_lines
from tests.positions import O_WINS_MOVES, X_WINS_MOVES

req = pytest.mark.req

START = "Choose 1, 2 or 3"
GAME_OVER = "Choose 1 or 2"


def board_rows_after(text, marker):
    """The 9 board rows of the first board drawn after `marker`."""
    lines = text.split(marker, 1)[1].splitlines()
    header = next(i for i, line in enumerate(lines) if line.startswith("    1 2 3"))
    return [line.split()[1:] for line in lines[header + 1 : header + 10]]


@req("FR-015", "US3-2")
def test_game_over_menu_offers_play_again_and_back(session):
    s = session(["2"] + moves_as_lines(X_WINS_MOVES))
    after = s.text.split("X wins!", 1)[1]
    assert "1  Play again" in after
    assert "2  Back to the start menu" in after
    assert GAME_OVER in after


@req("FR-017", "SC-006", "EDGE-invalid-menu-choice")
@pytest.mark.parametrize("entry", ["7", "x", "", "3"])
def test_invalid_game_over_choice_shows_the_menu_again(session, entry):
    s = session(["2"] + moves_as_lines(X_WINS_MOVES) + [entry, "2", "3"])
    assert "not a choice" in s.text.split("X wins!", 1)[1]
    assert s.text.count(GAME_OVER) == 2
    assert s.code == 0


@req("US3-3")
def test_play_again_two_player_starts_empty_with_x(session):
    s = session(["2"] + moves_as_lines(X_WINS_MOVES) + ["1"])
    rows = board_rows_after(s.text, f"{GAME_OVER}: 1")
    assert all(cell == "." for row in rows for cell in row)
    after = s.text.split(f"{GAME_OVER}: 1", 1)[1]
    first_prompt = next(line for line in after.splitlines() if " to move" in line)
    assert first_prompt.startswith("X to move")


@req("US3-4", "FR-016", "FR-015")
def test_back_to_the_start_menu_then_quit(session):
    s = session(["2"] + moves_as_lines(X_WINS_MOVES) + ["2", "3"])
    assert s.text.count(START) == 2
    assert s.code == 0
    assert "goodbye" not in s.text.lower()


@req("US3-2", "US3-3", "US3-4")
def test_full_session_from_the_independent_test(session):
    lines = (["2"] + moves_as_lines(X_WINS_MOVES) + ["1"]
             + moves_as_lines(O_WINS_MOVES) + ["2", "3"])
    s = session(lines)
    assert "X wins!" in s.text
    assert "O wins!" in s.text
    assert s.text.count(START) == 2
    assert s.code == 0
