"""Board positions and move sequences shared by the tests (tasks.md, Conventions)."""

# A full board with no line longer than 2: X on 41 squares, O on 40.
DRAW_PATTERN = tuple("XXOOXXOOX" if r % 2 == 1 else "OOXXOOXXO" for r in range(1, 10))

_X_SQUARES = tuple(
    (r, c) for r in range(1, 10) for c in range(1, 10) if DRAW_PATTERN[r - 1][c - 1] == "X"
)
_O_SQUARES = tuple(
    (r, c) for r in range(1, 10) for c in range(1, 10) if DRAW_PATTERN[r - 1][c - 1] == "O"
)

# The 81 squares of DRAW_PATTERN in a legal order: X, O, X, O, ..., ending with X's 41st.
# The final board has no five in a line, so no earlier board does either.
DRAW_MOVES = tuple(sq for pair in zip(_X_SQUARES, _O_SQUARES) for sq in pair) + _X_SQUARES[-1:]

# X wins on the ninth move along row 5.
X_WINS_MOVES = ((5, 1), (1, 1), (5, 2), (1, 2), (5, 3), (1, 3), (5, 4), (1, 4), (5, 5))

# O wins on the tenth move along row 1.
O_WINS_MOVES = (
    (9, 1), (1, 1), (9, 3), (1, 2), (9, 5), (1, 3), (9, 7), (1, 4), (7, 1), (1, 5),
)
