import pygame
from constants import *
from Board import *
from Logic import *


class Game:
    def __init__(self, win):
        self.win = win
        self.board = Board(Logic(), BOARDSIZE)

    def run(self):

        game_on = True
        clock = pygame.time.Clock()
        while game_on:
            clock.tick(60)
            self.win.fill(BG_COLOR)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:  # si on appuie sur la croix
                    game_on = False

                # on gère tous les évènements ici

            self.draw_everything()
            pygame.display.flip()  # update l'affichage
        pygame.quit()

    def draw_everything(self):
        self.board.draw(self.win, MIDW - BOARDSIZE // 2, MIDH - BOARDSIZE // 2)
