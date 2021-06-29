from copy import deepcopy
from itertools import product

import numpy as np
from numpy import matrix

from fonctions import isInbounds, other_color


class Logic:
    """ a Logic instance is an independant chess board that has every fonction needed to play the game like isMate(
    color) or cases_attacked_by(color) and attributes such as turn, state, castle_rights etc"""

    def __init__(self, data=None, fen=None, data2=np.array(None)):
        """

        :param data: de la forme : board, castle_rights
        :param fen:
        """
        if data:
            self.board = data[0]
            self.castle_rights = data[1]
            self.turn = data[2]

        elif data2.size > 1:
            self.board = list()
            self.load_data(data2)
            self.castle_rights = "KQkq"

        elif fen:
            # variables pour les privilèges de roquer
            self.castle_rights = "kqKQ"  # kingside, queenside
            # ["game_on","blackwins", "whitewins", "stalemate"]
            self.board = [[None for _ in range(8)] for _ in range(8)]
            self.turn = "white"
            self.load_fen(fen)
        else:
            raise ArithmeticError
        self.mark = list()  # en passant

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
                    if c.upper() == "P" and i != (1 if b_row[-1].color == "black" else 6):
                        b_row[-1].never_moved = False
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
        i, j = 0, 0
        lines = list()
        while i < 8:
            line = ""
            while j < 8:
                # si on a un espace
                if not self.piece_at(i, j):
                    c = 0
                    while j < 8 and not self.piece_at(i, j):
                        c += 1
                        j += 1
                    line += str(c)
                else:
                    line += self.piece_at(i, j).abreviation
                    j += 1
            lines.append(line)
            i += 1
            j = 0

        board = "/".join(lines)
        turn = self.turn[0]
        castle_rights = f"{self.castle_rights}"

        returnfen = " ".join([board, turn, castle_rights])
        return returnfen

    def data(self):
        newboard = deepcopy(self.board)
        return newboard, self.castle_rights, self.turn

    def castle_rights_bit(self):
        return [0 for char in self.castle_rights if 1]

    def get_data(self):
        L = np.array(
            [self.board[i][j].value
             if self.board[i][j] and self.board[i][j].color == "white"
             else self.board[i][j].value + 10 if self.board[i][j] else 0 for i in range(8) for j in range(8)],
            dtype=np.int8)
        L = np.append(L, (1 if self.turn == "white" else 0))
        return L

    def load_data(self, data):
        # print("\n\nSTART ")

        L = list()
        for i in range(8):

            L.append(
                [dico2[val - 10]("black", 0, 0)
                 if val > 10
                 else dico2[val]("white", 0, 0)
                if val != 0
                else dico2[val] for val in data[i * 8:i * 8 + 8]])

            for j in range(8):
                if L[i][j]:
                    L[i][j].set_coord_weird(i, j)
        self.board = L
        self.turn = "white" if data[64] == 1 else "black"

    def check(self):
        for i in range(8):
            for j in range(8):
                if self.piece_at(i, j):
                    if self.board[i][j].i != i or self.board[i][j].j != j:
                        print(i, j, self.board[i][j].i, self.board[i][j].j)
                        # return False
        return True

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

    def hasLegalmoves(self, color):
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if piece and piece.color == color and piece.legal_moves(self):
                    return True
        return False

    def king_coord(self, color: str) -> tuple:

        for i in range(8):
            for j in range(8):
                if self.piece_at(i, j) and self.board[i][j].abreviation == ("K" if color == "white" else "k"):
                    king_i, king_j = i, j
                    return king_i, king_j

    def king(self, color: str):
        i, j = self.king_coord(color)
        return self.board[i][j]

    def isIncheck(self, color: str) -> bool:
        i, j = self.king_coord(color)
        return (i, j) in self.cases_attacked_by(("white" if color == "black" else "black"))

    def isMate(self, color: str) -> bool:
        return self.isIncheck(color) and not self.hasLegalmoves(color)

    def isStalemate(self, color: str) -> bool:
        return not self.hasLegalmoves(color)

    def update_game_state(self, color: str):
        """ possible states : ["black wins","white wins","stalemate"]"""
        if self.isMate(color):
            self.state = "".join([other_color(color), "wins"])
        elif self.isStalemate(color):
            self.state = "draw"

    def move(self, i: int, j: int, dest_i, dest_j) -> None:
        """
        Moves a piece to a square regardless of rules
        i,j origin coordinates, dest_i,dest_j destination coordinates
        :return: None
        """
        piece = self.board[i][j]
        if piece is None:
            print(i, j)
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
        self.mark = []
        # special moves

        # castle
        if i == 0 and j == 4 and dest_i == 0 and dest_j == 2 and piece.never_moved:
            self.real_move(0, 0, 0, 3, False)
        elif i == 0 and j == 4 and dest_i == 0 and dest_j == 6 and piece.never_moved:
            self.real_move(0, 0, 0, 5, False)
        elif i == 7 and j == 4 and dest_i == 7 and dest_j == 2 and piece.never_moved:
            self.real_move(7, 0, 7, 3, False)
        elif i == 7 and j == 4 and dest_i == 7 and dest_j == 6 and piece.never_moved:
            self.real_move(7, 7, 7, 5, False)

        # promotion
        elif piece.abreviation.lower() == "p" and dest_i == (0 if piece.direction == -1 else 7):
            piece = Queen(piece.color, i, j)

        # en passant
        elif piece.abreviation.lower() == "p" and dest_i == i + 2 * piece.direction:
            self.mark = [(i + piece.direction, j)]
        elif piece.abreviation.lower() == 'p' and j != dest_j and not self.piece_at(dest_i, dest_j):
            self.capture(i, dest_j)

        self.board[i][j] = None
        self.board[dest_i][dest_j] = piece
        self.board[dest_i][dest_j].moved(dest_i, dest_j)
        if switch_turn:
            self.switch_turn()
        print("update")
        self.update_game_state(self.turn)

    def capture(self, i, j):
        self.board[i][j] = None

    def switch_turn(self) -> None:
        self.turn = "white" if self.turn == "black" else "black"

    def get_score(self, color):
        score = 0
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if piece and piece.color == color:
                    score += values[piece.abreviation.lower()]
        return score

    def get_static_simple_eval(self):
        return self.get_score("white") - self.get_score("black")

    def get_static_eval(self):
        simple_eval = self.get_static_simple_eval()
        if self.nb_pieces_on_board() >= 4:
            return simple_eval

        i, j = self.king_coord("black")
        center_penality = (abs(3 - i) * abs(3 + j)) / 16
        return simple_eval + center_penality

    def nb_pieces_on_board(self):
        return len([0 for i in range(8) for j in range(8) if self.board[i][j]])

    def __repr__(self) -> str:
        returnboard = [[" " for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if self.board[i][j]:
                    returnboard[i][j] = self.board[i][j].abreviation

        return str(matrix(returnboard))


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

    def set_coord_weird(self, i, j):
        self.i, self.j = i, j

    def almost_legal_moves(self, board: Logic) -> list:
        """Cette fonction est overriden pour chacune des pièces, elle renvoie les moves possible pour une pièce
        en prenant en compte les autres pièces de l'échequier mais sans prendre en compte les échecs au roi"""
        pass

    def legal_moves(self, logic: Logic) -> list[(int, int)]:
        """ Returns the list of every almost legal move this piece has which means it does not care about checks,
        checks are handled in  legal_moves """

        returnlist = []
        if self.color != logic.turn:
            return []
        for move in self.almost_legal_moves(logic):
            virtual = Logic(data2=logic.get_data())
            # virtual2 = Logic(data=logic.data())
            # color = virtual2.turn
            # print(virtual, "\n\n", virtual2, virtual.turn, virtual2.turn, virtual.isIncheck(color),
            # virtual2.isIncheck(color))

            virtual.move(self.i, self.j, *move)
            if not virtual.isIncheck(self.color):
                # print(f"Not in check with the move {move}")
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
        self.value = 1
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
                if isInbounds(i2, j) and not piece_at(i2, j):
                    returnlist.append((i2, j))

        # captures
        for ja in [j - 1, j + 1]:
            if isInbounds(i1, ja) and piece_at(i1, ja) and piece_at(i1, ja).color != self.color:
                returnlist.append((i1, ja))

        # en croissant
        if i == (3 if self.color == "white" else 4):
            for jb in [j - 1, j + 1]:
                if isInbounds(i1, jb) and (i1, jb) in board.mark:
                    returnlist.append((i1, jb))

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
        self.value = 2
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
        self.value = 3
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
        self.value = 4
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
        self.value = 5
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
        self.value = 6
        # self.image = globals()[f"{self.abreviation}_image"]

    def almost_legal_moves(self, board):
        piece_at = board.piece_at
        returnlist = []

        i, j = self.i, self.j
        for a, b in [[-1, -1], [-1, 1], [-1, 0], [1, -1], [1, 1], [1, 0], [0, 1], [0, -1]]:
            i1, j1 = i + a, j + b
            if isInbounds(i1, j1) and (not piece_at(i1, j1) or piece_at(i1, j1).color != self.color):
                returnlist.append((i1, j1))

        castle_rights = board.castle_rights

        if self.color == "white":
            rights = str([char for char in castle_rights if char.lower() == char])
        else:
            rights = str([char for char in castle_rights if char.upper() == char])
        if rights:
            i, j = (0, 4) if self.color == "black" else (7, 4)
            if "k" in rights.lower():
                if not piece_at(i, j + 1) and not piece_at(i, j + 2):
                    attacked_cases = board.cases_attacked_by(other_color(self.color))
                    if (i, j) not in attacked_cases and (i, j + 1) not in attacked_cases and (
                            i, j + 2) not in attacked_cases:
                        returnlist.append((i, j + 2))
            if "q" in rights.lower():
                if not piece_at(i, j - 1) and not piece_at(i, j - 2) and not piece_at(i, j - 3):
                    attacked_cases = board.cases_attacked_by(other_color(self.color))
                    if (i, j) not in attacked_cases and (i, j - 1) not in attacked_cases and (
                            i, j - 2) not in attacked_cases:
                        returnlist.append((i, j - 2))
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
dico2 = {0: None, 1: Pawn, 2: Bishop, 3: Rook, 4: Knight, 5: Queen, 6: King}
values = {"p": 1, "r": 5, "b": 3, "n": 3, "q": 9, "k": 0}


def piece_from_abreviation(abreviation, i, j):
    if abreviation.lower() == abreviation:
        color = "black"
    else:
        color = "white"

    return dico[abreviation.lower()](color, i, j)
