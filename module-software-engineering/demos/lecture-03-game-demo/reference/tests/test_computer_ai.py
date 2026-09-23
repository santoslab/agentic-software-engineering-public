import random

from game import Game
from computer_ai import ComputerAI


def test_random_move_returns_position_in_available_moves():
    """SPECS §5.2: random_move picks from game.available_moves()."""
    g = Game()
    g.make_move(5, 5)  # X plays center; (5, 5) is now occupied.
    move = ComputerAI.random_move(g)
    assert move in g.available_moves()


def test_random_move_when_only_one_cell_remains():
    """SPECS §5.2: when one cell remains, random_move must return that cell."""
    g = Game()
    # Fill 80 cells via direct assignment (allowed by SPECS §9.3 for setup);
    # leave (4, 4) (internal (3, 3)) empty.
    for r in range(9):
        for c in range(9):
            if (r, c) != (3, 3):
                g.board[r][c] = 'X'
    assert g.available_moves() == [(4, 4)]
    assert ComputerAI.random_move(g) == (4, 4)


def test_random_move_always_returns_valid_position_over_many_calls():
    """SPECS §5.2: across many randomly partially-filled boards, every result must be
    a member of available_moves(). Pre-filling forces the 'must be available' contract
    to bite — on an empty board, every move trivially satisfies it."""
    rng = random.Random(12345)
    for _ in range(100):
        g = Game()
        # Place 10-70 X marks randomly via direct assignment.
        prefill_count = rng.randint(10, 70)
        cells = [(r, c) for r in range(9) for c in range(9)]
        for r, c in rng.sample(cells, prefill_count):
            g.board[r][c] = 'X'
        move = ComputerAI.random_move(g)
        assert move in g.available_moves()
