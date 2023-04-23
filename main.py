import pygame
from constants import *
from Game import Game

if __name__ == "__main__":
    pygame.init()
    win = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE, pygame.FULLSCREEN)
    game = Game(win, fenmate2[0])
    game.run()
    pygame.quit()
