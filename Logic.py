from itertools import product

import numpy as np

from fonctions import isInbounds, other_color

from constants import *


class Logic:
    """ a Logic instance is an independant chess board that has every fonction needed to play the game like isMate(
    color) or cases_attacked_by(color) and attributes such as turn, state, castle_rights etc"""

    def __init__(self, fen):
        self.board = [[None for _ in range(8)] for _ in range(8)]
        self.turn = "white"
        self.load_fen(fen)

        # variables pour les privilèges de roquer
        self.castle_rights = "kqKQ"  # kingside, queenside
        # ["game_on","blackwins", "whitewins", "stalemate"]
        self.state = "game_on"

    def load_fen(self, fen) -> None:
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
                self.castle_rights = part

        self.board = board.copy()

    def get_fen(self) -> str:
        """returns the fen of the current position"""
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

    def cases_attacked_by(self, color: str) -> list:
        L = []
        for i in range(8):
            for j in range(8):
                piece = self.board[i][j]
                if piece and piece.color == color:
                    L.extend(piece.attacking_squares(self))
        return list(set(L))

    def legal_moves(self, color="") -> list[(int, int, int, int)]:
        color = self.turn if color == "" else color
        """origin, destination"""
        returnlist = []
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if piece and piece.color == color:
                    legals = piece.legal_moves(self)
                    if legals:
                        for legal in legals:
                            returnlist.append((i, j, *legal))
        return returnlist

    def king_coord(self, color: str) -> tuple:
        king_i, king_j = 0, 0
        for i in range(8):
            for j in range(8):
                if self.piece_at(i, j) and self.board[i][j].abreviation == ("K" if color == "white" else "k"):
                    king_i, king_j = i, j
                    return king_i, king_j

    def isIncheck(self, color: str) -> bool:
        i, j = self.king_coord(color)
        return (i, j) in self.cases_attacked_by(("white" if color == "black" else "black"))

    def isMate(self, color: str) -> bool:
        return self.isIncheck(color) and self.legal_moves(color) == []

    def isStalemate(self, color: str) -> bool:
        return self.legal_moves(color) == []

    def king(self, color: str):
        i, j = self.king_coord(color)
        return self.board[i][j]

    def update_game_state(self, color: str):
        """ possible states : ["black wins","white wins","stalemate"]"""
        if self.isMate(color):
            self.state = other_color(color) + "wins"
        elif self.isStalemate(color):
            self.state = "stalemeate"

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

    def real_move(self, i: int, j: int, dest_i, dest_j, switch_turn=True) -> None:
        """move method used when moving on the real board (not in virtual ones, probably a terrible idea btw) switch
        turn is set to false when moving the rook during castling"""
        piece = self.board[i][j]
        if not piece:
            print('no piece here')
            raise Exception

        if i == 0 and j == 4 and dest_i == 0 and dest_j == 2 and piece.never_moved:
            self.real_move(0, 0, 0, 3, False)
        elif i == 0 and j == 4 and dest_i == 0 and dest_j == 6 and piece.never_moved:
            self.real_move(0, 0, 0, 5, False)
        elif i == 7 and j == 4 and dest_i == 7 and dest_j == 2 and piece.never_moved:
            self.real_move(7, 0, 7, 3, False)
        elif i == 7 and j == 4 and dest_i == 7 and dest_j == 6 and piece.never_moved:
            self.real_move(7, 7, 7, 5, False)

        self.board[i][j] = None
        self.board[dest_i][dest_j] = piece
        self.board[dest_i][dest_j].moved(dest_i, dest_j)
        if switch_turn:
            self.switch_turn()
        self.update_game_state(self.turn)

    def switch_turn(self) -> None:
        self.turn = "white" if self.turn == "black" else "black"

    def __repr__(self) -> str:
        returnboard = [[" " for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    returnboard[i][j] = self.board[i][j].abreviation

        return str(np.matrix(returnboard))


class Piece:
    def __init__(self, color, i, j):
        self.never_moved = True
        self.color = color
        self.i = i
        self.j = j
        self.abreviation = None

    def set_abreviation(self, name) -> None:
        inv_map = {v: k for k, v in dico.items()}
        abreviation = inv_map[name]
        if self.color == "white":
            abreviation = abreviation.upper()
        self.abreviation = abreviation

    def almost_legal_moves(self, board: Logic) -> list:
        """Cette fonction est overriden pour chacune des pièces, elle renvoie les moves possible pour une pièce
        en prenant en compte les autres pièces de l'échequier mais sans prendre en compte les échecs au roi"""
        pass

    def legal_moves(self, board: Logic) -> list[(int, int)]:
        """ Returns the list of every almost legal move this piece has which means it does not care about checks,
        checks are handled in  legal_moves """

        returnlist = []
        if self.color != board.turn:
            return []
        for move in self.almost_legal_moves(board):
            virtual = Logic(board.get_fen())
            virtual.move(self.i, self.j, *move)
            if not virtual.isIncheck(self.color):
                returnlist.append(move)

        return returnlist

    def attacking_squares(self, board) -> list:
        """returns the list of every coordinates this piece is attacking/protecting, it is a bit different from
        almos_legal moves since a protected piece is not attacked """
        return self.almost_legal_moves(board)

    def moved(self, dest_i, dest_j) -> None:
        """Updates the info the piece has about itself"""
        self.i, self.j = dest_i, dest_j
        self.never_moved = False


class Pawn(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)

        # self.image = globals()[f"{self.abreviation}_image"]
        self.direction = -1 if self.color == 'white' else +1

    def almost_legal_moves(self, board: Logic) -> list:

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

    def attacking_squares(self, board) -> list:
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
        # self.image = globals()[f"{self.abreviation}_image"]

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
        # self.image = globals()[f"{self.abreviation}_image"]

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
        # self.image = globals()[f"{self.abreviation}_image"]

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
        # self.image = globals()[f"{self.abreviation}_image"]

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
        # self.image = globals()[f"{self.abreviation}_image"]

    def almost_legal_moves(self, board):
        piece_at = board.piece_at
        returnlist = []

        i, j = self.i, self.j
        for a, b in [[-1, -1], [-1, 1], [-1, 0], [1, -1], [1, 1], [1, 0], [0, 1], [0, -1]]:
            i1, j1 = i + a, j + b
            if isInbounds(i1, j1) and (not piece_at(i1, j1) or piece_at(i1, j1).color != self.color):
                returnlist.append((i1, j1))

        bc = board.castle_rights
        rights_w = ""  # c'est de la merde
        rights_b = ""  # c'est de la merde
        for c in bc:
            if c.upper() == c:
                rights_w += c
            elif c.lower() == c:
                rights_b += c
        rights = (rights_b if self.color == "black" else rights_w).upper()
        attack = board.cases_attacked_by(self.color)
        if self.never_moved:
            for e in [n for n in [-1 * ("Q" in rights), 1 * ("K" in rights)] if n != 0]:  # queenside, kingside

                if [([i, b + j] not in attack) and (not piece_at(i, b + j) or b == 0) for b in [0, 1 * e, 2 * e]] == [
                    True] * 3:
                    coord1, coord2 = (7 if e == 1 and self.color == "white" else 0), (
                        0 if e == -1 and self.color == "black" else 7)
                    # black : k [0,7] q [0,0]
                    # white : K [7,7] Q [0,7]
                    if piece_at(coord1, coord2) and piece_at(coord1, coord2).abreviation.upper() == "R" and piece_at(
                            coord1, coord2).never_moved:
                        returnlist.append((i, j + 2 * e))
        return returnlist

    def attacking_squares(self, board):
        piece_at = board.piece_at
        returnlist = []

        i, j = self.i, self.j
        for a, b in [[-1, -1], [-1, 1], [-1, 0], [1, -1], [1, 1], [1, 0], [0, 1], [0, -1]]:
            i1, j1 = i + a, j + b
            if isInbounds(i1, j1) and (not piece_at(i1, j1) or piece_at(i1, j1).color != self.color):
                returnlist.append((i1, j1))
        return returnlist


dico = {"p": Pawn, "r": Rook, "b": Bishop, "n": Knight, "q": Queen, "k": King}


def piece_from_abreviation(abreviation, i, j):
    if abreviation.lower() == abreviation:
        color = "black"
    else:
        color = "white"

    return dico[abreviation.lower()](color, i, j)
