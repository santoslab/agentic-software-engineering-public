"""Evidence for contracts/cli.md C-7: reading a square."""

import pytest

from five_in_a_row.cli.parse import parse_move
from five_in_a_row.engine import Square

req = pytest.mark.req


@req("FR-004")
@pytest.mark.parametrize("text", ["4 7", "4,7", " 4 , 7 ", "4   7", "4, 7", "4 ,7"])
def test_row_then_column_separated_by_space_or_comma(text):
    assert parse_move(text) == Square(4, 7)


@req("FR-004", "EDGE-out-of-range-square")
@pytest.mark.parametrize("text, square", [("0 3", Square(0, 3)), ("10 3", Square(10, 3)),
                                          ("-1 3", Square(-1, 3))])
def test_out_of_range_numbers_are_left_for_the_engine(text, square):
    assert parse_move(text) == square


@req("FR-004", "EDGE-unreadable-input")
@pytest.mark.parametrize("text", ["abc", "5", "1 2 3", "", "4;7", "4,,7", "x y"])
def test_anything_else_is_unreadable(text):
    assert parse_move(text) is None
