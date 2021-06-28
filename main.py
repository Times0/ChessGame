import pygame

from constants import *
from game import Game

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.FULLSCREEN)
    game = Game(win, mate2fen)
    game.run()
