from itertools import product
from enum import Enum
from fonctions import other_color, isInbounds
from square import Square, Move


# forwards declaration
class Logic:
    pass


class Color(Enum):
    WHITE = 0
    BLACK = 1


class Piece:
    def __init__(self, color, square: Square):
        from Logic import Logic

        self.never_moved = True
        self.color: Color = color
        self.square: Square = square
        self.abreviation = None

    def set_abreviation(self, name) -> None:
        inv_map = {v: k for k, v in dico.items()}
        abreviation = inv_map[name]
        if self.color == Color.WHITE:
            abreviation = abreviation.upper()
        self.abreviation = abreviation

    def set_coord_weird(self, i, j) -> None:
        self.i, self.j = i, j

    def almost_legal_moves(self, board: Logic) -> list[Move]:
        """Cette fonction est overriden pour chacune des pièces, elle renvoie les moves possible pour une pièce
        en prenant en compte les autres pièces de l'échequier mais sans prendre en compte les échecs au roi"""
        pass

    def legal_moves(self, logic: Logic) -> list[Move]:
        """ Returns the list of every almost legal move this piece has which means it does not care about checks,
        checks are handled in  legal_moves
         Format is (i, j, id) with id being 1 if it is a capture and ((2 if it is a check)) (else 0) """
        from Logic import Logic
        returnlist = []
        if self.color != logic.turn:
            raise Exception(f"It is not this piece's turn, it is {logic.turn} turn\n"
                            f" and this piece is {self.color}\n"
                            f" and the piece is at {self.square}")
        for move in self.almost_legal_moves(logic):
            virtual = Logic(logic.get_fen())
            virtual.move(move)
            me_is_in_check = virtual.isIncheck(self.color)
            if not me_is_in_check:
                if virtual.isIncheck(other_color(self.color)):
                    move.is_check = True
                returnlist.append(move)
        return returnlist

    def attacking_squares(self, logic) -> list[Square]:
        """returns the list of every coordinates this piece is attacking/protecting, it is a bit different from
        almos_legal moves since a protected piece is not attacked """
        return [move.destination for move in self.almost_legal_moves(logic)]

    def moved(self, square: Square) -> None:
        """Updates the info the piece has about itself"""
        self.never_moved = False
        self.square = square

    def __str__(self):
        s = f"{self.color} {self.abreviation} at {self.square}"
        return s


class Pawn(Piece):
    def __init__(self, color, square: Square):
        super().__init__(color, square)
        self.set_abreviation(self.__class__)
        self.direction = 1 if self.color == Color.WHITE else -1

    def almost_legal_moves(self, board: Logic) -> list[Move]:
        piece_at = board.get_piece
        i, j = self.square.i, self.square.j
        dir = self.direction
        returnlist = []

        # move devant
        i1 = i + dir  # case devant le pion (relativement)
        if isInbounds(i1, j) and not piece_at(Square(i1, j)):
            returnlist.append(Move(self.square, Square(i1, j)))
            if self.never_moved:
                i2 = i1 + dir  # deux cases devant le pion
                if isInbounds(i2, j) and not piece_at(Square(i2, j)):
                    returnlist.append(Move(self.square, Square(i2, j)))

        # captures
        for ja in [j - 1, j + 1]:
            if 0 <= ja < 8:
                p = piece_at(Square(i1, ja))
                if isInbounds(i1, ja) and p and p.color != self.color:
                    returnlist.append(Move(self.square, Square(i1, ja), is_capture=True))

        # en croissant
        if board.en_passant_square:
            i2, j2 = board.en_passant_square.i, board.en_passant_square.j
            if i2 == i1 and abs(j2 - j) == 1:
                returnlist.append(Move(self.square, Square(i1, j2), is_capture=True))
        return returnlist

    def attacking_squares(self, logic) -> list[Square]:
        piece_at = logic.get_piece
        i, j = self.square.i, self.square.j
        dir = self.direction
        i1 = i + dir
        returnlist = []
        # attacked squares
        for ja in [j - 1, j + 1]:
            if isInbounds(i1, ja):
                returnlist.append(Square(i1, ja))

        return returnlist


class Bishop(Piece):
    def __init__(self, color, square: Square):
        super().__init__(color, square)
        self.set_abreviation(self.__class__)

    def almost_legal_moves(self, board) -> list[Move]:
        piece_at = board.get_piece
        returnlist = []
        i, j = self.square.i, self.square.j

        for a, b in [[1, 1], [-1, 1], [1, -1], [-1, -1]]:
            i1, j1 = i + a, j + b
            while isInbounds(i1, j1):
                try:
                    piece = piece_at(Square(i1, j1))
                except IndexError:
                    break
                if not piece:
                    returnlist.append(Move(self.square, Square(i1, j1)))
                elif piece.color != self.color:
                    returnlist.append(Move(self.square, Square(i1, j1), is_capture=True))
                    break
                else:
                    break
                i1, j1 = i1 + a, j1 + b

        return returnlist


