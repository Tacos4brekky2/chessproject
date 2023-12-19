import pygame
import setup as st




class Pawn(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple):
        super().__init__()
        if color == 1:
            image = st.b_pawn
        else:
            image = st.w_pawn
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)



class Bishop(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple):
        super().__init__()
        if color == 1:
            self.image = st.b_bishop
        else:
            self.image = st.w_bishop

        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)




class Knight(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple):
        super().__init__()
        if color == 1:
            self.image = st.b_knight
        else:
            self.image = st.w_knight

        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)




class Rook(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple):
        super().__init__()
        if color == 1:
            self.image = st.b_rook
        else:
            self.image = st.w_rook

        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)



class Queen(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple):
        super().__init__()
        if color == 1:
            self.image = st.b_queen
        else:
            self.image = st.w_queen

        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)




class King(pygame.sprite.Sprite):
    def __init__(self, 
                 color: str, 
                 coords: tuple):
        super().__init__()
        if color == 1:
            self.image = st.b_king
        else:
            self.image = st.w_king

        self.rect = self.image.get_rect()
        self.rect.topleft = (coords[0] + 5, coords[1] + 8)




class Board(pygame.sprite.Sprite):
    def __init__(self,
                 skin: str,
                 x = 0,
                 y = 0):
        super().__init__()
        match skin:
            case 'tarzan':
                image = st.board_skin_tarzan
        self.image = pygame.transform.scale(image, st.SCREEN)
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
