import random


class ComputerAI:
    @staticmethod
    def random_move(game):
        return random.choice(game.available_moves())
