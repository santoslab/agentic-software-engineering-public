import random


class ComputerAI:
    @staticmethod
    def random_move(game):
        """Pick a uniformly-random move from the game's available cells.

        Params: game — Game instance; must have at least one available move.
        Returns: (row, col) tuple, both 1-9.
        """
        return random.choice(game.available_moves())
