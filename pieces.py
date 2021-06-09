from constants import *
from Logic import Logic


def piece_from_abreviation(abreviation, i, j):
    if abreviation.lower() == abreviation:
        color = "black"
    else:
        color = "white"

    return dico[abreviation.lower()](color, i, j)


class Piece:
    def __init__(self, color, i, j):
        self.has_moved = False
        self.color = color
        self.i = i
        self.j = j
        self.abreviation = None

    def possible_moves(self):
        """ Retourne les moves qui seraient possibles s'il n'y avait aucune piece sur l'echequier"""

    def legal_moves(self, board):
        """Retourne tous les moves légaux dans une position pour une piece"""


class Pawn(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.abreviation = "p"
        self.image = globals()[f"{self.abreviation}_image"]
        self.direction = -1 if self.color == 'white' else +1

    def possible_moves(self):
        i = self.i
        j = self.j
        move_list = [(i, j + self.direction)]

    def legal_moves(self, board: Logic):
        piece_at = board.piece_at
        i, j = self.i, self.j
        dir = self.direction
        retunrlist = []

        # move devant
        if (piece_at(i + dir, j)) is None:
            retunrlist.append((i + dir, j))
            if i == 1 and self.color == "black" or i == 6 and self.color == "white":
                if piece_at(i + 2 * dir, j) is None:
                    retunrlist.append((i + 2 * dir, j))

        # captures sur les cotés
        if piece_at(i + dir, j + 1).color != self.color:
            retunrlist.append((i + dir, j + 1))
        if piece_at(i + dir, j - 1).color != self.color:
            retunrlist.append((i + dir, j - 1))

        return retunrlist


class Bishop(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.abreviation = "b"
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def legal_moves(self, board: Logic):
        piece_at = board.piece_at


class Rook(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.abreviation = "r"
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def legal_moves(self, board: Logic):
        piece_at = board.piece_at


class Knight(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.abreviation = "n"
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def legal_moves(self, board: Logic):
        piece_at = board.piece_at


class Queen(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.abreviation = "q"
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def legal_moves(self, board: Logic):
        piece_at = board.piece_at


class King(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.abreviation = "k"
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def legal_moves(self, board: Logic):
        piece_at = board.piece_at


dico = {"p": Pawn, "r": Rook, "b": Bishop, "n": Knight, "q": Queen, "k": King}
