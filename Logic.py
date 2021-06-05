# toute la partie back, juste la logique
from pieces import *
import numpy as np


class Logic:
    def __init__(self, fen):
        self.board = [[NonePiece() for _ in range(8)] for _ in range(8)]
        self.load_fen(fen)
        self.turn = "white"

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

    def isMovelegal(self, i, j, destination_i, destination_j) -> bool:
        piece = self.board[i][j]
        if piece is None or piece.color != self.turn:
            return False

        possible_moves = piece.possible_moves(i, j)
        legal_moves = list()
        if (destination_i, destination_j) in legal_moves:
            self.move(i, j, destination_i, destination_j)
            return 1

    def move(self, i: int, j: int, dest_i, dest_j) -> None:
        """
        Moves a piece to a square regardless of rules
        i,j origin coordinates, dest_i,dest_j destination coordinates
        :return: None
        """
        piece = self.board[i][j]
        if type(piece) == NonePiece:
            raise Exception
        self.board[i][j] = NonePiece()
        self.board[dest_i][dest_j] = piece

    def __repr__(self):
        returnboard = [[" " for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                returnboard[i][j] = self.board[i][j].abreviation

        return str(np.matrix(returnboard))


a = Logic(STARTINGPOSFEN)
print(a)
a.move(6, 4, 4, 4)
print(a)