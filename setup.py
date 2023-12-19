import pygame

FPS = 60

L_PAD = 0
R_PAD = 0
U_PAD = 0
D_PAD = 0

WIDTH = 600 + L_PAD + R_PAD
HEIGHT = 600 + U_PAD + D_PAD
SCREEN = WIDTH, HEIGHT
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
_board_x_bound = [x + L_PAD for x in range(0, WIDTH - R_PAD - L_PAD + 1) if x % CELL_SIZE == 0]
SQUARE_BOUNDARIES_X = {
    # X, a-h file -> int
    (_board_x_bound[0], _board_x_bound[1]): 0,
    (_board_x_bound[1], _board_x_bound[2]): 1,
    (_board_x_bound[2], _board_x_bound[3]): 2,
    (_board_x_bound[3], _board_x_bound[4]): 3,
    (_board_x_bound[4], _board_x_bound[5]): 4,
    (_board_x_bound[5], _board_x_bound[6]): 5,
    (_board_x_bound[6], _board_x_bound[7]): 6,
    (_board_x_bound[7], _board_x_bound[8]): 7
}
_board_y_bound = [x + U_PAD for x in range(0, HEIGHT - D_PAD + 1) if x % CELL_SIZE == 0]
SQUARE_BOUNDARIES_Y = {
    # Y, 8-1 rank -> int
    (_board_y_bound[0], _board_y_bound[1]): 0,
    (_board_y_bound[1], _board_y_bound[2]): 1,
    (_board_y_bound[2], _board_y_bound[3]): 2,
    (_board_y_bound[3], _board_y_bound[4]): 3,
    (_board_y_bound[4], _board_y_bound[5]): 4,
    (_board_y_bound[5], _board_y_bound[6]): 5,
    (_board_y_bound[6], _board_y_bound[7]): 6,
    (_board_y_bound[7], _board_y_bound[8]): 7
}


print(_board_x_bound, SQUARE_BOUNDARIES_X)
print(_board_y_bound, SQUARE_BOUNDARIES_Y)

# FONTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# font1 = pygame.font.Font('Assets/Fonts/Helvetica/helvetica-condensed-light')
# font2 = pygame.font.SysFont('cursive', 25)

