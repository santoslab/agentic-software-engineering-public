"""Evidence for FR-018 / contracts/cli.md C-9: leaving a game partway through."""

import pytest

from five_in_a_row.cli.parse import is_leave_command, parse_move
from tests.cli.conftest import moves_as_lines

req = pytest.mark.req

START = "Choose 1, 2 or 3"


@req("FR-018", "US3-5")
@pytest.mark.parametrize("entry", ["m", "M", " m "])
def test_leave_command_returns_to_the_start_menu(session, entry):
    s = session(["2", "5 5", entry])
    assert s.text.count(START) == 2
    after = s.text.split(f"{entry}\n", 1)[1]
    assert "wins!" not in after and "draw" not in after.lower()
    assert "Play again" not in s.text
    assert "not understood" not in s.text


@req("FR-018", "FR-007")
def test_every_move_prompt_mentions_the_leave_command(session):
    s = session(["1", "5 5", "5 6", "m"], opponent_moves=[(1, 1), (1, 2)])
    prompts = [line for line in s.text.splitlines() if " to move" in line]
    assert len(prompts) == 3
    assert all("m for the menu" in p for p in prompts)


@req("FR-013", "FR-018")
def test_leaving_as_o_then_playing_the_computer_again_makes_the_human_x(session):
    human = [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]
    computer = [(1, 1), (1, 2), (1, 3), (1, 4), (9, 9)]
    s = session(["1"] + moves_as_lines(human) + ["1", "m", "1"], opponent_moves=computer)
    new_series = s.text.rsplit(f"{START}: 1", 1)[1]
    first_prompt = next(l for l in new_series.splitlines() if " to move" in l)
    assert first_prompt.startswith("X to move")


@req("FR-018")
@pytest.mark.parametrize("entry", ["m", "M", " m "])
def test_leave_command_is_recognised_and_is_not_a_move(entry):
    assert is_leave_command(entry)
    assert parse_move(entry) is None


@req("FR-018")
@pytest.mark.parametrize("entry", ["menu", "q", "mm", "m 1"])
def test_other_words_are_not_the_leave_command(entry):
    assert not is_leave_command(entry)
