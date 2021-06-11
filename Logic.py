# toute la partie back, juste la logique
from pieces import *
import numpy as np


class Logic:
    def __init__(self, fen):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.load_fen(fen)

        self.turn = "white"
        # variables pour les privilèges de roquer
        self.q, self.Q, self.k, self.K = 1, 1, 1, 1

    def load_fen(self, fen):
        new_board = [[None for _ in range(8)] for _ in range(8)]
        remaining = None
        i, j = 0, 0
        for k, char in enumerate(fen):
            if char == " ":
                remaining = fen[k + 1:]
                break
            if char == "/":
                i += 1
                j = 0
            elif char.isnumeric():
                j += int(char)
            elif char.isalpha():
                new_board[i][j] = piece_from_abreviation(char, i, j)
                j += 1
            if i == 7 and j == 8:  # to finish
                break
        self.board = new_board.copy()

    def piece_at(self, i, j):
        return self.board[i][j]

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
        if piece is None:
            raise Exception

        self.board[i][j] = None
        self.board[dest_i][dest_j] = piece
        self.board[dest_i][dest_j].moved(dest_i, dest_j)
        self.switch_turn()

    def switch_turn(self) -> None:
        if self.turn == "white":
            self.turn = "black"
        else:
            self.turn = "white"

    def __repr__(self):
        returnboard = [[" " for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is None:
                    returnboard[i][j] = " "
                else:
                    returnboard[i][j] = self.board[i][j].abreviation

        return str(np.matrix(returnboard))
