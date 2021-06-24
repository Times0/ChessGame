import random


class Edouard:
    def __init__(self, color):
        self.color = color

    def play_random(self, board) -> (int, int, int, int):
        choice = random.choice(board.legal_moves(self.color))
        return choice
