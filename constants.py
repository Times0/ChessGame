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
wp_image = pygame.image.load(r"assets/row-1-col-6.png")
wr_image = pygame.image.load(r"assets/row-1-col-5.png")
wn_image = pygame.image.load(r"assets/row-1-col-4.png")
wb_image = pygame.image.load(r"assets/row-1-col-3.png")
wq_image = pygame.image.load(r"assets/row-1-col-2.png")
wk_image = pygame.image.load(r"assets/row-1-col-1.png")

bp_image = pygame.image.load(r"assets/row-2-col-6.png")
br_image = pygame.image.load(r"assets/row-2-col-5.png")
bn_image = pygame.image.load(r"assets/row-2-col-4.png")
bb_image = pygame.image.load(r"assets/row-2-col-3.png")
bq_image = pygame.image.load(r"assets/row-2-col-2.png")
bk_image = pygame.image.load(r"assets/row-2-col-1.png")


