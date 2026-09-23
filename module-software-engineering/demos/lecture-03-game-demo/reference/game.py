class Game:
    def __init__(self, starting_player='X'):
        """Initialize an empty 9x9 board with the given starting player.

        Params: starting_player — 'X' or 'O' (default 'X').
        """
        self.board = [[None] * 9 for _ in range(9)]
        self.current_player = starting_player
        self.starting_player = starting_player
        self.winner = None

    def make_move(self, row, col):
        """Apply the current player's mark at (row, col) and switch turn.

        Params: row, col — ints in 1-9.
        Returns: True on success; False if the game is over, row/col is not an
            int in 1-9, or the cell is already occupied (state unchanged in
            each case). SPECS §5.1.
        """
        if self.winner is not None:
            return False
        if not isinstance(row, int) or not isinstance(col, int):
            return False
        if not (1 <= row <= 9 and 1 <= col <= 9):
            return False
        if self.board[row - 1][col - 1] is not None:
            return False
        self.board[row - 1][col - 1] = self.current_player
        self.current_player = 'O' if self.current_player == 'X' else 'X'
        return True

    def available_moves(self):
        """List every empty cell on the board, in row-major order.

        Returns: list of (row, col) tuples; rows/cols are 1-9.
        """
        return [(r + 1, c + 1)
                for r in range(9)
                for c in range(9)
                if self.board[r][c] is None]

    def check_winner(self):
        """Scan for a 5+-in-a-row run or a tie and update self.winner.

        Returns: 'X' or 'O' if that player has 5+ consecutive cells in any
            row, column, or diagonal; 'tie' if the board is full with no
            winner; None if the game is still ongoing.
        """
        # Horizontal 5-windows.
        for r in range(9):
            for c in range(5):
                first = self.board[r][c]
                if first is not None and all(self.board[r][c + i] == first for i in range(5)):
                    self.winner = first
                    return self.winner

        # Vertical 5-windows.
        for c in range(9):
            for r in range(5):
                first = self.board[r][c]
                if first is not None and all(self.board[r + i][c] == first for i in range(5)):
                    self.winner = first
                    return self.winner

        # Diagonal down-right (↘).
        for r in range(5):
            for c in range(5):
                first = self.board[r][c]
                if first is not None and all(self.board[r + i][c + i] == first for i in range(5)):
                    self.winner = first
                    return self.winner

        # Diagonal up-right (↗).
        for r in range(4, 9):
            for c in range(5):
                first = self.board[r][c]
                if first is not None and all(self.board[r - i][c + i] == first for i in range(5)):
                    self.winner = first
                    return self.winner

        if all(cell is not None for row in self.board for cell in row):
            self.winner = 'tie'
            return self.winner

        self.winner = None
        return self.winner

    def is_over(self):
        """Whether the game has ended (win or tie).

        Returns: True if self.winner is set; False if still ongoing.
        """
        return self.winner is not None

    def render(self):
        """Render the board as a string per SPECS §7.2 (byte-exact format).

        Returns: multi-line string. Empty cells appear as '.', occupied cells
            as 'X' or 'O'. Row/column labels are always visible.
        """
        header = "    " + " ".join(str(c) for c in range(1, 10))
        border = "  +" + "-" * 19 + "+"
        lines = [header, border]
        for r in range(9):
            cells = " ".join(
                self.board[r][c] if self.board[r][c] is not None else "."
                for c in range(9)
            )
            lines.append(f"{r + 1} | {cells} |")
        lines.append(border)
        return "\n".join(lines)
