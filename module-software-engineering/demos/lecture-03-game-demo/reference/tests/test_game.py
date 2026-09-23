import pytest

from game import Game


# ---------- Helpers ----------

def _tie_pattern(r, c):
    """SPECS §4.2: a verified anti-5 pattern. 'O' at (3r+c)%5==0 else 'X'.
    By construction this leaves no run of 5 in any row, column, or diagonal."""
    return 'O' if (3 * r + c) % 5 == 0 else 'X'


def _fill_tie_board(g):
    for r in range(9):
        for c in range(9):
            g.board[r][c] = _tie_pattern(r, c)


# ---------- __init__ (SPECS §5.1) ----------

def test_init_defaults():
    """SPECS §5.1: __init__ defaults to starting_player='X' and an empty 9x9 board."""
    g = Game()
    assert g.board == [[None] * 9 for _ in range(9)]
    assert g.current_player == 'X'
    assert g.starting_player == 'X'
    assert g.winner is None


def test_init_with_o_start():
    """SPECS §5.1: __init__ honors a non-default starting_player."""
    g = Game(starting_player='O')
    assert g.current_player == 'O'
    assert g.starting_player == 'O'
    assert g.winner is None


# ---------- make_move success (SPECS §5.1) ----------

@pytest.mark.parametrize("row,col", [
    (1, 1), (1, 9), (5, 5), (9, 1), (9, 9), (3, 7), (8, 2),
])
def test_make_move_places_mark_at_correct_cell(row, col):
    """SPECS §3.2 / §5.1: make_move(row, col) writes to board[row-1][col-1]."""
    g = Game()
    assert g.make_move(row, col) is True
    assert g.board[row - 1][col - 1] == 'X'
    for r in range(9):
        for c in range(9):
            if (r, c) != (row - 1, col - 1):
                assert g.board[r][c] is None


def test_make_move_switches_player_x_to_o():
    """SPECS §5.1: make_move switches current_player after a successful move."""
    g = Game()
    g.make_move(5, 5)
    assert g.current_player == 'O'


def test_make_move_switches_player_o_to_x():
    """SPECS §5.1: switching works in both directions (covers the ternary's other branch)."""
    g = Game(starting_player='O')
    g.make_move(5, 5)
    assert g.current_player == 'X'


# ---------- make_move failures (SPECS §5.1, §6.2) ----------

@pytest.mark.parametrize("bad_row", ["5", 5.0, None, [], (1, 1)])
def test_make_move_rejects_non_int_row(bad_row):
    """SPECS §5.1: make_move returns False when row is not int; state unchanged."""
    g = Game()
    assert g.make_move(bad_row, 5) is False
    assert g.board == [[None] * 9 for _ in range(9)]
    assert g.current_player == 'X'


@pytest.mark.parametrize("bad_col", ["5", 5.0, None, [], (1, 1)])
def test_make_move_rejects_non_int_col(bad_col):
    """SPECS §5.1: make_move returns False when col is not int; state unchanged."""
    g = Game()
    assert g.make_move(5, bad_col) is False
    assert g.board == [[None] * 9 for _ in range(9)]
    assert g.current_player == 'X'


@pytest.mark.parametrize("row,col", [
    (0, 5), (10, 5), (-1, 5), (100, 5),
    (5, 0), (5, 10), (5, -1), (5, 100),
])
def test_make_move_rejects_out_of_range(row, col):
    """SPECS §5.1: make_move returns False for row/col outside 1-9; state unchanged."""
    g = Game()
    assert g.make_move(row, col) is False
    assert g.board == [[None] * 9 for _ in range(9)]
    assert g.current_player == 'X'


def test_make_move_rejects_occupied_cell():
    """SPECS §5.1: make_move returns False on an occupied cell; current_player unchanged."""
    g = Game()
    g.make_move(5, 5)
    assert g.current_player == 'O'
    assert g.make_move(5, 5) is False
    assert g.current_player == 'O'
    assert g.board[4][4] == 'X'


