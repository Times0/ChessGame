import pygame
from constants import *


class Game:
    def __init__(self, win):
        self.win = win

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
        pygame.draw.circle(self.win, WHITE, (MIDW - 40, MIDH - 20), 5)
        pygame.draw.circle(self.win, WHITE, (MIDW + 40, MIDH - 20), 5)
        pygame.draw.line(self.win, WHITE, (MIDW - 40, MIDH + 20), (MIDW + 40, MIDH + 20))
