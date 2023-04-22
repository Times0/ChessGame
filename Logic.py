import numpy as np
from numpy import ndarray, sqrt
from Pieces import Square, Move, Queen, Color, piece_from_abreviation, other_color
import enum

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
        self.board = np.empty((8, 8), dtype=Piece)
        self.state = State.GAMEON
        self.turn = Color
        self.castle_rights = str()
        self.full_move_number = int()
        self.half_move_clock = int()
        self.en_passant_square = str()
        self.load_fen(fen)

    def load_fen(self, fen) -> None:
        """loads a fen into the board"""
        fen = fen.split(" ")
        fen_board = fen[0].split("/")
        for i in range(8):
            j = 0
            for char in fen_board[i]:
                if char.isdigit():
                    j += int(char)
                else:
                    self.set_piece(Square(7 - i, j), piece_from_abreviation(char, 7 - i, j))
                    j += 1
        self.turn = Color.WHITE if fen[1] == "w" else Color.BLACK
        self.castle_rights = fen[2]
        self.en_passant_square = Square(fen[3]) if fen[3] != "-" else None
        self.half_move_clock = int(fen[4])
        self.full_move_number = int(fen[5])

    def get_fen(self) -> str:
        """returns the fen of the current position"""
        fen = ""
        empty = 0
        for i in range(7, -1, -1):
            for j in range(8):
                piece = self.get_piece(Square(i, j))
                if piece:
                    if empty:
                        fen += str(empty)
                        empty = 0
                    fen += piece.abreviation
                else:
                    empty += 1
            if empty:
                fen += str(empty)
                empty = 0
            if i != 0:
                fen += "/"
        fen += f" {'w' if self.turn == Color.WHITE else 'b'}"
        fen += f" {self.castle_rights if self.castle_rights else '-'}"
        fen += f" {self.en_passant_square if self.en_passant_square else '-'}"
        fen += f" {self.half_move_clock} {self.full_move_number}"
        return fen

    def get_piece(self, square: Square) -> Piece or None:
        return self.board[square.i][square.j]

    def set_piece(self, square: Square, piece: Piece) -> None:
        self.board[square.i][square.j] = piece

    def squares_attacked_by(self, color: Color) -> list[Square]:
        L = set()
        for i in range(8):
            for j in range(8):
                piece = self.get_piece(Square(i, j))
                if piece and piece.color == color:
                    L.update(piece.attacking_squares(self))
        return list(L)

    def legal_moves(self, color) -> list[Move]:
        color = self.turn if color is None else color
        return_list = []
        for i in range(8):
            for j in range(8):
                piece = self.get_piece(Square(i, j))
                if piece and piece.color == color:
                    legal_moves = piece.legal_moves(self)
                    return_list.extend(legal_moves)
        return return_list

    def get_legal_moves_piece(self, square: Square):
        piece = self.get_piece(square)

        if piece is None:
            raise Exception("No piece at this square")
        elif piece.color != self.turn:
            raise Exception("Piece is not the right color")
        else:
            return piece.legal_moves(self)

    def ordered_legal_moves(self, color: Color):
        lm = self.legal_moves(color)
        return lm
        # TODO: order the moves checks first, captures second, then the rest

    def hasLegalmoves(self, color):
        for i in range(8):
            for j in range(8):
                piece = self.get_piece(Square(i, j))
                if piece and piece.color == color and piece.almost_legal_moves(self):
                    return True
        return False

    def get_king_square(self, color: Color) -> Square:
        target = "K" if color == Color.WHITE else "k"
        for i in range(8):
            for j in range(8):
                piece = self.get_piece(Square(i, j))
                if piece and piece.abreviation == target:
                    return Square(i, j)

    def king(self, color: Color):
        s = self.get_king_square(color)
        return self.get_piece(s)

    @staticmethod
    def isCapture(move: Move) -> bool:
        return move.is_capture

    @staticmethod
    def isCheck(move):
        return move.is_check

    def isIncheck(self, color: Color) -> bool:
        s = self.get_king_square(color)
        square_attacked = self.squares_attacked_by(other_color(color))
        return s in square_attacked

    def update_game_state(self, debug=False):
        for i in range(8):
            for j in range(8):
                p = self.get_piece(Square(i, j))
                if p and p.color == self.turn and p.legal_moves(self):
                    if debug:
                        print(f"{self.turn} has legal moves : {p.legal_moves(self)}")
                        self.state = State.GAMEON
                    return

        if self.isIncheck(self.turn):
            self.state = State.WHITEWINS if self.turn == Color.BLACK else State.BLACKWINS
        else:
            self.state = State.DRAW
        print(f"game state : {self.state}")

    def move(self, move: Move) -> None:
        piece = self.get_piece(move.origin)
        if not piece:
            raise Exception(f"no piece at this square : {move.origin}")
        if piece.color != self.turn:
            raise Exception(f"it's not {piece.color}'s turn")
        self.en_passant_square = None

        # special moves
        # castle
        piece_type = piece.abreviation.lower()
        if piece_type == "k":
            self.remove_castle_rights(piece.color)
            if abs(move.origin.j - move.destination.j) == 2:
                rook_square = Square(i, 7 if j < move.destination.j else 0)
                rook = self.get_piece(rook_square)
                self.set_piece(rook_square, None)
                self.set_piece(Square(i, 5 if j < move.destination.j else 3), rook)
                rook.moved(Square(i, 5 if j < move.destination.j else 3))

        elif piece_type == "r" and piece.never_moved and self.castle_rights:
            self.remove_castle_rights(piece.color, move.origin.j)
        # promotion
        elif piece_type == "p" and move.destination.i == (0 if piece.direction == -1 else 7):
            self.set_piece(move.origin, None)
            self.set_piece(move.destination, Queen(piece.color, move.destination))


        # en passant square
        elif piece_type == "p" and move.destination.i == move.origin.i + 2 * piece.direction:
            self.en_passant_square = Square(move.origin.i + piece.direction, move.origin.j)
        # en passant capture
        elif piece_type == 'p' and move.origin.j != move.destination.j:
            self.set_piece(Square(move.origin.i, move.destination.j), None)  # capture the pawn

        self.set_piece(move.origin, None)
        self.set_piece(move.destination, piece)
        piece.moved(move.destination)

    def real_move(self, move: Move) -> None:
        """Called once the move is validated, updates the game state, switches the turn and increments the halfmove clock"""
        self.move(move)
        self.switch_turn()

        if self.turn == Color.WHITE:
            self.full_move_number += 1
        dest = move.destination
        piece = self.get_piece(dest)
        if piece and piece.abreviation.lower() == "p" or move.is_capture:
            self.half_move_clock = 0
        else:
            self.half_move_clock += 1
        self.update_game_state()

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
                piece = self.get_piece(i, j)
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
        i, j = self.get_king_square(color)
        return sqrt((i - 3) ** 2 + (j - 3) ** 2)

    def nb_pieces_on_board(self):
        return len([0 for i in range(8) for j in range(8) if self.board[i][j]])

    def __repr__(self):
        s = ""
        for i in range(8, 0, -1):
            s += str(i) + " "
            for j in "abcdefgh":
                piece = self.get_piece(Square(j + str(i)))
                if piece:
                    s += piece.abreviation + " "
                else:
                    s += "~ "
            s += "\n"
        s += "____________________\n"
        s += "  a b c d e f g h"
        return s

    def test_move(self, move):
        pass


piece_value = {"p": 1, "r": 5, "b": 3, "n": 3, "q": 9, "k": 0}


def translate_move(start, end):
    i = 8 - int(start[1])
    j = ord(start[0]) - ord("a")
    dest_i = 8 - int(end[1])
    dest_j = ord(end[0]) - ord("a")
    return i, j, dest_i, dest_j


if __name__ == "__main__":
    from constants import STARTINGPOSFEN

    l = Logic(STARTINGPOSFEN)
    l.real_move(Move(Square("e2"), Square("e4")))
    l.real_move(Move(Square("f7"), Square("f5")))
