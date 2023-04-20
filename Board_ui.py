import pygame

from constants import *
from typing import Tuple

from fonctions import isInbounds

PADDING_WIDTH = 150
PADDING_HEIGHT = 10


def get_x_y_w_h():
    W, H = pygame.display.get_surface().get_size()
    m = min(W - 2 * PADDING_WIDTH, H - 2 * PADDING_HEIGHT)
    x = (W - m) // 2
    y = (H - m) // 2
    return x, y, m, m


def coord_from_pos(coord_x, coord_y) -> Tuple[int, int]:
    """
    Fait le lien entre les pixels et les coordonnées de la matrice
    :return: Retourne i,j les coordonnées de la matrice de Board
    """
    x, y, w, h = get_x_y_w_h()
    i = (coord_y - y) // (h // 8)
    j = (coord_x - x) // (w // 8)
    return i, j


class Board:
    def __init__(self, size):
        self.size = size
        self.case_size = int(self.size // 8)
        self.x = 0  # coordonnées en pixel par rapport à la fenetre
        self.y = 0
        self.board_to_output = [[None for _ in range(8)] for _ in range(8)]
        boardstates = ["idle", "dragging"]
        self.state = "idle"

        self.clicked_piece_coord = None
        self.dragged_piece = None
        self.dragged_piece_coord = None  # i,j
        self.dragged_piece_pos = None
        self.dragging = False

    def set_to_gone(self, x, y):
        i, j = coord_from_pos(x, y)
        self.dragged_piece = self.piece_at_coord(i, j)
        if not self.dragged_piece:
            return
        self.dragging = True
        self.board_to_output[i][j] = "gone"
        self.dragged_piece_pos = x, y
        self.dragged_piece_coord = i, j
        self.clicked_piece_coord = i, j

    def set_to_not_gone(self):
        i, j = self.dragged_piece_coord
        if self.dragged_piece:
            self.board_to_output[i][j] = self.dragged_piece
        self.dragged_piece = None
        self.dragged_piece_coord = None
        self.dragged_piece_pos = None
        self.dragging = False

    def pos_from_coord(self, i, j):
        return self.x + j * CASESIZE, self.y + i * CASESIZE

    def piece_at_coord(self, i, j):
        return self.board_to_output[i][j]

    def isNonempty(self, i, j):
        return (self.board_to_output[i][j]) is not None

    def update(self, logic):
        for i in range(8):
            for j in range(8):
                self.board_to_output[i][j] = logic.board[i][j]

    def clicked(self, pos) -> bool:
        """Called when the mouse is clicked return True if there is a piece at the position"""
        i, j = coord_from_pos(*pos)
        if not isInbounds(i, j):
            return False
        if self.isNonempty(i, j):
            self.set_to_gone(*pos)
            return True
        return False

    def drag(self, pos):
        """Called only when a piece is already being dragged"""
        self.dragged_piece_pos = pos

    def drop(self, pos):
        """Called when a piece is already being dragged and the mouse is released"""
        i, j = coord_from_pos(*pos)
        self.set_to_not_gone()
        return i, j

    # affichage

    def draw(self, win, dots, x, y, w, h):
        """Draws everything"""
        self.draw_board(win, x, y, w, h)
        self.draw_pieces(win, x, y, w, h)
        self.draw_dots(win, dots, x, y, w, h)

    def draw_board(self, win, x, y, w, h):
        case_size = w // 8
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = CASECOLOR1
                else:
                    color = CASECOLOR2
                pygame.draw.rect(win, color, (x + j * case_size, y + i * case_size, case_size, case_size))

    def draw_pieces(self, win, x, y, w, h):
        case_size = w // 8
        board = self.board_to_output
        for i in range(8):
            for j in range(8):
                if board[i][j] == "gone":
                    image_p = globals()[f"{self.dragged_piece.abreviation}_image"]
                    image_p = pygame.transform.smoothscale(image_p, (int(case_size * 1.1), int(case_size * 1.1)))
                    win.blit(image_p,
                             (self.dragged_piece_pos[0] - case_size // 2,
                              self.dragged_piece_pos[1] - case_size // 2))
                elif board[i][j] is not None:
                    image_p = globals()[f"{board[i][j].abreviation}_image"]
                    image_p = pygame.transform.smoothscale(image_p, (case_size, case_size))
                    image_p = pygame.transform.smoothscale(image_p, (case_size, case_size))
                    win.blit(image_p, (x + j * case_size, y + i * case_size))

    def draw_dots(self, win, moves, x, y, w, h):
        case_size = w // 8
        for move in moves:
            i, j, _ = move
            pygame.draw.circle(win, RED, (x + j * case_size + case_size // 2, y + i * case_size + case_size // 2), 5)
