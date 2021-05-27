from win32api import GetSystemMetrics

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BG_COLOR = BLACK

# Sizes
WIDTH = GetSystemMetrics(0)
HEIGHT = GetSystemMetrics(1)
MIDW = WIDTH // 2
MIDH = HEIGHT // 2