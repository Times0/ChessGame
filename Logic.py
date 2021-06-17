import itertools

import numpy as np
from fonctions import *
from constants import *
from itertools import product


class Logic:
    def __init__(self, fen):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.load_fen(fen)

        self.turn = "white"
        # variables pour les privilèges de roquer
        self.castle_rights = "kqKQ"  # kingside, queenside
        # ["game_on","blackismated", "whiteismated", "draw"]
        self.state = "game_on"

    def load_fen(self, fen):
        board = []
        i, j = 0, 0
        parts = fen.split(" ")

        # part 1
        for row in parts[0].split("/"):
            b_row = []
            for c in row:
                if c == " ":
                    break
                elif c.isnumeric():
                    b_row.extend([None] * int(c))
                    j += int(c)
                elif c.isalpha():
                    b_row.append(piece_from_abreviation(c, i, j))
                    j += 1
            board.append(b_row)
            i += 1
            j = 0

        for i, part in enumerate(parts[1:]):

            if i == 0:
                self.turn = "white" if part == "w" else "black"

            elif i == 1:
                self.castle_rights = part[2]

        self.board = board.copy()

    def get_fen(self):
        returnfen = ""
        # liste des caractèrs représentant les pièces
        i, j = 0, 0
        while i < 8:
            while j < 8:
                # si on a un espace
                if not self.piece_at(i, j):
                    c = 0
                    while j < 8 and self.piece_at(i, j) is None:
                        c += 1
                        j += 1
                    returnfen += str(c)
                else:
                    returnfen += self.piece_at(i, j).abreviation
                    j += 1
            returnfen += "/"
            i += 1
            j = 0
        # propriétés de l'échequier :

        returnfen += f" {'w' if self.turn == 'white' else 'black'}"
        returnfen += f" {self.castle_rights}"
        return returnfen

    def piece_at(self, i, j):
        return self.board[i][j]

    def cases_attacked_by(self, color):
        L = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and piece.color == color:
                    L.extend(piece.attacking_squares(self))
        return list(set(L))

    def legal_moves(self, color):
        returnlist = []
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if piece and piece.color == color:
                    if piece.legal_moves(self):
                        returnlist.append(piece.legal_moves(self))
        return returnlist

    def king_coord(self, color):
        king_i, king_j = 0, 0
        for i in range(8):
            for j in range(8):
                if self.piece_at(i, j) and self.board[i][j].abreviation == ("K" if color == "white" else "k"):
                    king_i, king_j = i, j
                    return king_i, king_j

    def isIncheck(self, color):
        i, j = self.king_coord(color)
        return (i, j) in self.cases_attacked_by(("white" if color == "black" else "black"))

    def isStalemate(self, color):
        return self.legal_moves(color) == []

    def king(self, color):
        i, j = self.king_coord(color)
        return self.board[i][j]

    def update_game_state(self):
        """ possible states : ["blackismated","whiteismated","draw"]"""
        for color in ["white", "black"]:
            reduced_l = list(itertools.chain(*self.legal_moves(color)))
            if self.isIncheck(color) and reduced_l == []:
                self.state = color + "ismated"

    def move(self, i: int, j: int, dest_i, dest_j) -> None:
        """
        Moves a piece to a square regardless of rules
        i,j origin coordinates, dest_i,dest_j destination coordinates
        :return: None
        """
        piece = self.board[i][j]
        if piece is None:
            print('no piece here')
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

    def almost_legal_moves(self, board):
        """Cette fonction est overriden pour chacune des pièces, elle renvoie les moves possible pour une pièce
        en prenant en compte les autres pièces de l'échequier mais sans prendre en compte les échecs au roi"""
        pass

    def legal_moves(self, board):
        """Retourne tous les moves légaux dans une position pour une piece"""
        returnlist = []
        if self.color != board.turn:
            return []
        for move in self.almost_legal_moves(board):
            virtual = Logic(board.get_fen())
            virtual.move(self.i, self.j, *move)
            if not virtual.isIncheck(self.color):
                returnlist.append(move)

        return returnlist

    def attacking_squares(self, board):
        return self.almost_legal_moves(board)

    def moved(self, dest_i, dest_j):
        self.i, self.j = dest_i, dest_j
        self.never_moved = False


