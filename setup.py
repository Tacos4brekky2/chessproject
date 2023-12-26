import pygame

pygame.mixer.init()

FPS = 60

L_PAD = 15
R_PAD = 15
U_PAD = 55
D_PAD = 45

WIDTH = (600 + L_PAD + R_PAD)
HEIGHT = (600 + U_PAD + D_PAD)
SCREEN = WIDTH, HEIGHT
CELL_SIZE = 75
ROWS = 8
COLS = 8

# COLORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# PIECES ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
WHITE_PAWN = 1
BLACK_PAWN = -1
WHITE_BISHOP = 2
BLACK_BISHOP = -2
WHITE_KNIGHT = 3
BLACK_KNIGHT = -3
WHITE_ROOK = 4
BLACK_ROOK = -4
WHITE_QUEEN = 5
BLACK_QUEEN = -5
WHITE_KING = 6
BLACK_KING = -6

# PLAYER COLORS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
PLAYER_WHITE = 1
PLAYER_BLACK = -1

# SKINS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
# Menu
default_menu_box = pygame.image.load('Assets/default_menu_box.png')
menu_box_purple_long = pygame.image.load('Assets/menu_box_purple_long.png')
menu_box_red = pygame.image.load('Assets/menu_box_red.png')
button_red = pygame.image.load('Assets/Buttons/button_red.png')
button_grey = pygame.image.load('Assets/Buttons/button_grey.png')
button_white = pygame.image.load('Assets/Buttons/button_white.png')
trim_bg = pygame.image.load('Assets/demo_trim.png')

# PIECES
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
# BOARDS
board_skin_tarzan = pygame.image.load('Assets/Boards/board_tarzan.png')

# SQUARE OVERLAYS
square_red_circle = pygame.image.load('Assets/red_circle.png')
square_highlight_yellow = pygame.image.load('Assets/Boards/highlight_yellow.png')
square_highlight_green = pygame.image.load('Assets/Boards/highlight_green.png')
square_highlight_blue = pygame.image.load('Assets/Boards/highlight_blue.png')
square_highlight_red = pygame.image.load('Assets/Boards/highlight_red.png')

# AUDIO ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
audio_checkmate = pygame.mixer.Sound('Assets/Audio/checkmate_audio.wav')

# BORDERS
gold_border_150x35 = pygame.image.load('Assets/gold_border.png')

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
    13: board_skin_tarzan,
    14: square_highlight_red
}

# BOARD ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
FILE_LETTERS = {
    'a': 0, 'b': 1, 'c': 2, 'd': 3, 'e': 4, 'f': 5, 'g': 6, 'h': 7,
    0: 'a', 1: 'b', 2: 'c', 3: 'd', 4: 'e', 5: 'f', 6: 'g', 7: 'h'
}
RANK_INDEX = {
    1: 7, 2: 6, 3: 5, 4: 4, 5: 3, 6: 2, 7: 1, 8: 0
}
board_x_bound = [x + L_PAD for x in range(0, WIDTH - R_PAD + 1) if x % CELL_SIZE == 0]
SQUARE_BOUNDARIES_X = {
    # X, a-h file -> int
    (board_x_bound[0], board_x_bound[1]): 0,
    (board_x_bound[1], board_x_bound[2]): 1,
    (board_x_bound[2], board_x_bound[3]): 2,
    (board_x_bound[3], board_x_bound[4]): 3,
    (board_x_bound[4], board_x_bound[5]): 4,
    (board_x_bound[5], board_x_bound[6]): 5,
    (board_x_bound[6], board_x_bound[7]): 6,
    (board_x_bound[7], board_x_bound[8]): 7
}
board_y_bound = [x + U_PAD for x in range(0, HEIGHT - D_PAD + 1) if x % CELL_SIZE == 0]
SQUARE_BOUNDARIES_Y = {
    # Y, 8-1 rank -> int
    (board_y_bound[0], board_y_bound[1]): 0,
    (board_y_bound[1], board_y_bound[2]): 1,
    (board_y_bound[2], board_y_bound[3]): 2,
    (board_y_bound[3], board_y_bound[4]): 3,
    (board_y_bound[4], board_y_bound[5]): 4,
    (board_y_bound[5], board_y_bound[6]): 5,
    (board_y_bound[6], board_y_bound[7]): 6,
    (board_y_bound[7], board_y_bound[8]): 7
}

results = {
    'checkmate': 1,
    'stalemate': 2,
    'resign': 3,
    'draw': 4,
}

# FONTS ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

# font1 = pygame.font.Font('Assets/Fonts/Helvetica/helvetica-condensed-light')
# font2 = pygame.font.SysFont('cursive', 25)

