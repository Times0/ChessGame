from win32api import GetSystemMetrics
import pygame

# Colors
BLACK = 0, 0, 0
WHITE = 255, 255, 255
LIGHTBEIGE = 181, 136, 99
BROWN = 240, 217, 181
GREEN = 63, 123, 82
ORANGE = 253, 189, 89
RED = (250, 41, 76)
GREY = 185, 199, 185

BG_COLOR = BLACK
CASECOLOR1 = BROWN
CASECOLOR2 = LIGHTBEIGE

# Sizes
WIDTH, HEIGHT = GetSystemMetrics(0), GetSystemMetrics(1)
MIDW = WIDTH // 2
MIDH = HEIGHT // 2
BOARDSIZE = HEIGHT * 0.8
BOARDTOPLEFTPOS = (MIDW - BOARDSIZE // 2, MIDH - BOARDSIZE // 2)

# Pieces

P_image = pygame.image.load(r"assets/row-1-col-6.png")  # white
R_image = pygame.image.load(r"assets/row-1-col-5.png")
N_image = pygame.image.load(r"assets/row-1-col-4.png")
B_image = pygame.image.load(r"assets/row-1-col-3.png")
Q_image = pygame.image.load(r"assets/row-1-col-2.png")
K_image = pygame.image.load(r"assets/row-1-col-1.png")

p_image = pygame.image.load(r"assets/row-2-col-6.png")  # black
r_image = pygame.image.load(r"assets/row-2-col-5.png")
n_image = pygame.image.load(r"assets/row-2-col-4.png")
b_image = pygame.image.load(r"assets/row-2-col-3.png")
q_image = pygame.image.load(r"assets/row-2-col-2.png")
k_image = pygame.image.load(r"assets/row-2-col-1.png")

# other
STARTINGPOSFEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
fen1 = "rnbqkbnr/ppp1pppp/8/3p4/4P3/8/PPPP1PPP/RNBQKBNR w KQkq - 0 2"
fencheck = "rnbqkbnr/pppppppp/5K2/8/8/8/PPPPPPPP/RNBQ1BNR w kq - 0 1"
fenmate = "r1bqkb1r/pppp1ppp/2n2n2/4p2Q/2B1P3/8/PPPP1PPP/RNB1K1NR w KQkq - 0 1"
test = 'rn1qkb1r/pp2pppp/5n2/3p1b2/3P4/2N1P3/PP3PPP/R1BQKBNR w KQkq - 0 1 id "CCR01"; bm Qb3;'