class Pawn(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)

        self.image = globals()[f"{self.abreviation}_image"]
        self.direction = -1 if self.color == 'white' else +1

    def almost_legal_moves(self, board):
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

    def attacking_squares(self, board):
        piece_at = board.piece_at
        i, j = self.i, self.j
        dir = self.direction
        i1 = i + dir
        returnlist = []
        # attacked squares
        for j in [j - 1, j + 1]:
            if isInbounds(i1, j) and (not piece_at(i1, j) or piece_at(i1, j).color != self.color):
                returnlist.append((i1, j))
        return returnlist


class Bishop(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def almost_legal_moves(self, board):
        piece_at = board.piece_at
        returnlist = []
        i, j = self.i, self.j
        for a, b in [[1, 1], [-1, 1], [1, -1],
                     [-1, -1]]:  # toutes les permutations de S2 , (ici écrire une liste avec for était bien plus long)
            for n in range(1, 8 + 1):  # on ne teste pas la case sur laquelle il y a déjà notre pièce
                i1, j1 = i + a * n, j + b * n

                if isInbounds(i1, j1):
                    if (not piece_at(i1, j1)) or piece_at(i1, j1).color != self.color:
                        # déplacement autorisé  ou capture
                        returnlist.append((i1, j1))
                    if piece_at(i1, j1):
                        break  # c'est cette ligne qui traduit la rupture de la 'ligne' si une pièce y est présente
        return returnlist


class Rook(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def almost_legal_moves(self, board):
        piece_at = board.piece_at
        returnlist = []
        i, j = self.i, self.j
        for a, b in [[1, 0], [-1, 0], [0, -1], [0, 1]]:
            for n in range(1, 8 + 1):  # on ne teste pas la case sur laquelle il y a déjà notre pièce
                i1, j1 = i + a * n, j + b * n
                if isInbounds(i1, j1):
                    if (not piece_at(i1, j1)) or piece_at(i1,
                                                          j1).color != self.color:  # déplacement autorisé  ou capture
                        returnlist.append((i1, j1))
                    if piece_at(i1, j1):
                        break  # rupture de la 'ligne' si une pièce y est présente
        return returnlist


class Knight(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def almost_legal_moves(self, board):
        piece_at = board.piece_at
        i, j = self.i, self.j
        moves = list(product([i - 1, i + 1], [j - 2, j + 2])) + list(product([i - 2, i + 2], [j - 1, j + 1]))
        return [move for move in moves if
                isInbounds(*move) and (not piece_at(*move) or piece_at(*move).color != self.color)]


class Queen(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def almost_legal_moves(self, board):
        piece_at = board.piece_at
        returnlist = []
        i, j = self.i, self.j
        for a, b in [[1, 0], [-1, 0], [0, -1], [0, 1], [1, 1], [-1, 1], [1, -1], [-1, -1]]:
            for n in range(1, 8 + 1):  # on ne teste pas la case sur laquelle il y a déjà notre pièce
                i1, j1 = i + a * n, j + b * n
                if isInbounds(i1, j1):
                    if (not piece_at(i1, j1)) or piece_at(i1,
                                                          j1).color != self.color:  # déplacement autorisé  ou capture
                        returnlist.append((i1, j1))
                    if piece_at(i1, j1):
                        break  # rupture de la 'ligne' si une pièce y est présente
        return returnlist


class King(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.image = globals()[f"{self.abreviation}_image"]

    def almost_legal_moves(self, board):
        piece_at = board.piece_at
        returnlist = []

        i, j = self.i, self.j
        for a, b in [[-1, -1], [-1, 1], [-1, 0], [1, -1], [1, 1], [1, 0], [0, 1], [0, -1]]:
            i1, j1 = i + a, j + b
            if isInbounds(i1, j1) and (not piece_at(i1, j1) or piece_at(i1, j1).color != self.color):
                returnlist.append((i1, j1))

        # castle
        rights = [i for i in board.castle_rights if i.lower() == i]
        if self.never_moved:
            pass

        return returnlist


dico = {"p": Pawn, "r": Rook, "b": Bishop, "n": Knight, "q": Queen, "k": King}


def piece_from_abreviation(abreviation, i, j):
    if abreviation.lower() == abreviation:
        color = "black"
    else:
        color = "white"

    return dico[abreviation.lower()](color, i, j)
