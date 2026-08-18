import random

from game import Game
from computer_ai import ComputerAI


def test_random_move_returns_tuple_in_available_moves():
    g = Game()
    g.make_move(5, 5)
    move = ComputerAI.random_move(g)
    assert isinstance(move, tuple) and len(move) == 2
    assert move in g.available_moves()


def test_random_move_when_only_one_cell_remains():
    g = Game()
    # Fill the whole board except for (4, 7).
    for r in range(9):
        for c in range(9):
            if (r, c) != (3, 6):
                g.board[r][c] = 'X' if (r + c) % 2 == 0 else 'O'
    assert g.available_moves() == [(4, 7)]
    assert ComputerAI.random_move(g) == (4, 7)


def test_random_move_always_returns_valid_position_over_many_calls():
    rng = random.Random(12345)
    for _ in range(100):
        g = Game()
        # Randomly fill some cells.
        prefill_count = rng.randint(1, 50)
        cells = rng.sample([(r, c) for r in range(9) for c in range(9)], prefill_count)
        for r, c in cells:
            g.board[r][c] = 'X'
        move = ComputerAI.random_move(g)
        assert move in g.available_moves()
