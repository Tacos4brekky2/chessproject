import pygame
from pygame.sprite import Group
import setup as st



class Pawn(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple,
                 rank_index: int,
                 file_index: int):
        super().__init__()
        if color == 1:
            image = st.b_pawn
        else:
            image = st.w_pawn
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)
        self.square = [rank_index, file_index]

    
    def move(
        self,
        target_square: list,
        coords: tuple
    ) -> None:
        self.square = target_square
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)



class Bishop(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple,
                 rank_index: int,
                 file_index: int):
        super().__init__()
        if color == 1:
            self.image = st.b_bishop
        else:
            self.image = st.w_bishop

        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)
        self.square = [rank_index, file_index]

    
    def move(
        self,
        target_square: list,
        coords: tuple
    ) -> None:
        self.square = target_square
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)




class Knight(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple,
                 rank_index: int,
                 file_index: int):
        super().__init__()
        if color == 1:
            self.image = st.b_knight
        else:
            self.image = st.w_knight

        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)
        self.square = [rank_index, file_index]

    
    def move(
        self,
        target_square: list,
        coords: tuple
    ) -> None:
        self.square = target_square
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)




class Rook(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple,
                 rank_index: int,
                 file_index: int):
        super().__init__()
        if color == 1:
            self.image = st.b_rook
        else:
            self.image = st.w_rook

        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)
        self.square = [rank_index, file_index]

    
    def move(
        self,
        target_square: list,
        coords: tuple
    ) -> None:
        self.square = target_square
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)



class Queen(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple,
                 rank_index: int,
                 file_index: int):
        super().__init__()
        if color == 1:
            self.image = st.b_queen
        else:
            self.image = st.w_queen

        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)
        self.square = [rank_index, file_index]

    
    def move(
        self,
        target_square: list,
        coords: tuple
    ) -> None:
        self.square = target_square
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)




class King(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple,
                 rank_index: int,
                 file_index: int):
        super().__init__()
        if color == 1:
            self.image = st.b_king
        else:
            self.image = st.w_king

        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)
        self.square = [rank_index, file_index]

    
    def move(
        self,
        target_square: list,
        coords: tuple
    ) -> None:
        self.square = target_square
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)




class Board(pygame.sprite.Sprite):
    def __init__(self,
                 skin: str,
                 x=st.L_PAD,
                 y=st.U_PAD):
        super().__init__()
        match skin:
            case 'tarzan':
                image = st.board_skin_tarzan
        self.image = pygame.transform.scale(image, (st.WIDTH - st.L_PAD - st.R_PAD, st.HEIGHT - st.U_PAD - st.D_PAD))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)




class Highlight(pygame.sprite.Sprite):
    def __init__(self,
                 skin: str,
                 coords: tuple):
        super().__init__()
        match skin:
            case 'red':
                image = st.square_highlight_red
            case 'yellow':
                image = st.square_highlight_yellow
            case 'blue':
                image = st.square_highlight_blue
            case 'green':
                image = st.square_highlight_green
            case 'circle_red':
                image = st.square_red_circle
        self.image = pygame.transform.scale(image, (75, 75))
        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 10)




class PlayerClock(pygame.sprite.Sprite):
    def __init__(self,
                 skin: str,
                 coords: tuple) -> None:
        super().__init__()
        match skin:
            case 'default_black':
                image = st.gold_border_150x35
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = coords


# Menu ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
menu_list = {
    'main menu': [0, [
        PlayerClock('default_black', (st.L_PAD + 615, st.U_PAD + 135)), 
        PlayerClock('default_black', (st.L_PAD + 615, st.U_PAD + 205))
    ]
],
    'board': [1, [
        Board('tarzan')
    ]
]
}
# Menu ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~