import pygame
import os
from pygame.locals import *
import config as cf
import setup as st
import Class.Sprites as sprites
import Class.Board as brd
 
class App:
    def __init__(self):
        self._running = True
        self.screen = pygame.display.set_mode(st.SCREEN, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.state = brd.Board(cf.starting_position)
        self.initial_square = []
        self.target_square = []
        self.perspective = 0           # White = 0, Black = 1
        print(self.state.board)
 
    def main(self):
        # Event handler
        while self._running:

            for event in pygame.event.get():
                #print(event)
                self.onEvent(event)
            self.onLoop()
            self.render()

        self.cleanup()

    def cleanup(self):
        pygame.quit()
 
    def onEvent(self, event):
        match event.type:
            case pygame.QUIT:
                self._running = False
            case pygame.MOUSEBUTTONUP:
                if len(self.initial_square) == 0:
                    square = self.getClickedSquare(pygame.mouse.get_pos())
                    if self.state.board[square[1]][square[0]] != 0:
                        self.initial_square = [square[1], square[0]]
                else:
                    square = self.getClickedSquare(pygame.mouse.get_pos())
                    self.target_square = [square[1], square[0]]
                    print(f'\nSELECTED SQUARE: {self.initial_square}\nTARGET SQUARE: {self.target_square}')
                    print(self.state.indexToMove(self.initial_square, self.target_square))
                    self.initial_square = []
                    self.target_square = []

    """
    Returns the board index of a square that was clicked.

    Output = [rank index, file index]
    """
    def getClickedSquare(self, 
                   pos: tuple
                   ) -> list:
        res = [-1, -1]
        for x_range in st.SQUARE_BOUNDARIES_X:
            if x_range[0] <= pos[0] <= x_range[1]:
                res[0] = (st.SQUARE_BOUNDARIES_X[x_range])
        for y_range in st.SQUARE_BOUNDARIES_Y:
            if y_range[0] <= pos[1] <= y_range[1]:
                res[1] = (st.SQUARE_BOUNDARIES_Y[y_range])
        return res

    def onLoop(self):
        pass

    def render(self):
        piece_sprites = pygame.sprite.Group()
        board_render = sprites.Board('tarzan')
        piece_sprites.add(board_render)
        for i, rank in enumerate(self.state.board):
            for j, piece in enumerate(rank):
                if piece == 0:
                    continue
                else:
                    coords = self.getSquareCoordinates(1, (j, i))
                    render = self.getPieceSprite(piece, coords)
                    piece_sprites.add(render)
        piece_sprites.draw(self.screen)

        pygame.display.update()
    
    
    def getSquareCoordinates(
            self,
            input_type: int,            # 0 = tuple(('a', 3)) -> coords((0, 375)), 1 = index((0, 2)) -> coords ((0, 450))
            square: tuple, 
            files = st.FILE_LETTERS, 
            ranks = st.RANK_INDEX,
            cell_size = st.CELL_SIZE
    ) -> tuple:
        if input_type == 0:
            return ((files[square[0]] * cell_size) - 5, 
                    (ranks[square[1]] * cell_size) - 10)
        elif input_type == 1:
            return (st.L_PAD + (square[0] * cell_size) - 5, 
                    st.U_PAD + (square[1] * cell_size) - 10)

    def getPieceSprite(self,
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
    
    def playerTurn(self):
        turn = True
        playermove = tuple()
        while turn:
            os.system('clear')
            print(f'\n======= Move {self.state.move_number} =======')
            print(self.state.board)
            print(self.state.active_color[1][self.state.active_color[0]])
            playermove = self.state.moveStrConvert(input("Enter a move: "))
            if playermove is None:
                continue
            elif playermove[6] == 97:
                continue
            elif self.state.moveScan(playermove):
                offset = self.state.moveScan(playermove)
                break

        match playermove[6]:
            case 99:
                #os.system('clear')
                if self.state.active_color[0] == 0:
                        print('Winner: Black')
                else:
                        print('Winner: White')
            case 98:
                #Draw
                pass

        self.state.movePiece(playermove, offset)





if __name__ == "__main__" :
    pygame.init()
    App().main()