def test_make_move_rejected_after_game_over():
    """SPECS §5.1: a move after the game is over returns False and changes nothing."""
    g = Game()
    for c in range(2, 7):
        g.board[4][c] = 'X'
    assert g.check_winner() == 'X'
    board_before = [row[:] for row in g.board]
    player_before = g.current_player
    assert g.make_move(1, 1) is False
    assert g.board == board_before
    assert g.current_player == player_before


# ---------- available_moves (SPECS §5.1) ----------

def test_available_moves_empty_board():
    """SPECS §5.1: all 81 cells available on an empty board, in row-major order."""
    g = Game()
    moves = g.available_moves()
    assert len(moves) == 81
    assert moves[0] == (1, 1)
    assert moves[8] == (1, 9)
    assert moves[9] == (2, 1)
    assert moves[-1] == (9, 9)


def test_available_moves_shrinks_after_moves():
    """SPECS §5.1: cells become unavailable after make_move."""
    g = Game()
    g.make_move(5, 5)
    g.make_move(1, 1)
    remaining = g.available_moves()
    assert (5, 5) not in remaining
    assert (1, 1) not in remaining
    assert len(remaining) == 79


def test_available_moves_empty_on_full_board():
    """SPECS §5.1: no cells available on a full board."""
    g = Game()
    _fill_tie_board(g)
    assert g.available_moves() == []


# ---------- check_winner: directions (SPECS §4.1) ----------

def test_check_winner_horizontal():
    """SPECS §4.1: 5+ same-symbol cells in a row wins (horizontal)."""
    g = Game()
    for c in range(2, 7):
        g.board[4][c] = 'X'
    assert g.check_winner() == 'X'
    assert g.winner == 'X'


def test_check_winner_vertical():
    """SPECS §4.1: 5+ same-symbol cells in a column wins (vertical)."""
    g = Game()
    for r in range(2, 7):
        g.board[r][4] = 'O'
    assert g.check_winner() == 'O'
    assert g.winner == 'O'


def test_check_winner_diagonal_down_right():
    """SPECS §4.1: 5+ same-symbol cells along ↘ diagonal wins."""
    g = Game()
    for i in range(5):
        g.board[2 + i][1 + i] = 'X'
    assert g.check_winner() == 'X'
    assert g.winner == 'X'


def test_check_winner_diagonal_up_right():
    """SPECS §4.1: 5+ same-symbol cells along ↗ diagonal wins."""
    g = Game()
    for i in range(5):
        g.board[6 - i][2 + i] = 'O'
    assert g.check_winner() == 'O'
    assert g.winner == 'O'


def test_check_winner_overline_counts():
    """SPECS §4.1: overlines (6+) count as a win."""
    g = Game()
    for c in range(9):
        g.board[3][c] = 'X'
    assert g.check_winner() == 'X'
    assert g.winner == 'X'


def test_check_winner_none_on_empty_board():
    """SPECS §5.1: check_winner returns None when no moves have been made."""
    g = Game()
    assert g.check_winner() is None
    assert g.winner is None


def test_check_winner_none_with_partial_runs():
    """SPECS §4.1: runs shorter than 5 do not win.

    Exercises the False branch of `all(...)` in each directional loop:
    a non-None first cell exists but the 5-window is not all the same symbol.
    """
    g = Game()
    # Horizontal 4-X run (not 5).
    g.board[0][0] = g.board[0][1] = g.board[0][2] = g.board[0][3] = 'X'
    # Vertical 4-O run.
    g.board[1][5] = g.board[2][5] = g.board[3][5] = g.board[4][5] = 'O'
    # Diagonal partial run.
    g.board[6][0] = g.board[7][1] = 'X'
    assert g.check_winner() is None
    assert g.winner is None


