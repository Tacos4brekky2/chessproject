import pygame

FPS = 60

SCREEN = WIDTH, HEIGHT = 600, 600
CELL_SIZE = 75
ROWS = 8
COLS = 8
clock = pygame.time.Clock()

# COLORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# IMAGES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
b_bishop = pygame.image.load('Assets/Pieces/black_bishop.png')
b_king = pygame.image.load('Assets/Pieces/black_king.png')
b_knight = pygame.image.load('Assets/Pieces/black_knight.png')
b_pawn = pygame.image.load('Assets/Pieces/black_pawn.png')
b_queen = pygame.image.load('Assets/Pieces/black_queen.png')
b_rook = pygame.image.load('Assets/Pieces/black_rook.png')
w_bishop = pygame.image.load('Assets/Pieces/white_bishop.png')
w_king = pygame.image.load('Assets/Pieces/white_king.png')
w_knight = pygame.image.load('Assets/Pieces/white_knight.png')
w_pawn = pygame.image.load('Assets/Pieces/white_pawn.png')
w_queen = pygame.image.load('Assets/Pieces/white_queen.png')
w_rook = pygame.image.load('Assets/Pieces/white_rook.png')
board_skin_tarzan = pygame.image.load('Assets/Boards/board_tarzan.png')

Assets = {
    1: b_pawn,
    2: w_pawn,
    3: b_bishop,
    4: w_bishop,
    5: b_knight,
    6: w_knight,
    7: b_rook,
    8: w_rook,
    9: b_queen,
    10: w_queen,
    11: b_king,
    12: w_king,
    13: board_skin_tarzan
}

# BOARD ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FILE_LETTERS = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
    0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'
}
RANK_INDEX = {
    1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 0
}

# FONTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# font1 = pygame.font.Font('Assets/Fonts/Helvetica/helvetica-condensed-light')
# font2 = pygame.font.SysFont('cursive', 25)

