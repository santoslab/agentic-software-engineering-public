"""Loader for fixtures/scenarios.json — the fixtures run as tests (VER-7).

Every scenario is a claim about SPECS §4.1, §4.2, and §5.1; the fixture file
is never edited to make a test pass.
"""
import json
import os

import pytest

from game import Game

_PATH = os.path.join(os.path.dirname(__file__), "..", "fixtures", "scenarios.json")
with open(_PATH) as _f:
    SCENARIOS = json.load(_f)


@pytest.mark.parametrize("s", SCENARIOS["games"], ids=lambda s: s["name"])
def test_game_scenario(s):
    """SPECS §4.1, §4.2, §5.1: every listed move is accepted, no winner is
    reported before the final move, and the winner after the final move equals
    expected_winner."""
    g = Game()
    moves = s["moves"]
    winner = None
    for n, (row, col) in enumerate(moves, start=1):
        assert g.make_move(row, col) is True, f"move {n} ({row},{col}) was rejected"
        winner = g.check_winner()
        if n < len(moves):
            assert winner is None, f"winner {winner!r} reported before the final move"
    assert winner == s["expected_winner"]


@pytest.mark.parametrize("s", SCENARIOS["rejections"], ids=lambda s: s["name"])
def test_rejection_scenario(s):
    """SPECS §5.1: after the setup moves, the attempt is rejected and the board
    and the turn are unchanged."""
    g = Game()
    for row, col in s["setup_moves"]:
        assert g.make_move(row, col) is True
    board_before = [row[:] for row in g.board]
    player_before = g.current_player
    assert g.make_move(*s["attempt"]) is False
    assert g.board == board_before
    assert g.current_player == player_before
