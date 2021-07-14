import pygame

from constants import *
from game import Game

# Todo : ADD IDENTIFIER ON MOVES, FOR EXAMPLE CAPTURES AND CHECKS
if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.FULLSCREEN)
    game = Game(win, fenmate2[3])
    game.run()
