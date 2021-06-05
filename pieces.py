from constants import *


def piece_from_abreviation(abreviation):
    if abreviation.lower() == abreviation:
        color = "black"
    else:
        color = "white"

    return dico[abreviation.lower()](color)


class Piece:
    pass


class Pawn(Piece):
    def __init__(self, color):
        self.color = color
        self.abreviation = "p"
        if self.color == "white":
            self.abreviation = self.abreviation.upper()
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self, i, j, board):
        pass


class Rook(Piece):
    def __init__(self, color):
        self.color = color
        self.abreviation = "r"
        if self.color == "white":
            self.abreviation = self.abreviation.upper()
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self, i, j, board):
        pass


class Bishop(Piece):
    def __init__(self, color):
        self.color = color
        self.abreviation = "b"
        if self.color == "white":
            self.abreviation = self.abreviation.upper()
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self, i, j, board):
        pass


class Knight(Piece):
    def __init__(self, color):
        self.color = color
        self.abreviation = "n"
        if self.color == "white":
            self.abreviation = self.abreviation.upper()
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self, i, j, board):
        pass


class Queen(Piece):
    def __init__(self, color):
        self.color = color
        self.abreviation = "q"
        if self.color == "white":
            self.abreviation = self.abreviation.upper()
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self, i, j, board):
        pass


class King(Piece):
    def __init__(self, color):
        self.color = color
        self.abreviation = "k"
        if self.color == "white":
            self.abreviation = self.abreviation.upper()
        self.image = globals()[f"{self.abreviation}_image"]

    def possible_moves(self, i, j, board):
        pass


class NonePiece(Piece):
    def __init__(self, color=None):
        self.color = color
        self.abreviation = " "
        self.image = None

    def possible_moves(self):
        return None


dico = {"p": Pawn, "r": Rook, "b": Bishop, "n": Knight, "q": Queen, "k": King, " ": NonePiece}
