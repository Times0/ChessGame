from constants import *
import pygame
from pieces import *


class Board:
    def __init__(self, size):
        self.size = size
        self.case_size = int(self.size // 8)
        self.x = 0  # coordonnées en pixel par rapport à la fenetre
        self.y = 0
        self.board = None  # board shown on screen which can have "gone" for somme coords
        boardstates = ["idle", "dragging"]
        self.state = "idle"

        self.movingpiece = None
        self.movingpiece_coord = None  # i,j
        self.movingpiece_pos = None

    def set_to_gone(self, x, y):
        i, j = self.coord_from_pos(x, y)
        self.movingpiece = self.piece_at_coord(i, j)
        self.board[i][j] = "gone"
        self.movingpiece_pos = x, y
        self.movingpiece_coord = i, j

    def set_to_not_gone(self):
        i, j = self.movingpiece_coord
        self.board[i][j] = self.movingpiece
        self.movingpiece = None
        self.movingpiece_coord = None
        self.movingpiece_pos = None

    def coord_from_pos(self, x, y) -> tuple[int, int]:
        """
        Fait le lien entre les pixels et les coordonnées de la matrice
        :param x:
        :param y:
        :return: Retourne i,j les coordonnées de la matrice de Board
        """
        j = (x - BOARDTOPLEFTPOS[0]) // self.case_size
        i = (y - BOARDTOPLEFTPOS[1]) // self.case_size
        return int(i), int(j)

    def piece_at_coord(self, i, j):
        return self.board[i][j]

    def isNotempty(self, i, j):
        return self.board[i][j] != ""

    def update(self, board):
        self.board = board

    def draw(self, win, x, y):
        """Draws everything"""
        self.draw_board(win, x, y)
        self.draw_pieces(win)

    def draw_board(self, win, x, y):
        self.x = x
        self.y = y
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = CASECOLOR1
                else:
                    color = CASECOLOR2

                pygame.draw.rect(win, color,
                                 (x + self.case_size * i, y + self.case_size * j, self.case_size, self.case_size))

    def draw_pieces(self, win):
        board = self.board
        for i in range(8):
            for j in range(8):
                if board[i][j] == "gone":
                    image = self.movingpiece.image
                    image = pygame.transform.smoothscale(image, (self.case_size, self.case_size))
                    win.blit(image,
                             (self.movingpiece_pos[0] - self.case_size // 2,
                              self.movingpiece_pos[1] - self.case_size // 2))
                elif board[i][j] is not None:
                    image = board[i][j].image
                    image = pygame.transform.smoothscale(image, (self.case_size, self.case_size))
                    win.blit(image, (self.x + self.case_size * j, self.y + self.case_size * i))

    def __repr__(self):  # useless
        returnboard = [[None for _ in range(8)] for _ in range(8)]
        for i in range(8):
            for j in range(8):
                if self.board[i][j] is not None:
                    returnboard[i][j] = self.board[i][j].abreviation
        return str(returnboard)