class Rook(Piece):
    def __init__(self, color, square: Square):
        super().__init__(color, square)
        self.set_abreviation(self.__class__)

    def almost_legal_moves(self, board) -> list[Move]:
        piece_at = board.get_piece
        returnlist = []
        i, j = self.square.i, self.square.j

        # Check squares in each direction separately
        for a, b in [(1, 0), (-1, 0), (0, 1), (0, -1)]:
            i1, j1 = i + a, j + b
            while isInbounds(i1, j1):
                piece = piece_at(Square(i1, j1))
                if not piece:
                    returnlist.append(Move(self.square, Square(i1, j1)))
                    i1, j1 = i1 + a, j1 + b
                elif piece.color != self.color:
                    returnlist.append(Move(self.square, Square(i1, j1), is_capture=True))
                    break
                else:
                    break

        return returnlist


class Knight(Piece):
    def __init__(self, color, square: Square):
        super().__init__(color, square)
        self.set_abreviation(self.__class__)

    def almost_legal_moves(self, board) -> list[Move]:
        piece_at = board.get_piece
        i, j = self.square.i, self.square.j
        returnlist = []

        # Iterate over each of the four possible moves
        for a, b in [(i - 1, j - 2), (i - 1, j + 2), (i + 1, j - 2), (i + 1, j + 2), (i - 2, j - 1), (i - 2, j + 1),
                     (i + 2, j - 1), (i + 2, j + 1)]:
            if isInbounds(a, b):
                piece = piece_at(Square(a, b))
                if not piece:
                    returnlist.append(Move(self.square, Square(a, b)))
                elif piece.color != self.color:
                    returnlist.append(Move(self.square, Square(a, b), is_capture=True))

        return returnlist


class Queen(Piece):
    def __init__(self, color, square: Square):
        super().__init__(color, square)
        self.set_abreviation(self.__class__)

    def almost_legal_moves(self, board):
        piece_at = board.get_piece
        returnlist = []
        i, j = self.square.i, self.square.j
        for a, b in [[1, 0], [-1, 0], [0, -1], [0, 1], [1, 1], [-1, 1], [1, -1], [-1, -1]]:
            for n in range(1, 8):  # on ne teste pas la case sur laquelle il y a déjà notre pièce
                i1, j1 = i + a * n, j + b * n
                if isInbounds(i1, j1):
                    piece = piece_at(Square(i1, j1))
                    if not piece:
                        returnlist.append(Move(self.square, Square(i1, j1)))
                    elif piece.color != self.color:
                        returnlist.append(Move(self.square, Square(i1, j1), is_capture=True))
                        break
                    else:
                        break  # rupture de la 'ligne' si une pièce y est présente
        return returnlist


class King(Piece):
    def __init__(self, color, square: Square):
        super().__init__(color, square)
        self.set_abreviation(self.__class__)

    def almost_legal_moves(self, board):
        piece_at = board.get_piece
        returnlist = []

        i, j = self.square.i, self.square.j
        for a, b in [[-1, -1], [-1, 1], [-1, 0], [1, -1], [1, 1], [1, 0], [0, 1], [0, -1]]:
            i1, j1 = i + a, j + b
            if isInbounds(i1, j1):
                piece = piece_at(Square(i1, j1))
                if not piece:
                    returnlist.append(Move(self.square, Square(i1, j1)))
                elif piece.color != self.color:
                    returnlist.append(Move(self.square, Square(i1, j1), is_capture=True))

        castle_rights = board.castle_rights
        if self.color == Color.WHITE:
            rights = str([char for char in castle_rights if char.upper() == char])
        else:
            rights = str([char for char in castle_rights if char.lower() == char])
        if rights:
            i, j = (0, 4) if self.color == Color.BLACK else (7, 4)
            if "k" in rights.lower():
                if not piece_at(Square(i, j + 1)) and not piece_at(Square(i, j + 2)):
                    attacked_cases = board.squares_attacked_by(other_color(self.color))
                    if Square(i, j) not in attacked_cases and Square(i, j + 1) not in attacked_cases and (
                            i, j + 2) not in attacked_cases and piece_at(i, 7):
                        returnlist.append(Move(self.square, Square(i, j + 2)))
            if "q" in rights.lower():
                if not piece_at(Square(i, j - 1)) and not piece_at(Square(i, j - 2)) and not piece_at(Square(i, j - 3)):
                    attacked_cases = board.squares_attacked_by(other_color(self.color))
                    if Square(i, j) not in attacked_cases and Square(i, j - 1) not in attacked_cases and Square(
                            i, j - 2) not in attacked_cases and piece_at(Square(i, 0)):
                        returnlist.append(Move(self.square, Square(i, j - 2)))
        return returnlist

    def attacking_squares(self, logic):
        piece_at = logic.get_piece
        returnlist = []

        i, j = self.square.i, self.square.j
        for a, b in [[-1, -1], [-1, 1], [-1, 0], [1, -1], [1, 1], [1, 0], [0, 1], [0, -1]]:
            i1, j1 = i + a, j + b
            if not isInbounds(i1, j1):
                continue
            p = piece_at(Square(i1, j1))
            if isInbounds(i1, j1) and (not p or p.color != self.color):
                returnlist.append(Square(i1, j1))
        return returnlist


dico = {"p": Pawn, "r": Rook, "b": Bishop, "n": Knight, "q": Queen, "k": King}
dico2 = {0: None, 1: Pawn, 2: Bishop, 3: Rook, 4: Knight, 5: Queen, 6: King}


def piece_from_abreviation(abreviation, i, j):
    return dico[abreviation.lower()](Color.BLACK if abreviation.lower() == abreviation else Color.WHITE, Square(i, j))
