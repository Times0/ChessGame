from itertools import product

from constants import *
from fonctions import *


def piece_from_abreviation(abreviation, i, j):
    if abreviation.lower() == abreviation:
        color = "black"
    else:
        color = "white"

    return dico[abreviation.lower()](color, i, j)


class Piece:
    def __init__(self, color, i, j):
        self.never_moved = True
        self.color = color
        self.i = i
        self.j = j
        self.abreviation = None

    def set_abreviation(self, name):
        inv_map = {v: k for k, v in dico.items()}
        abreviation = inv_map[name]
        if self.color == "white":
            abreviation = abreviation.upper()
        self.abreviation = abreviation

    def _legal_moves(self, board):
        pass

    def legal_moves(self, board):
        """Retourne tous les moves légaux dans une position pour une piece"""
        if self.color != board.turn:
            return []
        return self._legal_moves(board)

    def moved(self, dest_i, dest_j):
        self.i, self.j = dest_i, dest_j
        self.never_moved = False


class Pawn(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)

        self.image = globals()[f"{self.abreviation}_image"]
        self.direction = -1 if self.color == 'white' else +1

    def _legal_moves(self, board):
        piece_at = board.piece_at
        i, j = self.i, self.j
        dir = self.direction
        returnlist = []

        # move devant
        i1 = i + dir  # case devant le pion (relativement)
        if isInbounds(i1, j) and not piece_at(i1, j):
            returnlist.append((i1, j))
            if self.never_moved:
                i2 = i1 + dir  # deux cases devant le pion
                if not piece_at(i2, j):
                    returnlist.append((i2, j))

        # captures
        for j in [j - 1, j + 1]:
            if isInbounds(i1, j) and piece_at(i1, j) and piece_at(i1, j).color != self.color:
                returnlist.append((i1, j))
        return returnlist


class Bishop(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def _legal_moves(self, board):
        piece_at = board.piece_at


class Rook(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def _legal_moves(self, board):
        piece_at = board.piece_at


class Knight(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def _legal_moves(self, board):
        i, j = self.i, self.j
        moves = list(product([i - 1, i + 1], [j - 2, j + 2])) + list(product([i - 2, i + 2], [j - 1, j + 1]))
        return [move for move in moves if isInbounds(*move)]


class Queen(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def _legal_moves(self, board):
        piece_at = board.piece_at


class King(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def _legal_moves(self, board):
        piece_at = board.piece_at


dico = {"p": Pawn, "r": Rook, "b": Bishop, "n": Knight, "q": Queen, "k": King}
