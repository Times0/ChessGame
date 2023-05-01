import pygame
from constants import *
from game import Game

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.FULLSCREEN)
    game = Game(win, STARTINGPOSFEN)
    game.run()
    pygame.quit()

"""
TODO: make board object less heavy, maybe piece functions outside object.
reduce the number of moves for minmax
allow promotion
"""
