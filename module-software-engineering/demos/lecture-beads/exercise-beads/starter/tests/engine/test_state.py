"""Evidence for contracts/engine.md: GameState.new, play, results."""

import pytest

from five_in_a_row.engine import (
    GameState,
    IllegalMove,
    IllegalMoveReason,
    Mark,
    Result,
    Square,
)
from tests.positions import DRAW_MOVES, DRAW_PATTERN

req = pytest.mark.req


def play(*moves, state=None):
    """Play (row, col) moves alternately from `state` (default: a new game)."""
    state = state or GameState.new()
    for row, col in moves:
        state = state.play(Square(row, col))
    return state


def position(x_squares, o_squares):
    """A legal in-progress position with X to move: X and O alternate, X first.

    `o_squares` has the same length as `x_squares`; O's moves are spare squares when the
    test only cares about X's line.
    """
    assert len(x_squares) == len(o_squares)
    moves = [sq for pair in zip(x_squares, o_squares) for sq in pair]
    return play(*moves)


# Spare O squares far from the lines tested below.
SPARE_O = [(9, 1), (9, 3), (9, 5), (9, 7), (9, 9)]


@req("FR-001", "FR-002")
def test_new_game():
    state = GameState.new()
    assert state.turn is Mark.X
    assert state.result is Result.IN_PROGRESS
    assert state.last_move is None
    assert len(state.board.empty_squares()) == 81
    assert state.winner is None


@req("FR-003", "US1-2")
def test_accepted_move_places_mark_and_passes_turn():
    start = GameState.new()
    after = start.play(Square(5, 5))
    assert after.board.at(Square(5, 5)) is Mark.X
    assert after.turn is Mark.O
    assert after.last_move == Square(5, 5)
    assert after.result is Result.IN_PROGRESS
    again = after.play(Square(1, 1))
    assert again.board.at(Square(1, 1)) is Mark.O
    assert again.turn is Mark.X


@req("FR-003")
def test_play_does_not_change_the_old_state():
    start = GameState.new()
    start.play(Square(5, 5))
    assert start.board.at(Square(5, 5)) is None
    assert start.turn is Mark.X


@req("FR-005", "SC-006", "EDGE-out-of-range-square")
@pytest.mark.parametrize("square", [Square(0, 3), Square(10, 3), Square(3, 0), Square(3, 10)])
def test_out_of_range_is_rejected(square):
    state = play((5, 5))
    with pytest.raises(IllegalMove) as err:
        state.play(square)
    assert err.value.reason is IllegalMoveReason.OUT_OF_RANGE
    assert err.value.square == square
    assert state.turn is Mark.O
    assert state.board.empty_squares() == play((5, 5)).board.empty_squares()


@req("FR-005", "SC-006", "EDGE-occupied-square")
def test_occupied_is_rejected():
    state = play((5, 5))
    with pytest.raises(IllegalMove) as err:
        state.play(Square(5, 5))
    assert err.value.reason is IllegalMoveReason.OCCUPIED
    assert state.board.at(Square(5, 5)) is Mark.X
    assert state.turn is Mark.O


@req("FR-005", "FR-009")
def test_game_over_is_rejected_before_other_reasons():
    won = position([(5, 1), (5, 2), (5, 3), (5, 4)], SPARE_O[:4]).play(Square(5, 5))
    assert won.result is Result.X_WON
    for square in (Square(1, 1), Square(0, 0), Square(5, 5)):
        with pytest.raises(IllegalMove) as err:
            won.play(square)
        assert err.value.reason is IllegalMoveReason.GAME_OVER


@req("FR-005")
def test_out_of_range_is_reported_before_occupied():
    with pytest.raises(IllegalMove) as err:
        GameState.new().play(Square(0, 0))
    assert err.value.reason is IllegalMoveReason.OUT_OF_RANGE


@req("FR-008", "FR-009", "US1-3")
def test_row_win():
    state = position([(3, 2), (3, 3), (3, 4), (3, 5)], SPARE_O[:4])
    won = state.play(Square(3, 6))
    assert won.result is Result.X_WON
    assert won.winner is Mark.X


