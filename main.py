from constants import *
from game import Game
import pygame

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.FULLSCREEN)
    game = Game(win, STARTINGPOSFEN)
    game.run()
