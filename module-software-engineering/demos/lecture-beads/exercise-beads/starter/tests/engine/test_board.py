"""Evidence for contracts/engine.md: Mark, Square, Board."""

import pytest

from five_in_a_row.engine import SIZE, GameState, Mark, Square

req = pytest.mark.req


@req("FR-002")
def test_mark_other_swaps_x_and_o():
    assert Mark.X.other() is Mark.O
    assert Mark.O.other() is Mark.X


@req("FR-004")
def test_squares_are_equal_by_row_and_column():
    assert Square(4, 7) == Square(4, 7)
    assert Square(4, 7) != Square(7, 4)


@req("FR-001")
def test_new_board_has_81_empty_squares_in_row_major_order():
    board = GameState.new().board
    assert SIZE == 9
    expected = tuple(Square(r, c) for r in range(1, 10) for c in range(1, 10))
    assert board.empty_squares() == expected
    assert all(board.at(sq) is None for sq in expected)
    assert not board.is_full()


@req("FR-004")
@pytest.mark.parametrize("square", [Square(0, 1), Square(10, 1), Square(1, 0), Square(1, 10)])
def test_at_off_board_square_raises(square):
    with pytest.raises(ValueError):
        GameState.new().board.at(square)
