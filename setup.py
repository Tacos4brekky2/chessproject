import pygame

FPS = 60
CELL_SIZE = 20
SCREEN = WIDTH, HEIGHT = 600, 600
ROWS = ((HEIGHT - 120) // CELL_SIZE)
COLS = WIDTH // CELL_SIZE
clock = pygame.time.Clock()


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
board_skin = pygame.image.load('Assets/Boards/board_tarzan.png')

Assets = {
    1: b_bishop,
    2: b_king,
    3: b_knight,
    4: b_pawn,
    5: b_queen,
    6: b_rook,
    7: w_bishop,
    8: w_king,
    9: w_knight,
    10: w_pawn,
    11: w_queen,
    12: w_rook,
    13: board_skin
}

# FONTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

font1 = pygame.font.Font('Assets/Fonts/Helvetica/helvetica-condensed-light')
font2 = pygame.font.SysFont('cursive', 25)
