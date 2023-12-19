import pygame
from pygame.locals import *
import config
import setup as st
import Class.Sprites as sprites
import Class.Board as brd
 
class App:
    def __init__(self):
        self._running = True
        self.screen = pygame.display.set_mode(st.SCREEN, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.state = brd.Board()
        self.perspective = 0            # White = 0, Black = 1
        print(self.state.board)
 
    def main(self):
        # Event handler
        while self._running:

            for event in pygame.event.get():
                self.on_event(event)

            self.on_loop()
            self.render()

        self.cleanup()

    def cleanup(self):
        pygame.quit()
 
    def on_event(self, event):
        if event.type == pygame.QUIT:
            self._running = False

    def on_loop(self):
        pass

    def render(self):
        piece_sprites = pygame.sprite.Group()
        board_render = sprites.Board('tarzan')
        piece_sprites.add(board_render)
        for i, r in enumerate(self.state.board):
            for j, f in enumerate(r):
                if f == 0:
                    continue
                else:
                    coords = self.getSquareCoordinates(1, (j, i))
                    render = self.getPiece(-f, coords)
                    piece_sprites.add(render)
        piece_sprites.draw(self.screen)

        pygame.display.update()
    
    
    def getSquareCoordinates(
            self,
            input_type: int,            # 0 = string tuple(('a', 3)) -> coords, 1 = index((0, 2))
            square: tuple, 
            files = st.FILE_LETTERS, 
            ranks = st.RANK_INDEX,
            cell_size = st.CELL_SIZE
    ) -> tuple:
        if input_type == 0:
            return ((files[square[0]] * cell_size) - 5, (ranks[square[1]] * cell_size) - 10)
        elif input_type == 1:
            return ((square[0] * cell_size) - 5, (ranks[square[1] + 1] * cell_size) - 10)

    def getPiece(self,
                 piece_number: int,
                 position: tuple):
        piece_dict = {
            -1: sprites.Pawn(1, position),
            1: sprites.Pawn(0, position),
            -2: sprites.Bishop(1, position),
            2: sprites.Bishop(0, position),
            -3: sprites.Knight(1, position),
            3: sprites.Knight(0, position),
            -4: sprites.Rook(1, position),
            4: sprites.Rook(0, position),
            -5: sprites.Queen(1, position),
            5: sprites.Queen(0, position),
            -6: sprites.King(1, position),
            6: sprites.King(0, position)
        }
        return piece_dict[piece_number]


if __name__ == "__main__" :
    pygame.init()
    App().main()