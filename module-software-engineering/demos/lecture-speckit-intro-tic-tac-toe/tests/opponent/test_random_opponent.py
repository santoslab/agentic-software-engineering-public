"""Evidence for contracts/opponent.md: RandomOpponent."""

import random

import pytest

from five_in_a_row.engine import GameState, Result, Square
from five_in_a_row.opponent import Opponent, RandomOpponent
from tests.positions import DRAW_MOVES

req = pytest.mark.req


def random_position(rng):
    """An in-progress position reached by random legal moves."""
    while True:
        state = GameState.new()
        for _ in range(rng.randrange(0, 70)):
            state = state.play(rng.choice(state.board.empty_squares()))
            if state.result is not Result.IN_PROGRESS:
                break
        if state.result is Result.IN_PROGRESS:
            return state


def ten_empty_position():
    """The first 71 moves of DRAW_MOVES: 10 empty squares, no win, O to move."""
    state = GameState.new()
    for row, col in DRAW_MOVES[:71]:
        state = state.play(Square(row, col))
    assert len(state.board.empty_squares()) == 10
    assert state.result is Result.IN_PROGRESS
    return state


def test_random_opponent_satisfies_the_protocol():
    assert isinstance(RandomOpponent(), Opponent)


@req("FR-012", "SC-004", "US2-3")
def test_a_thousand_moves_are_all_onto_empty_squares():
    positions = random.Random(2026)
    opponent = RandomOpponent(random.Random(7))
    for _ in range(1000):
        state = random_position(positions)
        square = opponent.choose_move(state)
        assert state.board.at(square) is None
        state.play(square)  # accepted: does not raise


@req("FR-012", "SC-004", "US2-3")
def test_every_empty_square_gets_chosen():
    state = ten_empty_position()
    opponent = RandomOpponent(random.Random(11))
    chosen = {opponent.choose_move(state) for _ in range(1000)}
    assert chosen == set(state.board.empty_squares())


def test_terminal_state_is_refused():
    state = GameState.new()
    for row, col in DRAW_MOVES:
        state = state.play(Square(row, col))
    with pytest.raises(ValueError):
        RandomOpponent().choose_move(state)


def test_the_state_is_not_changed():
    state = ten_empty_position()
    before = (state.board, state.turn, state.result, state.last_move)
    RandomOpponent(random.Random(3)).choose_move(state)
    assert (state.board, state.turn, state.result, state.last_move) == before
