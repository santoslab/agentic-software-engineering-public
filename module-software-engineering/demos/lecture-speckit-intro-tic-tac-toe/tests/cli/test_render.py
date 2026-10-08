"""Evidence for contracts/cli.md C-5: drawing the board."""

import pytest

from five_in_a_row.cli.render import render_board
from five_in_a_row.engine import GameState, Square

req = pytest.mark.req


@req("FR-006", "FR-004")
def test_board_shows_numbers_marks_and_empty_squares():
    state = GameState.new()
    for row, col in [(1, 1), (5, 5), (9, 9)]:
        state = state.play(Square(row, col))   # X, O, X
    lines = render_board(state.board).splitlines()
    assert lines[0].split() == [str(n) for n in range(1, 10)]
    rows = lines[1:10]
    assert [line.split()[0] for line in rows] == [str(n) for n in range(1, 10)]
    cells = [line.split()[1:] for line in rows]
    assert all(len(row) == 9 for row in cells)
    assert cells[0][0] == "X"
    assert cells[4][4] == "O"
    assert cells[8][8] == "X"
    assert sum(row.count(".") for row in cells) == 78
