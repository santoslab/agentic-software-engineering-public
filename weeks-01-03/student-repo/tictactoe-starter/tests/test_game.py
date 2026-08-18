import pytest

from game import Game


def _empty_board():
    return [[None] * 9 for _ in range(9)]


def _tie_pattern_cell(r, c):
    """5-coloring (r + 2c) % 5 — guarantees no 5-in-a-row in any direction.

    The step (a + b) for direction (1,1) is 3 (coprime to 5), and (a - b) for
    direction (1,-1) is -1 (coprime to 5), so a window of 5 cells in any
    direction sees all 5 residues — exactly one is 'O' and four are 'X'.
    """
    return 'O' if (r + 2 * c) % 5 == 0 else 'X'


# ---------- __init__ ----------

def test_init_defaults():
    g = Game()
    assert g.board == _empty_board()
    assert g.current_player == 'X'
    assert g.starting_player == 'X'
    assert g.winner is None


def test_init_with_o_start():
    g = Game(starting_player='O')
    assert g.current_player == 'O'
    assert g.starting_player == 'O'
    assert g.board == _empty_board()
    assert g.winner is None


# ---------- make_move ----------

def test_make_move_writes_to_correct_cell():
    g = Game()
    assert g.make_move(3, 4) is True
    assert g.board[2][3] == 'X'
    for r in range(9):
        for c in range(9):
            if (r, c) != (2, 3):
                assert g.board[r][c] is None


def test_make_move_switches_player():
    g = Game()
    g.make_move(5, 5)
    assert g.current_player == 'O'
    g.make_move(1, 1)
    assert g.current_player == 'X'


@pytest.mark.parametrize("row,col", [
    (0, 5), (10, 5), (-1, 5), (5, 0), (5, 10), (5, -1),
])
def test_make_move_rejects_out_of_range(row, col):
    g = Game()
    assert g.make_move(row, col) is False
    assert g.board == _empty_board()
    assert g.current_player == 'X'


@pytest.mark.parametrize("row,col", [
    ('a', 5), (5, 'a'), (None, 5), (5, None), (1.5, 5), (5, 1.5),
    (True, 5), (5, False),
])
def test_make_move_rejects_non_int(row, col):
    g = Game()
    assert g.make_move(row, col) is False
    assert g.board == _empty_board()
    assert g.current_player == 'X'


def test_make_move_rejects_occupied_cell():
    g = Game()
    g.make_move(5, 5)
    assert g.current_player == 'O'
    assert g.make_move(5, 5) is False
    # Player did not switch; board unchanged.
    assert g.current_player == 'O'
    assert g.board[4][4] == 'X'


# ---------- available_moves ----------

def test_available_moves_initial_row_major():
    g = Game()
    moves = g.available_moves()
    assert len(moves) == 81
    assert moves[0] == (1, 1)
    assert moves[8] == (1, 9)
    assert moves[9] == (2, 1)
    assert moves[-1] == (9, 9)


def test_available_moves_shrinks_after_moves():
    g = Game()
    g.make_move(5, 5)
    g.make_move(1, 1)
    moves = g.available_moves()
    assert (5, 5) not in moves
    assert (1, 1) not in moves
    assert len(moves) == 79


def test_available_moves_empty_on_full_board():
    g = Game()
    for r in range(9):
        for c in range(9):
            g.board[r][c] = 'X'
    assert g.available_moves() == []


# ---------- row_has_space ----------

def test_row_has_space_empty_row():
    g = Game()
    assert g.row_has_space(5) is True


def test_row_has_space_partially_filled():
    g = Game()
    g.make_move(5, 5)
    assert g.row_has_space(5) is True


def test_row_has_space_full_row():
    g = Game()
    for c in range(9):
        g.board[4][c] = 'X'
    assert g.row_has_space(5) is False


@pytest.mark.parametrize("bad", [0, 10, -1, 'a', None, 1.5, True])
def test_row_has_space_rejects_invalid(bad):
    g = Game()
    assert g.row_has_space(bad) is False


# ---------- check_winner ----------

# Five-in-a-row cell sets across the 4 win directions.
WIN_RUNS = [
    # rightward (→) in row 3, cols 2..6
    [(3, 2), (3, 3), (3, 4), (3, 5), (3, 6)],
    # rightward at bottom row (non-origin start, near right edge)
    [(9, 5), (9, 6), (9, 7), (9, 8), (9, 9)],
    # downward (↓) in col 7, rows 4..8
    [(4, 7), (5, 7), (6, 7), (7, 7), (8, 7)],
    # diagonal ↘ starting (1, 1)
    [(1, 1), (2, 2), (3, 3), (4, 4), (5, 5)],
    # diagonal ↙ starting (1, 9)
    [(1, 9), (2, 8), (3, 7), (4, 6), (5, 5)],
]