# ---------- check_winner: tie & precedence (SPECS §4.2, §4.3) ----------

def test_check_winner_detects_tie():
    """SPECS §4.2: tie = fully filled board with no winning line."""
    g = Game()
    _fill_tie_board(g)
    assert g.check_winner() == 'tie'
    assert g.winner == 'tie'


def test_check_winner_winner_over_tie_precedence():
    """SPECS §4.3: when the final move both fills the board AND completes a
    5-line, winner wins (tie is only declared when no winner exists)."""
    g = Game()
    _fill_tie_board(g)
    # Remove (0, 5) — was 'O' in the tie pattern — to open one cell.
    # In the tie pattern, row 0 cols 1-4 are 'X' (col 0 was 'O', col 5 was 'O').
    # Filling (0, 5) with 'X' creates a horizontal 5-X run at cols 1-5.
    g.board[0][5] = None
    g.current_player = 'X'
    assert g.make_move(1, 6) is True
    assert g.check_winner() == 'X'
    assert g.winner == 'X'


# ---------- is_over (SPECS §5.1) ----------

def test_is_over_false_initially():
    """SPECS §5.1: is_over is False on a fresh game."""
    assert Game().is_over() is False


def test_is_over_true_on_win():
    """SPECS §5.1: is_over is True after a winning line is detected."""
    g = Game()
    for c in range(5):
        g.board[0][c] = 'X'
    g.check_winner()
    assert g.is_over() is True


def test_is_over_true_on_tie():
    """SPECS §5.1, §4.2: a tie is a terminal state."""
    g = Game()
    _fill_tie_board(g)
    g.check_winner()
    assert g.is_over() is True


# ---------- render (SPECS §7.2) ----------

EMPTY_BOARD = (
    "    1 2 3 4 5 6 7 8 9\n"
    "  +-------------------+\n"
    "1 | . . . . . . . . . |\n"
    "2 | . . . . . . . . . |\n"
    "3 | . . . . . . . . . |\n"
    "4 | . . . . . . . . . |\n"
    "5 | . . . . . . . . . |\n"
    "6 | . . . . . . . . . |\n"
    "7 | . . . . . . . . . |\n"
    "8 | . . . . . . . . . |\n"
    "9 | . . . . . . . . . |\n"
    "  +-------------------+"
)

MID_GAME_BOARD = (
    "    1 2 3 4 5 6 7 8 9\n"
    "  +-------------------+\n"
    "1 | . . . . . . . . . |\n"
    "2 | . . . . . . . . . |\n"
    "3 | . . X . . . . . . |\n"
    "4 | . . . O . . . . . |\n"
    "5 | . . . . . . . . . |\n"
    "6 | . . . . . . . . . |\n"
    "7 | . . . . . . . . . |\n"
    "8 | . . . . . . . . . |\n"
    "9 | . . . . . . . . . |\n"
    "  +-------------------+"
)


def test_render_empty_board():
    """SPECS §7.2: empty board byte-exact format."""
    assert Game().render() == EMPTY_BOARD


def test_render_mid_game_byte_exact():
    """SPECS §7.2: mid-game render with X at (3,3) and O at (4,4) matches the spec mockup."""
    g = Game()
    g.make_move(3, 3)
    g.make_move(4, 4)
    assert g.render() == MID_GAME_BOARD


def test_render_full_board_contains_expected_marks():
    """SPECS §7.2: render works on a fully populated board (covers the ternary's
    'cell is not None' branch for every cell)."""
    g = Game()
    _fill_tie_board(g)
    rendered = g.render()
    # Every line includes only X, O, label digits, and box characters — no dots.
    for line in rendered.splitlines():
        if line.startswith("  +") or line.startswith("    "):
            continue
        assert "." not in line
    # Spot-check a few cells per the tie pattern.
    assert g.board[0][0] == 'O'
    assert g.board[0][1] == 'X'
    assert g.board[4][4] == 'X'
