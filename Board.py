from constants import *
import pygame


class Board:
    def __init__(self, logic, size):
        self.size = size
        self.case_size = self.size // 8

        self.color1 = CASECOLOR1

        self.logic = logic

    def draw(self, win, x, y):
        """Draws everything"""
        self.draw_board(win, x, y)
        self.draw_pieces(win)

    def draw_board(self, win, x, y):
        for i in range(8):
            for j in range(8):
                if (i + j) % 2 == 0:
                    color = CASECOLOR1
                else:
                    color = CASECOLOR2

                pygame.draw.rect(win, color, (
                    x + self.case_size * i, y + self.case_size * j, self.case_size, self.case_size))

    def draw_pieces(self, win):
        pass
