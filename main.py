import pygame, os
from game import Game
from constants import *

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN, pygame.RESIZABLE)
    game = Game(win)
    game.run()
