from itertools import product
from enum import Enum
from fonctions import other_color, isInbounds


# forwards declaration
class Logic:
    pass


class Color(Enum):
    WHITE = 0
    BLACK = 1


class Piece:
    def __init__(self, color, i, j):
        from Logic import Logic

        self.never_moved = True
        self.color: Color = color
        self.i = i
        self.j = j
        self.abreviation = None

    def set_abreviation(self, name) -> None:
        inv_map = {v: k for k, v in dico.items()}
        abreviation = inv_map[name]
        if self.color == Color.WHITE:
            abreviation = abreviation.upper()
        self.abreviation = abreviation

    def set_coord_weird(self, i, j) -> None:
        self.i, self.j = i, j

    def almost_legal_moves(self, board: Logic) -> list:
        """Cette fonction est overriden pour chacune des pièces, elle renvoie les moves possible pour une pièce
        en prenant en compte les autres pièces de l'échequier mais sans prendre en compte les échecs au roi"""
        pass

    def legal_moves(self, logic: Logic) -> list[(int, int, int)]:
        """ Returns the list of every almost legal move this piece has which means it does not care about checks,
        checks are handled in  legal_moves
         Format is (i, j, id) with id being 1 if it is a capture and ((2 if it is a check)) (else 0) """
        from Logic import Logic
        returnlist = []
        if self.color != logic.turn:
            return []

        for move in self.almost_legal_moves(logic):
            virtual = Logic(logic.get_fen())
            true_move = self.i, self.j, *move
            virtual.move(true_move)
            if not virtual.isIncheck(self.color):
                if virtual.isIncheck(other_color(self.color)):
                    returnlist.append((move[0], move[1], 2))
                else:
                    returnlist.append(move)

        return returnlist

    def attacking_squares(self, logic) -> list:
        """returns the list of every coordinates this piece is attacking/protecting, it is a bit different from
        almos_legal moves since a protected piece is not attacked """
        return [(e[0], e[1]) for e in self.almost_legal_moves(logic)]

    def moved(self, dest_i, dest_j) -> None:
        """Updates the info the piece has about itself"""
        self.i, self.j = dest_i, dest_j
        self.never_moved = False


class Pawn(Piece):
    def __init__(self, color, i, j):
        super().__init__(color, i, j)
        self.set_abreviation(self.__class__)
        self.value = 1
        self.direction = -1 if self.color == Color.WHITE else 1

    def almost_legal_moves(self, board: Logic) -> list:
        piece_at = board.piece_at
        i, j = self.i, self.j
        dir = self.direction
        returnlist = []

        # move devant
        i1 = i + dir  # case devant le pion (relativement)
        if isInbounds(i1, j) and not piece_at(i1, j):
            returnlist.append((i1, j, 0))
            if self.never_moved:
                i2 = i1 + dir  # deux cases devant le pion
                if isInbounds(i2, j) and not board.piece_at(i2, j):
                    returnlist.append((i2, j, 0))

        # captures
        for ja in [j - 1, j + 1]:
            if isInbounds(i1, ja) and piece_at(i1, ja) and piece_at(i1, ja).color != self.color:
                returnlist.append((i1, ja, 1))

        # en croissant
        if i == (3 if self.color == Color.WHITE else 4):
            for jb in [j - 1, j + 1]:
                if isInbounds(i1, jb) and (i1, jb) in board.mark:
                    returnlist.append((i1, jb, 1))
        return returnlist

    def attacking_squares(self, logic) -> list:
        piece_at = logic.piece_at
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
        for a, b in [[1, 1], [-1, 1], [1, -1], [-1, -1]]:
            for n in range(1, 8):  # on ne teste pas la case sur laquelle il y a déjà notre pièce
                i1, j1 = i + a * n, j + b * n
                if isInbounds(i1, j1):
                    piece = piece_at(i1, j1)
                    if not piece:
                        returnlist.append((i1, j1, 0))
                    elif piece.color != self.color:
                        returnlist.append((i1, j1, 1))
                    if piece:
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
            for n in range(1, 8):  # on ne teste pas la case sur laquelle il y a déjà notre pièce
                i1, j1 = i + a * n, j + b * n
                if isInbounds(i1, j1):
                    piece = piece_at(i1, j1)
                    if not piece:
                        returnlist.append((i1, j1, 0))
                    elif piece.color != self.color:
                        returnlist.append((i1, j1, 1))
                    if piece:
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
        returnlist = []
        moves = list(product([i - 1, i + 1], [j - 2, j + 2])) + list(product([i - 2, i + 2], [j - 1, j + 1]))
        # return [move for move in moves if
        #         isInbounds(*move) and (not piece_at(*move) or piece_at(*move).color != self.color)]
        for i1, j1 in moves:
            if isInbounds(i1, j1):
                piece = piece_at(i1, j1)
                if not piece:
                    returnlist.append((i1, j1, 0))
                elif piece.color != self.color:
                    returnlist.append((i1, j1, 1))
        return returnlist


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
            for n in range(1, 8):  # on ne teste pas la case sur laquelle il y a déjà notre pièce
                i1, j1 = i + a * n, j + b * n
                if isInbounds(i1, j1):
                    piece = piece_at(i1, j1)
                    if not piece:
                        returnlist.append((i1, j1, 0))
                    elif piece.color != self.color:
                        returnlist.append((i1, j1, 1))
                    if piece:
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
            if isInbounds(i1, j1):
                piece = piece_at(i1, j1)
                if not piece:
                    returnlist.append((i1, j1, 0))
                elif piece.color != self.color:
                    returnlist.append((i1, j1, 1))

        castle_rights = board.castle_rights
        if self.color == Color.WHITE:
            rights = str([char for char in castle_rights if char.upper() == char])
        else:
            rights = str([char for char in castle_rights if char.lower() == char])
        if rights:
            i, j = (0, 4) if self.color == Color.BLACK else (7, 4)
            if "k" in rights.lower():
                if not piece_at(i, j + 1) and not piece_at(i, j + 2):
                    attacked_cases = board.cases_attacked_by(other_color(self.color))
                    if (i, j) not in attacked_cases and (i, j + 1) not in attacked_cases and (
                            i, j + 2) not in attacked_cases and piece_at(i, 7):
                        returnlist.append((i, j + 2, 0))
            if "q" in rights.lower():
                if not piece_at(i, j - 1) and not piece_at(i, j - 2) and not piece_at(i, j - 3):
                    attacked_cases = board.cases_attacked_by(other_color(self.color))
                    if (i, j) not in attacked_cases and (i, j - 1) not in attacked_cases and (
                            i, j - 2) not in attacked_cases and piece_at(i, 0):
                        returnlist.append((i, j - 2, 0))
        return returnlist

    def attacking_squares(self, logic):
        piece_at = logic.piece_at
        returnlist = []

        i, j = self.i, self.j
        for a, b in [[-1, -1], [-1, 1], [-1, 0], [1, -1], [1, 1], [1, 0], [0, 1], [0, -1]]:
            i1, j1 = i + a, j + b
            if isInbounds(i1, j1) and (not piece_at(i1, j1) or piece_at(i1, j1).color != self.color):
                returnlist.append((i1, j1))
        return returnlist


dico = {"p": Pawn, "r": Rook, "b": Bishop, "n": Knight, "q": Queen, "k": King}
dico2 = {0: None, 1: Pawn, 2: Bishop, 3: Rook, 4: Knight, 5: Queen, 6: King}


def piece_from_abreviation(abreviation, i, j):
    return dico[abreviation.lower()](Color.BLACK if abreviation.lower() == abreviation else Color.WHITE, i, j)
