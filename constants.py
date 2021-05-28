from win32api import GetSystemMetrics
import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RANDOM = (145, 32, 14)
RANDOM2 = (45, 32, 74)

BG_COLOR = BLACK
CASECOLOR1 = WHITE
CASECOLOR2 = BLACK

# Sizes
WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
MIDW = WIDTH // 2
MIDH = HEIGHT // 2
BOARDSIZE = HEIGHT * 0.8

