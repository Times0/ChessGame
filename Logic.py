import numpy as np


# toute la partie back, juste la logique

class Logic:
    def __init__(self):

        self.board = [["" for i in range(8)] for i in range(8)]
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
                self.board[i][j] = char
                j += 1
            if i == 7 and j == 8:  # to finish
                break
