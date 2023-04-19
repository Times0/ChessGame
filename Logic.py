import numpy as np
from numpy import ndarray, sqrt

import enum

from Pieces import Queen, piece_from_abreviation, Color

format_cr = "KQkq"


class State(enum.Enum):
    GAMEON = 0
    BLACKWINS = 1
    WHITEWINS = 2
    DRAW = 3  # 50 moves rule, stalemate


class Piece:
    pass


class Logic:
    """ a Logic instance is an independant chess board that has every fonction needed to play the game like isMate(
    color) or cases_attacked_by(color) and attributes such as turn, state, castle_rights etc"""

    def __init__(self, fen):

        if fen:
            # variables pour les privilèges de roquer
            self.castle_rights = "kqKQ"  # kingside, queenside
            self.board = [[None for _ in range(8)] for _ in range(8)]
            self.load_fen(fen)
        else:
            raise ArithmeticError
        self.mark = list()  # en passant

        self.state = State.GAMEON
        self.fen = self.get_fen()

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
                    if c.upper() == "P" and i != (1 if b_row[-1].color == Color.BLACK else 6):
                        b_row[-1].never_moved = False
                    j += 1
            board.append(b_row)
            i += 1
            j = 0
        self.fen = fen

        for i, part in enumerate(parts[1:]):

            if i == 0:
                self.turn = Color.WHITE if part == "w" else Color.BLACK

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
        turn = "w" if self.turn == Color.WHITE else "b"
        castle_rights = f"{self.castle_rights}"

        returnfen = " ".join([board, turn, castle_rights])
        return returnfen

    def castle_rights_bit(self) -> ndarray:

        cr = self.castle_rights
        return np.array([1 if char in cr else 0 for char in format_cr])

    def piece_at(self, i, j) -> Piece or None:
        piece = self.board[i][j]
        return piece

    def set_piece(self, i, j, piece):
        self.board[i][j] = piece

    def cases_attacked_by(self, color: Color) -> list:
        L = []
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if piece and piece.color == color:
                    L.extend(piece.attacking_squares(self))
        return list(set(L))

    def legal_moves(self, color=None):
        color = self.turn if color is None else color
        return_list = []
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if piece and piece.color == color:
                    legals = piece.legal_moves(self)
                    if legals:
                        for legal in legals:
                            return_list.append((i, j, legal[0], legal[1], legal[2]))
        return return_list

    def get_legal_moves_piece(self, i, j):
        piece = self.piece_at(i, j)
        if piece:
            return piece.legal_moves(self)
        else:
            return []

    def ordered_legal_moves(self, color: Color):
        lm = self.legal_moves(color)
        lm.sort(key=lambda tup: tup[4], reverse=True)
        return lm

    def hasLegalmoves(self, color):
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if piece and piece.color == color and piece.legal_moves(self):
                    return True
        return False

    def king_coord(self, color: Color) -> tuple:
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if piece and piece.abreviation == ("K" if color == Color.WHITE else "k"):
                    return i, j

    def king(self, color: Color):
        i, j = self.king_coord(color)
        return self.piece_at(i, j)

    @staticmethod
    def isCapture(move) -> bool:
        return move[4] == 1

    @staticmethod
    def isCheck(move):
        return move[4] == 2

    def isIncheck(self, color: Color) -> bool:
        i, j = self.king_coord(color)
        return (i, j) in self.cases_attacked_by((Color.WHITE if color == Color.BLACK else Color.BLACK))

    def isMated(self, color: Color) -> bool:
        return self.isIncheck(color) and not self.hasLegalmoves(color)

    def isStalemate(self, color: Color) -> bool:
        return not self.hasLegalmoves(color)

    def update_game_state(self, color: Color):
        if self.isMated(color):
            self.state = State.BLACKWINS if color == Color.WHITE else State.WHITEWINS
        elif self.isStalemate(color):
            self.state = State.DRAW

    def move(self, move, switch_turn=True) -> None:
        i, j, dest_i, dest_j, _ = move
        piece = self.piece_at(i, j)
        if not piece:
            print(f"{i,j=}")
            print(f"{self}")
            raise Exception
        self.mark = []

        # special moves
        # castle
        piece_type = piece.abreviation.lower()
        if piece_type == "k":
            self.remove_castle_rights(piece.color)
            if i == 0 and j == 4 and dest_i == 0 and dest_j == 2:
                self.move((0, 0, 0, 3, 0), False)
            elif i == 0 and j == 4 and dest_i == 0 and dest_j == 6:
                self.move((0, 7, 0, 5, 0), False)
            elif i == 7 and j == 4 and dest_i == 7 and dest_j == 2:
                self.move((7, 0, 7, 3, 0), False)
            elif i == 7 and j == 4 and dest_i == 7 and dest_j == 6:
                self.move((7, 7, 7, 5, 0), False)

        elif piece_type == "r" and piece.never_moved and self.castle_rights:
            self.remove_castle_rights(piece.color, j)
        # promotion
        elif piece.abreviation.lower() == "p" and dest_i == (0 if piece.direction == -1 else 7):
            piece = Queen(piece.color, i, j)

        # en passant
        elif piece_type == "p" and dest_i == i + 2 * piece.direction:
            self.mark = [(i + piece.direction, j)]
        elif piece_type == 'p' and j != dest_j and not self.piece_at(dest_i, dest_j):
            self.capture(i, dest_j)

        self.set_piece(i, j, None)
        self.set_piece(dest_i, dest_j, piece)
        piece.moved(dest_i, dest_j)

        self.fen = self.get_fen()
        if switch_turn:
            self.switch_turn()

    def real_move(self, move):
        """Only used in Game.py, it is called once per move and not when calculating"""
        self.move(move)
        self.update_game_state(self.turn)

    def capture(self, i, j):
        self.board[i][j] = None

    def remove_castle_rights(self, color, j=None) -> None:
        if not self.castle_rights:
            return
        if j == 0:
            r = "q"
        elif j == 7:
            r = "k"
        else:
            r = "qk"
        if color == Color.WHITE:
            r = r.upper()
        for char in r:
            self.castle_rights = self.castle_rights.replace(char, "")

    def switch_turn(self) -> None:
        self.turn = Color.WHITE if self.turn == Color.BLACK else Color.BLACK

    def get_score(self, color):
        score = 0
        for i in range(8):
            for j in range(8):
                piece = self.piece_at(i, j)
                if piece and piece.color == color:
                    score += piece_value[piece.abreviation.lower()]
        return score

    def get_static_simple_eval(self):
        return self.get_score(Color.WHITE) - self.get_score(Color.BLACK)

    def get_static_eval(self):
        simple_eval = self.get_static_simple_eval()
        if self.nb_pieces_on_board() >= 4:
            return simple_eval

        if simple_eval < -5:
            loser = Color.WHITE
        elif simple_eval > 5:
            loser = Color.BLACK
        else:
            loser = Color.WHITE

        c_distance = self.distance_center_king(loser)
        k_distance = self.distance_between_kings()

        if loser == Color.WHITE:
            return simple_eval - c_distance + k_distance
        elif loser == Color.BLACK:
            return simple_eval + c_distance - k_distance
        else:
            return simple_eval

    def distance_between_kings(self):
        bk = self.king(Color.BLACK)
        wk = self.king(Color.WHITE)
        return sqrt((bk.i - wk.i) ** 2 + (bk.i - wk.i) ** 2)

    def distance_center_king(self, color):
        i, j = self.king_coord(color)
        return sqrt((i - 3) ** 2 + (j - 3) ** 2)

    def nb_pieces_on_board(self):
        return len([0 for i in range(8) for j in range(8) if self.board[i][j]])


piece_value = {"p": 1, "r": 5, "b": 3, "n": 3, "q": 9, "k": 0}
