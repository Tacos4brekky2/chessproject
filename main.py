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
        self.perspective = 0    
        
        self.piece_sprites = pygame.sprite.Group()
        self.board_sprites = pygame.sprite.Group()
        self.gui_elements = pygame.sprite.Group()  
        
        
        self.updateSprites()
 
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
                mouse_pos = pygame.mouse.get_pos()
                if (
                    (st.L_PAD <= mouse_pos[0] <= (st.L_PAD + st.WIDTH)) and
                    (st.U_PAD <= mouse_pos[1] <= (st.L_PAD + st.WIDTH))
                ):
                    square = self.getClickedSquare(mouse_pos)
                    if len(self.initial_square) == 0:
                        if self.state.board[square[1]][square[0]] != 0:
                            self.initial_square = [square[1], square[0]]
                    elif (len(self.initial_square) == 2) and square[1] == self.initial_square[0] and square[0] == self.initial_square[1]:
                        self.initial_square = []
                    else:
                        os.system('clear')
                        self.target_square = [square[1], square[0]]
                        move_tuple = self.state.indexToMove(self.initial_square, self.target_square)
                        print(self.state.mateScan(move_tuple[0]))
                        self.state.movePiece(move_tuple)
                        self.updateSprites()
                        print(f'\nSELECTED SQUARE: {self.initial_square}\nTARGET SQUARE: {self.target_square}\nMOVE: {move_tuple}\nMOVE NUMBER: {self.state.move_number}\nFIFTY MOVE: {self.state.fifty_move_count}')
                        self.initial_square = []
                        self.target_square = []
                        print(f'{self.state.active_color[1][self.state.active_color[0]]}')


    def onLoop(self):
        pass

    def render(self):
        self.board_sprites.draw(self.screen)

        highlight_sprites = pygame.sprite.Group()
        if (
            (len(self.initial_square) == 2)
        ):
            coords = self.getTopLeft(1, (self.initial_square[1], self.initial_square[0]))
            highlight_sprites.add(sprites.Highlight('yellow', coords))
        elif self.state.in_check[0] == 1:
            coords = self.getTopLeft(1, (self.state.king_pos[0][1], self.state.king_pos[0][0]))
            highlight_sprites.add(sprites.Highlight('red', coords))
        elif self.state.in_check[1] == 1:
            coords = self.getTopLeft(1, (self.state.king_pos[1][1], self.state.king_pos[1][0]))
            highlight_sprites.add(sprites.Highlight('red', coords))
        highlight_sprites.draw(self.screen)

        self.piece_sprites.draw(self.screen)
        self.gui_elements.draw(self.screen)

        pygame.display.update()
    
    def updateSprites(self):
        self.gui_elements.empty()
        self.board_sprites.empty()
        self.piece_sprites.empty()
        board_render = sprites.Board('tarzan')
        self.board_sprites.add(board_render)

        for i, rank in enumerate(self.state.board):
            for j, piece in enumerate(rank):
                if piece == 0:
                    continue
                else:
                    coords = self.getTopLeft(1, (j, i))
                    render = self.getPieceSprite(piece, coords)
                    self.piece_sprites.add(render)
    
        self.gui_elements.add(sprites.PlayerClock('default_black', (st.L_PAD + 70, st.U_PAD + 620)))
        self.gui_elements.add(sprites.PlayerClock('default_black', (st.L_PAD + 380, st.U_PAD + 620)))
    
   

    def getClickedSquare(
            self,
            pos: tuple
        ) -> list:
            """Returns the board index of a square that was clicked.
    Output = [file index, rank index]
    """
            
            res = [-1, -1]
            for i, x in enumerate(st.board_x_bound):
                if x < pos[0]:
                    res[0] = st.SQUARE_BOUNDARIES_X[(x, st.board_x_bound[i + 1])]
            for i, y in enumerate(st.board_y_bound):
                if y < pos[1]:
                    res[1] = st.SQUARE_BOUNDARIES_Y[(y, st.board_y_bound[i + 1])]
            return res
     

    def getTopLeft(
            self,
            input_type: int,
            square: tuple, 
            files = st.FILE_LETTERS, 
            ranks = st.RANK_INDEX,
            cell_size = st.CELL_SIZE
    ) -> tuple:
        """Returns the top left coordinates of a square that was clicked.
    Input types:
        - 0: Algebraic notation. ('a', 3)
        - 1: Board index. (file, rank)
    Output: (x, y)
    """

        if input_type == 0:
            return (
                st.L_PAD + (files[square[0]] * cell_size) - 5, 
                st.U_PAD(ranks[square[1]] * cell_size) - 10
            )
        elif input_type == 1:
            return (st.L_PAD + (square[0] * cell_size) - 5, 
                    st.U_PAD + (square[1] * cell_size) - 10
                )
        


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

if __name__ == "__main__" :
    pygame.init()
    App().main()