from constants import *


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

    def possible_moves(self):
        """ Retourne les moves qui seraient possibles s'il n'y avait aucune piece sur l'echequier"""

    def legal_moves(self, board):
        """Retourne tous les moves légaux dans une position pour une piece"""


class Pawn(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)

        self.image = globals()[f"{self.abreviation}_image"]
        self.direction = -1 if self.color == 'white' else +1

    def possible_moves(self):
        i = self.i
        j = self.j
        move_list = [(i, j + self.direction)]

    def legal_moves(self, board):
        piece_at = board.piece_at
        i, j = self.i, self.j
        dir = self.direction
        returnlist = []

        # move devant
        i1 = i + dir  # case devant le pion (relativement)
        if not piece_at(i1, j):
            returnlist.append((i1, j))
            if self.never_moved:
                i2 = i1 + dir  # deux cases devant le pion
                if not piece_at(i2, j):
                    returnlist.append((i2, j))

        # captures

        for j in range(j - 1, j + 1):
            if piece_at(i1, j) and piece_at(i1, j).color != self.color:
                returnlist.append((i1, j))

        return returnlist


class Bishop(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def legal_moves(self, board):
        piece_at = board.piece_at


class Rook(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def legal_moves(self, board):
        piece_at = board.piece_at


class Knight(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def legal_moves(self, board):
        piece_at = board.piece_at


class Queen(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def legal_moves(self, board):
        piece_at = board.piece_at


class King(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self):
        pass

    def legal_moves(self, board):
        piece_at = board.piece_at


dico = {"p": Pawn, "r": Rook, "b": Bishop, "n": Knight, "q": Queen, "k": King}
