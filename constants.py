from win32api import GetSystemMetrics
import pygame

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
LIGHTBEIGE = (181, 136, 99)
BROWN = (240, 217, 181)

BG_COLOR = BLACK
CASECOLOR1 = BROWN
CASECOLOR2 = LIGHTBEIGE

# Sizes
WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
MIDW = WIDTH // 2
MIDH = HEIGHT // 2
BOARDSIZE = HEIGHT * 0.8
