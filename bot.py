import random
from Logic import Logic


class Edouard:
    def __init__(self, color):
        self.color = color

    def play_random(self, board: Logic):
        return random.choice(board.legal_moves(self.color))
