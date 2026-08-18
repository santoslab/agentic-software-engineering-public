BOARD_SIZE = 9
WIN_LENGTH = 5

# (dr, dc) for rightward, downward, down-right diagonal, down-left diagonal.
_DIRECTIONS = ((0, 1), (1, 0), (1, 1), (1, -1))


def _is_valid_coord(value):
    return isinstance(value, int) and not isinstance(value, bool) and 1 <= value <= BOARD_SIZE


class Game:
    def __init__(self, starting_player='X'):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = starting_player
        self.starting_player = starting_player
        self.winner = None

    def make_move(self, row, col):
        if not (_is_valid_coord(row) and _is_valid_coord(col)):
            return False
        if self.board[row - 1][col - 1] is not None:
            return False
        self.board[row - 1][col - 1] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def available_moves(self):
        return [
            (r, c)
            for r in range(1, BOARD_SIZE + 1)
            for c in range(1, BOARD_SIZE + 1)
            if self.board[r - 1][c - 1] is None
        ]

    def row_has_space(self, row):
        if not _is_valid_coord(row):
            return False
        return any(cell is None for cell in self.board[row - 1])

    def check_winner(self):
        for r in range(BOARD_SIZE):
            for c in range(BOARD_SIZE):
                mark = self.board[r][c]
                if mark is None:
                    continue
                for dr, dc in _DIRECTIONS:
                    end_r = r + (WIN_LENGTH - 1) * dr
                    end_c = c + (WIN_LENGTH - 1) * dc
                    if not (0 <= end_r < BOARD_SIZE and 0 <= end_c < BOARD_SIZE):
                        continue
                    if all(self.board[r + k * dr][c + k * dc] == mark for k in range(WIN_LENGTH)):
                        self.winner = mark
                        return self.winner
        if all(cell is not None for row in self.board for cell in row):
            self.winner = 'tie'
            return self.winner
        self.winner = None
        return self.winner

    def is_over(self):
        return self.winner is not None

    def render(self, selected_row=None):
        lines = ["     1 2 3 4 5 6 7 8 9", "   +" + "-" * 18 + "+"]
        for r in range(1, BOARD_SIZE + 1):
            margin = "> " if selected_row == r else "  "
            cells = "".join(
                f" {cell if cell is not None else '.'}"
                for cell in self.board[r - 1]
            )
            lines.append(f"{margin}{r}|{cells}|")
        lines.append("   +" + "-" * 18 + "+")
        return "\n".join(lines)

    def reset(self, starting_player):
        self.board = [[None] * BOARD_SIZE for _ in range(BOARD_SIZE)]
        self.current_player = starting_player
        self.starting_player = starting_player
        self.winner = None
