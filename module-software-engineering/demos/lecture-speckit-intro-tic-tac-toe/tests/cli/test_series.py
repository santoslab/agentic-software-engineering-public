"""Evidence for FR-013 across "play again": sides swap against the computer."""

import pytest

from tests.cli.conftest import moves_as_lines

req = pytest.mark.req

GAME_OVER = "Choose 1 or 2"

# Game 1: human X wins on row 5; computer O plays row 1.
GAME1_HUMAN = [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]
GAME1_COMPUTER = [(1, 1), (1, 2), (1, 3), (1, 4)]
# Game 2: computer X moves first; human O wins on row 1.
GAME2_COMPUTER = [(9, 9), (9, 7), (9, 5), (9, 3), (7, 7)]
GAME2_HUMAN = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]


def first_lines_after(text, marker, n=40):
    return text.split(marker, 1)[1].splitlines()[:n]


def first_event(lines):
    """'computer' or 'prompt <mark>', whichever comes first."""
    for line in lines:
        if line.startswith("Computer ("):
            return "computer " + line[len("Computer (")]
        if " to move" in line:
            return "prompt " + line.lstrip()[0]
    return None


@req("FR-013", "US2-5")
def test_play_again_makes_the_human_o_and_the_computer_moves_first(session):
    s = session(["1"] + moves_as_lines(GAME1_HUMAN) + ["1"],
                opponent_moves=GAME1_COMPUTER + GAME2_COMPUTER)
    assert "You win! (X)" in s.text
    assert first_event(first_lines_after(s.text, f"{GAME_OVER}: 1")) == "computer X"
    assert "Computer (X) plays row 9, column 9." in s.text
    after = s.text.split("Computer (X) plays row 9, column 9.", 1)[1]
    assert next(l for l in after.splitlines() if " to move" in l).startswith("O to move")
    assert len(s.opponents) == 1                    # one opponent for the whole series


@req("FR-013", "US2-6")
def test_next_play_again_makes_the_human_x_again(session):
    lines = (["1"] + moves_as_lines(GAME1_HUMAN) + ["1"]
             + moves_as_lines(GAME2_HUMAN) + ["1"])
    s = session(lines, opponent_moves=GAME1_COMPUTER + GAME2_COMPUTER)
    assert "You win! (O)" in s.text
    game3 = s.text.split("You win! (O)", 1)[1].split(f"{GAME_OVER}: 1", 1)[1]
    assert first_event(game3.splitlines()) == "prompt X"


@req("FR-013", "US2-7")
def test_back_to_the_start_menu_resets_the_human_to_x(session):
    lines = (["1"] + moves_as_lines(GAME1_HUMAN) + ["1"]
             + moves_as_lines(GAME2_HUMAN) + ["2", "1"])
    s = session(lines, opponent_moves=GAME1_COMPUTER + GAME2_COMPUTER)
    new_series = s.text.rsplit("Choose 1, 2 or 3: 1", 1)[1]
    assert first_event(new_series.splitlines()) == "prompt X"
    assert len(s.opponents) == 2                    # a new series, a new opponent