@req("FR-008", "FR-009")
def test_column_win():
    state = position([(1, 4), (2, 4), (3, 4), (4, 4)], SPARE_O[:4])
    assert state.play(Square(5, 4)).result is Result.X_WON


@req("FR-008", "FR-009", "US1-4")
def test_diagonal_win():
    state = position([(1, 1), (2, 2), (3, 3), (4, 4)], SPARE_O[:4])
    assert state.play(Square(5, 5)).result is Result.X_WON


@req("FR-008", "FR-009", "US1-5")
def test_anti_diagonal_win():
    state = position([(1, 9), (2, 8), (3, 7), (4, 6)], SPARE_O[:4])
    assert state.play(Square(5, 5)).result is Result.X_WON


@req("FR-008")
def test_o_wins_too():
    moves = [(9, 1), (1, 1), (9, 3), (1, 2), (9, 5), (1, 3), (9, 7), (1, 4), (7, 1), (1, 5)]
    won = play(*moves)
    assert won.result is Result.O_WON
    assert won.winner is Mark.O


@req("FR-008", "US1-6", "EDGE-more-than-five-in-a-row")
def test_six_in_a_row_by_filling_a_gap_wins():
    state = position([(7, 1), (7, 2), (7, 4), (7, 5), (7, 6)], SPARE_O)
    assert state.result is Result.IN_PROGRESS
    assert state.play(Square(7, 3)).result is Result.X_WON


@req("FR-008", "EDGE-two-lines-at-once")
def test_two_lines_at_once_is_one_win():
    x = [(5, 1), (5, 2), (5, 3), (5, 4), (1, 5), (2, 5), (3, 5), (4, 5)]
    o = [(9, 1), (9, 2), (9, 3), (9, 4), (9, 6), (9, 7), (9, 8), (8, 1)]
    won = position(x, o).play(Square(5, 5))
    assert won.result is Result.X_WON
    assert won.winner is Mark.X


@req("FR-010", "EDGE-win-on-the-last-square")
def test_win_on_the_last_square_is_a_win():
    # DRAW_PATTERN with row 1 changed to XXXXXOOOO (same counts: X 41, O 40). Without
    # (1,3) no line is longer than 3; X fills (1,3) last and completes five on row 1.
    pattern = ("XXXXXOOOO",) + DRAW_PATTERN[1:]
    squares = [(r, c, pattern[r - 1][c - 1]) for r in range(1, 10) for c in range(1, 10)]
    xs = [(r, c) for r, c, m in squares if m == "X" and (r, c) != (1, 3)]
    os_ = [(r, c) for r, c, m in squares if m == "O"]
    before_last = play(*[sq for pair in zip(xs, os_) for sq in pair])
    assert before_last.result is Result.IN_PROGRESS
    assert before_last.board.empty_squares() == (Square(1, 3),)
    last = before_last.play(Square(1, 3))
    assert last.board.is_full()
    assert last.result is Result.X_WON


@req("FR-010", "US1-7", "SC-003")
def test_full_board_without_a_win_is_a_draw():
    state = GameState.new()
    for i, (row, col) in enumerate(DRAW_MOVES):
        assert state.result is Result.IN_PROGRESS, f"terminal before move {i + 1}"
        state = state.play(Square(row, col))
    assert state.board.is_full()
    assert state.result is Result.DRAW
    assert state.winner is None


@req("SC-003")
def test_four_in_a_line_is_not_a_win():
    state = position([(2, 1), (2, 2), (2, 3)], SPARE_O[:3]).play(Square(2, 4))
    assert state.result is Result.IN_PROGRESS


@req("SC-003")
def test_five_broken_by_a_gap_is_not_a_win():
    state = position([(2, 1), (2, 2), (2, 4), (2, 5)], SPARE_O[:4]).play(Square(2, 6))
    assert state.result is Result.IN_PROGRESS


@req("SC-003")
def test_five_broken_by_the_other_mark_is_not_a_win():
    # O sits at (2,3) between X's marks.
    x = [(2, 1), (2, 2), (2, 4), (2, 5)]
    o = [(2, 3), (9, 1), (9, 3), (9, 5)]
    state = position(x, o).play(Square(2, 6))
    assert state.result is Result.IN_PROGRESS
