import pygame
from pygame.sprite import Group
import setup as st



class Pawn(pygame.sprite.Sprite):
    def __init__(
        self, 
        color: str, 
        coords: tuple,
        rank_index: int,
        file_index: int
    ):
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
    def __init__(
        self, 
        color: str, 
        coords: tuple,
        rank_index: int,
        file_index: int
    ):
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
    def __init__(
        self, 
        color: str, 
        coords: tuple,
        rank_index: int,
        file_index: int
    ):
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
    def __init__(
        self, 
        color: str, 
        coords: tuple,
        rank_index: int,
        file_index: int
    ):
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
    def __init__(
        self, 
        color: str, 
        coords: tuple,
        rank_index: int,
        file_index: int
    ):
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
    def __init__(
        self, 
        color: str, 
        coords: tuple,
        rank_index: int,
        file_index: int
    ):
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
                 coords: tuple
    ):
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
                 coords: tuple
    ):
        super().__init__()
        match skin:
            case 'default_black':
                image = st.gold_border_150x35
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = coords


class Menu(pygame.sprite.Sprite):
    def __init__(self,
                 skin: str,
                 coords: tuple,
                 size: tuple,
                 rotation=0
    ):
        super().__init__()
        match skin:
            case 'default menu box':
                image = st.default_menu_box
            case 'menu box purple long':
                image = st.menu_box_purple_long
            case 'menu box red':
                image = st.menu_box_red
            case 'button red':
                image = st.button_red
            case 'button white':
                image = st.button_white
            case 'button grey':
                image = st.button_grey
            case 'trim bg':
                image = st.trim_bg

        self.image = pygame.transform.scale(image, size)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect()
        self.rect.topleft = coords


class CapturedPieces(pygame.sprite.Sprite):
    def __init__(
            self,
            skin: str,
            coords: tuple,
            size: tuple,
            color: int,
            rotation = 0
    ) -> None:
        super().__init__()
        match skin:
            case 'default':
                image = st.default_menu_box

        self.image = pygame.transform.scale(image, size)
        self.image = pygame.transform.rotate(self.image, rotation)
        self.rect = self.image.get_rect()
        self.rect.topleft = coords
        self.color = color
        self.dict = {
            1: 0,
            2: 0,
            3: 0,
            4: 0,
            5: 0,
            6: 0,
        }
        self.value = 0

    
    def add_piece(
            self,
            piece: int
    ):
        self.dict[piece] += 1
        



# Menu ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
menu_list = {
    0: {
        'name': 'main menu',
        'gui assets': [
            Menu('default menu box', (300, 300), (400, 500))
        ]
    },
    1: {'name': 'board',
        'board assets': [
            Board('tarzan'),
            CapturedPieces('default', (st.WIDTH - st.R_PAD - 245, 10), (257, 38), -1),
            CapturedPieces('default', (st.WIDTH - st.R_PAD - 245, st.HEIGHT - st.D_PAD + 10), (257, 38), 1)
        ],
        'gui assets': [
            #Menu('menu box purple long', (0, 0), (150, st.HEIGHT // 2.5)),
            #Menu('menu box purple long', (0, st.HEIGHT - (st.HEIGHT // 2.5)), (150, st.HEIGHT // 2.5), 180),
            #Menu('default menu box', (st.WIDTH - st.R_PAD, 0), (150, 350)),
            Menu('default menu box', (st.L_PAD - 9, 10), (257, 38)),
            Menu('default menu box', (st.L_PAD - 9, st.HEIGHT - st.D_PAD + 10), (257, 38)),
            Menu('trim bg', (0, 0), (st.WIDTH, st.HEIGHT)),
            Menu('button grey', ((st.WIDTH // 2) - 49, 6), (100, 40)),
            Menu('button white', ((st.WIDTH // 2) - 49, st.HEIGHT - st.D_PAD + 2), (100,40)),
            
        ]
    }
}
# Menu ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~