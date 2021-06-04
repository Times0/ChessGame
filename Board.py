from constants import *
import pygame


class Board:
    def __init__(self, logic, size):
        self.size = size
        self.case_size = int(self.size // 8)
        self.test = "test"
        self.x = 0
        self.y = 0

        self.logic = logic

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
        board = self.logic.board
        for i in range(8):
            for j in range(8):
                if board[i][j].strip() != "":
                    image = globals()[f"{board[i][j]}_image"]
                    image = pygame.transform.smoothscale(image, (self.case_size, self.case_size))
                    win.blit(image, (self.x + self.case_size * j, self.y + self.case_size * i))
