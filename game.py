import time

import pygame
from constants import *
from Board import *
from Logic import *
from fonctions import *


class Game:
    def __init__(self, win, fen):
        self.win = win
        self.logic = Logic(fen)
        self.board = Board(BOARDSIZE)
        self.board.update(self.logic)

    def run(self):

        game_on = True
        clock = pygame.time.Clock()
        while game_on:
            clock.tick(60)
            self.win.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # si on appuie sur la croix
                    game_on = False

                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and \
                        isInrectangle(event.pos, BOARDTOPLEFTPOS, BOARDSIZE, BOARDSIZE) and \
                        self.board.isNotempty(*self.board.coord_from_pos(*event.pos)):  # si on clique sur une piece
                    self.board.set_to_gone(*event.pos)
                    self.board.state = "dragging"

                    i, j = self.board.coord_from_pos(*event.pos)

                    print(i, j)

                    moves = self.logic.board[i][j].legal_moves(self.logic)
                    self.board.legal_moves_to_output = moves

                elif event.type == pygame.MOUSEBUTTONUP and event.button == 1 and self.board.state == "dragging":
                    self.board.set_to_not_gone()
                    self.board.state = "idle"

                    # if self.logic.isMovelegal(.....):
                    #    self.logic.move(......)
                    #    self.board.update(self.logic.board)

                elif self.board.state == "dragging" and event.type == pygame.MOUSEMOTION:
                    self.board.dragged_piece_pos = event.pos

            self.draw_everything()
            pygame.display.flip()  # update l'affichage
        pygame.quit()

    def draw_everything(self):
        self.board.draw(self.win, *BOARDTOPLEFTPOS)
