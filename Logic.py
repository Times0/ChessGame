# toute la partie back, juste la logique
from pieces import *


class Logic:
    def __init__(self, fen):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.load_fen(fen)
        self.turn = 0

    def load_fen(self, fen):
        i, j = 0, 0
        for char in fen:
            if char == "/":
                i += 1
                j = 0
            elif char.isnumeric():
                j += int(char) - 1
            elif char.isalpha():
                self.board[i][j] = piece_from_abreviation(char)
                j += 1
            if i == 7 and j == 8:  # to finish
                break