@pytest.mark.parametrize("winner", ['X', 'O'])
@pytest.mark.parametrize("cells", WIN_RUNS)
def test_check_winner_detects_5_in_a_row(winner, cells):
    g = Game()
    for r, c in cells:
        g.board[r - 1][c - 1] = winner
    assert g.check_winner() == winner
    assert g.winner == winner


def test_check_winner_4_in_a_row_no_winner():
    g = Game()
    for c in range(1, 5):
        g.board[0][c - 1] = 'X'
    assert g.check_winner() is None
    assert g.winner is None


def test_check_winner_empty_board_returns_none():
    g = Game()
    assert g.check_winner() is None
    assert g.winner is None


def test_check_winner_bounds_no_wraparound_horizontal():
    """4 marks at end of row 1 + 1 mark at start of row 2 must NOT count as 5."""
    g = Game()
    for c in range(6, 10):
        g.board[0][c - 1] = 'X'
    g.board[1][0] = 'X'
    assert g.check_winner() is None


def test_check_winner_bounds_lone_mark_near_edge():
    """A single mark with no room to extend 5 cells in any direction must not crash."""
    g = Game()
    g.board[8][8] = 'X'  # bottom-right corner; no direction can extend
    assert g.check_winner() is None


def test_check_winner_detects_tie():
    g = Game()
    for r in range(9):
        for c in range(9):
            g.board[r][c] = _tie_pattern_cell(r, c)
    assert g.check_winner() == 'tie'
    assert g.winner == 'tie'


# ---------- is_over ----------

def test_is_over_false_initially():
    assert Game().is_over() is False


def test_is_over_true_on_win():
    g = Game()
    for c in range(1, 6):
        g.board[0][c - 1] = 'X'
    g.check_winner()
    assert g.is_over() is True


def test_is_over_true_on_tie():
    g = Game()
    for r in range(9):
        for c in range(9):
            g.board[r][c] = _tie_pattern_cell(r, c)
    g.check_winner()
    assert g.is_over() is True


# ---------- render ----------

EMPTY_RENDER_NO_CARET = (
    "     1 2 3 4 5 6 7 8 9\n"
    "   +------------------+\n"
    "  1| . . . . . . . . .|\n"
    "  2| . . . . . . . . .|\n"
    "  3| . . . . . . . . .|\n"
    "  4| . . . . . . . . .|\n"
    "  5| . . . . . . . . .|\n"
    "  6| . . . . . . . . .|\n"
    "  7| . . . . . . . . .|\n"
    "  8| . . . . . . . . .|\n"
    "  9| . . . . . . . . .|\n"
    "   +------------------+"
)


EMPTY_RENDER_ROW_4_SELECTED = (
    "     1 2 3 4 5 6 7 8 9\n"
    "   +------------------+\n"
    "  1| . . . . . . . . .|\n"
    "  2| . . . . . . . . .|\n"
    "  3| . . . . . . . . .|\n"
    "> 4| . . . . . . . . .|\n"
    "  5| . . . . . . . . .|\n"
    "  6| . . . . . . . . .|\n"
    "  7| . . . . . . . . .|\n"
    "  8| . . . . . . . . .|\n"
    "  9| . . . . . . . . .|\n"
    "   +------------------+"
)


def test_render_empty_board_no_caret():
    assert Game().render() == EMPTY_RENDER_NO_CARET


def test_render_empty_board_explicit_none_selected_row():
    assert Game().render(selected_row=None) == EMPTY_RENDER_NO_CARET


def test_render_row_4_selected():
    assert Game().render(selected_row=4) == EMPTY_RENDER_ROW_4_SELECTED


def test_render_marks_appear_in_correct_cells():
    g = Game()
    g.make_move(1, 1)  # X
    g.make_move(9, 9)  # O
    rendered = g.render()
    # Row 1: X at col 1, dots elsewhere
    assert "  1| X . . . . . . . .|" in rendered
    # Row 9: O at col 9
    assert "  9| . . . . . . . . O|" in rendered


def test_render_caret_appears_only_on_selected_row():
    rendered = Game().render(selected_row=7)
    lines = rendered.split("\n")
    # Find the line for row 7 — it should start with "> 7|"
    matching = [line for line in lines if line.startswith("> ")]
    assert len(matching) == 1
    assert matching[0].startswith("> 7|")


# ---------- reset ----------

def test_reset_clears_board_and_sets_starter():
    g = Game()
    g.make_move(5, 5)
    g.make_move(1, 1)
    g.check_winner()
    g.reset(starting_player='O')
    assert g.board == _empty_board()
    assert g.current_player == 'O'
    assert g.starting_player == 'O'
    assert g.winner is None
