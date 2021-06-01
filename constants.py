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

# Pieces
P_image = pygame.image.load(r"assets/row-1-col-6.png")
R_image = pygame.image.load(r"assets/row-1-col-5.png")
N_image = pygame.image.load(r"assets/row-1-col-4.png")
B_image = pygame.image.load(r"assets/row-1-col-3.png")
Q_image = pygame.image.load(r"assets/row-1-col-2.png")
K_image = pygame.image.load(r"assets/row-1-col-1.png")

p_image = pygame.image.load(r"assets/row-2-col-6.png")
r_image = pygame.image.load(r"assets/row-2-col-5.png")
n_image = pygame.image.load(r"assets/row-2-col-4.png")
b_image = pygame.image.load(r"assets/row-2-col-3.png")
q_image = pygame.image.load(r"assets/row-2-col-2.png")
k_image = pygame.image.load(r"assets/row-2-col-1.png")
