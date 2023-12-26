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
        self.in_game = False
        self.screen = pygame.display.set_mode(st.SCREEN, pygame.HWSURFACE | pygame.DOUBLEBUF)
        self.menu = 1
        self.initial_square = []
        self.perspective = 0

        self.gui_elements = pygame.sprite.Group()
        self.piece_sprites = pygame.sprite.Group()
        self.board_sprites = pygame.sprite.Group()
        self.main_menu = pygame.sprite.Group()
        self.state = object
        self.clock = pygame.time.Clock()
        self.player_clock_font = pygame.font.SysFont('Comic Sans', 30)
        self.white_time = int
        self.black_time = int
        self.updateSprites()
        self.startGame((120, 120))
 

    # vvvvv Main vvvvv ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        
    def main(self) -> None:
        """ Main loop.
    """
        while self._running:
            #start_time = time.time() # start time of the loop

            for event in pygame.event.get():
                #print(event)
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
        self.clock.tick(st.FPS)
        self.state.clock[st.PLAYER_WHITE] = self.state.player_clock.white_time
        self.white_time = self.state.player_clock.white_time
        self.state.clock[st.PLAYER_BLACK] = self.state.player_clock.black_time
        self.black_time = self.state.player_clock.black_time

        if self.state.final_result == st.results['checkmate']:
            #self.updateSprites()
            pygame.mixer.Sound.play(st.audio_checkmate)
            time.sleep(2)
            self.cleanup()


    def render(self) -> None:
        match self.menu:
            case 0:
                self.main_menu.draw(self.screen)
            case 1:
                self.board_sprites.draw(self.screen)
                white_clock_text = self.player_clock_font.render(str(self.white_time), False, (255, 255, 255))
                black_clock_text = self.player_clock_font.render(str(self.black_time), False, (255, 255, 255))

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

                self.gui_elements.draw(self.screen)
                highlight_sprites.draw(self.screen)
                self.piece_sprites.draw(self.screen)
                self.screen.blit(white_clock_text, ((st.WIDTH // 2) - 17, st.HEIGHT - st.U_PAD + 7))
                self.screen.blit(black_clock_text, ((st.WIDTH // 2) - 17, 8))

                #Menu('button grey', ((st.WIDTH // 2) - 50, 5), (100, 50)),
                #Menu('button white', ((st.WIDTH // 2) - 50, st.HEIGHT - st.R_PAD + 95), (100, 50)),

        pygame.display.update()

    # ^^^^^ Main ^^^^^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


    # VVVVV Menu VVVVV ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    
    def startGame(
            self,
            time_control: tuple
    ) -> None:
        self.state = board.Board((15, 15))
        self.getPieceSprites()
        self.in_game = True



    # ^^^^^ Menu ^^^^^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
        

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
                friendly_sprite = [x for x in self.piece_sprites if x.square == [move[2], move[3]]]
                if (
                    (abs(move[1]) == st.WHITE_PAWN) and
                    (self.state.en_passant_target == [move[4] + move[0], move[5]])
                ):
                    target_sprite = [x for x in self.piece_sprites if x.square == [move[4] + move[0], move[5]]]
                else:
                    target_sprite = [x for x in self.piece_sprites if x.square == [move[4], move[5]]]
                if len(target_sprite) > 0:
                    self.piece_sprites.remove(target_sprite[0])
                coords = self.getTopLeft(1, (move[5], move[4]))
                friendly_sprite[0].move([move[4], move[5]], coords)
                self.state.movePiece(move)

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
        
        self.main_menu.add(sprites.menu_list[0]['gui assets'])
        self.board_sprites.add(sprites.menu_list[1]['board assets'])
        self.gui_elements.add(sprites.menu_list[1]['gui assets'])
        

    def getPieceSprites(
        self,
     ) -> None:
        
        for r, rank in enumerate(self.state.board):
            for f, piece in enumerate(rank):
                coords = self.getTopLeft(1, (f, r))
                piece_dict = {
                    -1: sprites.Pawn(1, coords, r, f),
                    1: sprites.Pawn(0, coords, r, f),
                    -2: sprites.Bishop(1, coords, r, f),
                    2: sprites.Bishop(0, coords, r, f),
                    -3: sprites.Knight(1, coords, r, f),
                    3: sprites.Knight(0, coords, r, f),
                    -4: sprites.Rook(1, coords, r, f),
                    4: sprites.Rook(0, coords, r, f),
                    -5: sprites.Queen(1, coords, r, f),
                    5: sprites.Queen(0, coords, r, f),
                    -6: sprites.King(1, coords, r, f),
                    6: sprites.King(0, coords, r, f)
                }
                if piece != 0:
                    self.piece_sprites.add(piece_dict[piece])

    # ^^^^^ Sprites ^^^^^ ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~


if __name__ == "__main__" :
    pygame.init()
    App().main()