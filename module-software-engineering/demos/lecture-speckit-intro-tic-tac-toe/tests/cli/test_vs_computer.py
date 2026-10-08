"""Evidence for User Story 2 through the CLI: playing the computer (C-10 to C-12).

Each script ends at the result line: what follows a finished game changes in US3.
"""

import io
import random
import time

import pytest

from five_in_a_row.cli import run
from five_in_a_row.opponent import RandomOpponent
from tests.cli.conftest import moves_as_lines

req = pytest.mark.req


@req("US2-1", "FR-013")
def test_human_is_x_and_moves_first(session):
    s = session(["1"])
    assert s.boards_drawn() == 1
    first_prompt = next(line for line in s.text.splitlines() if " to move" in line)
    assert first_prompt.lstrip().startswith("X to move")
    assert s.opponents[0].calls == 0


@req("FR-012", "FR-019", "US2-2")
def test_computer_moves_without_input_and_names_its_square(session):
    s = session(["1", "5 5"], opponent_moves=[(4, 7)])
    assert s.opponents[0].calls == 1
    assert "Computer (O) plays row 4, column 7." in s.text
    assert s.boards_drawn() == 3                       # start, after X, after O
    after = s.text.split("Computer (O) plays row 4, column 7.")[1]
    assert " 4  . . . . . . O . ." in after
    prompts = [line.lstrip()[0] for line in s.text.splitlines() if " to move" in line]
    assert prompts == ["X", "X"]                       # no prompt on the computer's turn


@req("US2-4", "FR-009")
def test_computer_win_is_announced(session):
    human = [(9, 1), (9, 3), (9, 5), (9, 7), (7, 1)]
    computer = [(1, 1), (1, 2), (1, 3), (1, 4), (1, 5)]
    s = session(["1"] + moves_as_lines(human), opponent_moves=computer)
    assert "The computer wins! (O)" in s.text
    assert "You win" not in s.text


@req("FR-009")
def test_human_win_is_announced(session):
    human = [(5, 1), (5, 2), (5, 3), (5, 4), (5, 5)]
    computer = [(1, 1), (1, 2), (1, 3), (1, 4)]
    s = session(["1"] + moves_as_lines(human), opponent_moves=computer)
    assert "You win! (X)" in s.text
    assert "computer wins" not in s.text.lower()


@req("SC-005")
def test_computer_turns_are_fast():
    # Human tries every square in order; taken ones are rejected and the next is tried.
    script = "1\n" + "".join(f"{r} {c}\n" for r in range(1, 10) for c in range(1, 10))
    out = io.StringIO()
    start = time.monotonic()
    run(io.StringIO(script), out, opponent_factory=lambda: RandomOpponent(random.Random(5)))
    elapsed = time.monotonic() - start
    computer_moves = out.getvalue().count("Computer (O) plays")
    assert computer_moves > 0
    assert elapsed < 1.0      # the whole game, so every computer turn is well under 1 s
