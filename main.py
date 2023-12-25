import pygame
import os
from pygame.locals import *
import config as cf
import setup as st
import Class.Sprites as sprites
import Class.Board as board
from threading import Thread
import time
 



class App(Thread):
    def __init__(self):
        super().__init__()
        self._running = True
        self.screen = pygame.display.set_mode(st.SCREEN, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.state = board.Board(cf.starting_position)
        self.initial_square = []
        self.perspective = 0    
        
        self.piece_sprites = pygame.sprite.Group()
        self.board_sprites = pygame.sprite.Group()
        self.gui_elements = pygame.sprite.Group()
        self.clock = pygame.time.Clock()
        
        self.updateSprites()
 

    # vvvvv Main vvvvv ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    def main(self) -> None:
        """ Main loop.
    """
        while self._running:
            #start_time = time.time() # start time of the loop

            for event in pygame.event.get():
                self.onEvent(event)

            self.onLoop()
            self.render()
            #print("FPS: ", 1.0 / (time.time() - start_time)) # FPS = 1 / time to process loop

        self.cleanup()


    def cleanup(self) -> None:
        self.state.player_clock.stop()
        pygame.quit()
 
    def onEvent(
        self,
        event
    ) -> None:
        """ Event handler.
    """
        match event.type:
            case pygame.QUIT:
                self._running = False
            case pygame.MOUSEBUTTONUP:
                mouse_pos = pygame.mouse.get_pos()
                if self.getClickedSquare(mouse_pos) != [-1, -1]:
                    self.playerBoardClick(mouse_pos)


    def onLoop(self) -> None:
        self.clock.tick(60)
        self.state.clock[st.PLAYER_WHITE] = self.state.player_clock.white_time
        self.state.clock[st.PLAYER_BLACK] = self.state.player_clock.black_time


    def render(self) -> None:
        self.board_sprites.draw(self.screen)

        highlight_sprites = pygame.sprite.Group()
        if (len(self.initial_square) == 2):
            coords = self.getTopLeft(1, (self.initial_square[1], self.initial_square[0]))
            highlight_sprites.add(sprites.Highlight('yellow', coords))
        elif self.state.in_check[st.PLAYER_WHITE] == 1:
            coords = self.getTopLeft(1, (self.state.king_pos[st.PLAYER_WHITE][1], self.state.king_pos[st.PLAYER_WHITE][0]))
            highlight_sprites.add(sprites.Highlight('red', coords))
        elif self.state.in_check[st.PLAYER_BLACK] == 1:
            coords = self.getTopLeft(1, (self.state.king_pos[st.PLAYER_BLACK][1], self.state.king_pos[st.PLAYER_BLACK][0]))
            highlight_sprites.add(sprites.Highlight('red', coords))
        highlight_sprites.draw(self.screen)

        self.piece_sprites.draw(self.screen)
        self.gui_elements.draw(self.screen)

        pygame.display.update()

    # ^^^^^ Main ^^^^^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    # vvvvv Player Functions vvvvv ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    def playerBoardClick(
            self,
            mouse_pos: tuple
    ) -> None:
        square = self.getClickedSquare(mouse_pos)
        # Select square.
        if (
            (len(self.initial_square) == 0) and
            (self.state.board[square[0]][square[1]] != 0)
        ):
            self.initial_square = square
        # Attempt to execute move.
        elif (
            (len(self.initial_square) == 2) and
            (square != self.initial_square)    
        ):
            move = self.state.indexToMove(self.initial_square, square)
            if move in self.state.legal_moves:
                self.state.movePiece(move)
                self.updateSprites()
            self.initial_square = []
        else:
            self.initial_square = []

    # ^^^^^ Player Functions ^^^^^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    
    # vvvvv Coordinates vvvvv ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
            
    def getClickedSquare(
            self,
            mouse_pos: tuple
    ) -> list:
        """Returns the board index of a square that was clicked.
    Output = [rank index, file index]
    """
        
        res = [-1, -1]
        if (
            (st.L_PAD <= mouse_pos[0] <= (st.WIDTH - st.R_PAD)) and
            (st.U_PAD <= mouse_pos[1] <= (st.HEIGHT - st.D_PAD))
        ):
            for i, x in enumerate(st.board_x_bound):
                if x < mouse_pos[0]:
                    res[1] = st.SQUARE_BOUNDARIES_X[(x, st.board_x_bound[i + 1])]
            for i, y in enumerate(st.board_y_bound):
                if y < mouse_pos[1]:
                    res[0] = st.SQUARE_BOUNDARIES_Y[(y, st.board_y_bound[i + 1])]
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
        
    # ^^^^^ Coordinates ^^^^^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    

    # vvvvv Sprites vvvvv ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    def updateSprites(
        self
    ) -> None:
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
        

    def getPieceSprite(
        self,
        piece_number: int,
        position: tuple
        ) -> object:
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
    
    # ^^^^^ Sprites ^^^^^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__" :
    pygame.init()
    App().main()