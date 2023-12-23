import numpy as np
import regex as re
import config
import setup as st
import os
from collections import defaultdict


class Board():
    def __init__(self, 
                 fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.position = re.split('[/ ]', fen)
        self.active_color = st.PLAYER_WHITE if self.position[8] == 'w' else st.PLAYER_BLACK
        self.opposite_color = st.PLAYER_WHITE if self.active_color == st.PLAYER_BLACK else st.PLAYER_BLACK
        self.lines = {
            'up': [(0, x) for x in range(1, 8)],
            'down': [(0, -x) for x in range(1, 8)],
            'right': [(x, 0) for x in range(1, 8)],
            'left': [(-x, 0) for x in range(1, 8)],
            'right_up': [(x, x) for x in range(1, 8)],
            'right_down': [(x, -x) for x in range(1, 8)],
            'left_up': [(-x, x) for x in range(1, 8)],
            'left_down': [(-x, -x) for x in range(1, 8)]
        }
        self.offsets = {
            -1: [(0, -1), (0, -2), (-1, -1), (1, -1)],          # Black Pawn
            1: [(0, 1), (0, 2), (1, 1), (-1, 1)],               # White Pawn
            2: self.lines['right_up'] +                         # Bishop
                self.lines['right_down'] +
                self.lines['left_up'] +
                self.lines['left_down'],
            3: [(1, 2), (-1, 2), (1, -2), (-1, -2),             # Knight
                (2, 1), (2, -1), (-2, 1), (-2, -1)],
            4: self.lines['up'] +                               # Rook
                self.lines['down'] +
                self.lines['right'] +
                self.lines['left'],
            5: self.lines['up'] +                               # Queen
                self.lines['down'] +
                self.lines['right'] +
                self.lines['left'] +
                self.lines['right_up'] +
                self.lines['right_down'] +
                self.lines['left_up'] +
                self.lines['left_down'],
            6: [(0, 1), (1, 1), (1, 0), (1, -1),                # King
                (0, -1), (-1, -1), (-1, 0), (-1, 1)],
            7: [[self.lines['up'],                              # Check scan
                self.lines['down'],
                self.lines['right'],
                self.lines['left']],
                [self.lines['right_up'],
                self.lines['right_down'],
                self.lines['left_up'],
                self.lines['left_down']]]
        }
        self.in_check = {
            st.PLAYER_WHITE: 0,
            st.PLAYER_BLACK: 0
        }
        self.king_pos = {
            st.PLAYER_WHITE: [7, 4],
            st.PLAYER_BLACK: [0, 4]
        } # RF INDEX
        self.checked_by = {
            st.PLAYER_WHITE: [],
            st.PLAYER_BLACK: []}
        self.legal_moves = list()

        self.move_number = int(self.position[12]) - 1
        self.fifty_move_count = int(self.position[11])
        self.can_castle = {
            (st.PLAYER_WHITE, 'o-o'): True if 'K' in self.position[9] else False,       # White kingside
            (st.PLAYER_WHITE, 'o-o-o'): True if 'Q' in self.position[9] else False,     # White queenside
            (st.PLAYER_BLACK, 'o-o'): True if 'k' in self.position[9] else False,       # Black kingside
            (st.PLAYER_BLACK, 'o-o-o'): True if 'q' in self.position[9] else False
        }     # Black queenside
        self.board = np.zeros((8, 8))
        self.file_letters = {
            'a': 0, 'b': 1, 'c': 2, 'd': 3,
            'e': 4, 'f': 5, 'g': 6, 'h': 7
        }
        self.piece_numbers = {
            'p': 1, 'b': 2, 'n': 3, 
            'r': 4, 'q': 5, 'k': 6
        }
        self.function_count = defaultdict(int)
        self.en_passant_target = (0, 0) if self.position[10] == '-' else (self.file_letters[self.position[10][0]], 8 - int(self.position[10][1]))
        self.populateBoard()
        self.startTurn(self.active_color)
    

    """
    --- Generates the initial board position on start ---
    ** Single-use
    (Modifies initial empty board array in place)

    Algorithm:
        - Takes a converted FEN string as input *(self.position): list.
        - Iterates through the ranks from 1-8,
            through the squares in each rank from a-h.
        - Places the integer equivalents of the pieces on
            their respective squares. -> Positive integers for white, negative integers for black.
        - If a number is found that represents a series of empty squares,
            perform an equivalent number of loops to mark each square as
            empty.

    TODO: Only populates empty ranks (8)
          Can't understand something like 4PPPP
    """
    def populateBoard(self):
        for r in range(7, -1, -1):
            for i, f in enumerate(self.position[r]):
                if re.match('[1-8]', f):
                    for n in range(int(f), int(self.position[r][int(i)])):
                        self.board[r][n] = 0
                elif re.match('[PBNRKQ]', f):
                    self.board[r][i] = self.piece_numbers[f.lower()]
                elif re.match('[pbnrkq]', f):
                    self.board[r][i] = -self.piece_numbers[f.lower()]

 
    """
    --- Executes a move ---
    ** MAIN FUNCTION

    Functionality:
        - Moves a piece to its destination square.
        - Marks the square previously occupied by said piece as empty.
        - Resets half move clock if no capture has been made.  Increments half move clock otherwise.
    """


    def movePiece(
            self,
            move: tuple
    ) -> None:
        self.function_count['board.movePiece'] += 1
        king_x = self.king_pos[st.PLAYER_WHITE][1] if move[0] == st.PLAYER_WHITE else self.king_pos[st.PLAYER_BLACK][1]
        king_y = self.king_pos[st.PLAYER_WHITE][0] if move[0] == st.PLAYER_WHITE else self.king_pos[st.PLAYER_BLACK][0]
        tmp = self.board[move[4]][move[5]]
        tmp_king_pos = [king_y, king_x]
        self.board[move[4]][move[5]] = move[1]
        self.board[move[2]][move[3]] = 0
        if abs(move[1]) == 6:
            king_x = move[5]
            king_y = move[4]
        if len(self.checkScan(move[0], king_x, king_y)) > 0:
            self.board[move[4]][move[5]] = tmp
            self.board[move[2]][move[3]] = move[1]
            self.king_pos[move[0]] = tmp_king_pos
        else:
            if abs(move[1]) == 6:
                self.king_pos[move[0]] = [move[4], move[5]]
            self.in_check[move[0]] = 0
            if len(self.checkScan(
                self.opposite_color,
                self.king_pos[move[0] * -1][1],
                self.king_pos[move[0] * -1][0])
            ) > 0:
                self.in_check[move[0] * -1] = 1
            self.incrementFiftyMoveCounter(tmp)
            self.startTurn(move[0] * -1)
                # print(f'''
# ===== Board.movePiece() =====
# WHITE KING POS (Ri, Fi): {self.king_pos[0]}
# BLACK KING POS (Ri, Fi): {self.king_pos[1]}
# TURN: {self.active_color[1][move[0]]}
# MOVE: {move}
# ===========================
#             ''')


    """
    *** OUTPUTS NEW MOVE TUPLE FORMAT ***
    --- Converts initial and target move squares to a move tuple ---
    Input:
        - initial = [initial rank index, initial file index]
        - target = [target rank index, target file index]
    
    Output -> move(tuple(int))
        Index   Meaning
        0       white/black (0/1)
        1       piece number
        2       initial rank
        3       initial file
        4       target rank
        5       target file
    """
    def indexToMove(self,
                    initial: list,
                    target: list
                    ) -> tuple:
        
        self.function_count['board.indexToMove'] += 1
        return (
            self.active_color, 
            self.board[initial[0]][initial[1]],
            initial[0],
            initial[1],
            target[0],
            target[1]
        )
    

    def getLegalMoves(
            self,
            color: int
    ) -> list:
        """ Returns all of a player's legal move tuples.
    """
        self.function_count['board.getLegalMoves'] += 1
        legal_moves = list()
        for r, rank in enumerate(self.board):
            for f, piece in enumerate(rank):
                if (piece / color > 0):
                    offset_key = abs(piece) if piece != st.BLACK_PAWN else -1
                    for offset in self.offsets[offset_key]:
                        if self.isValidOffset(r, f, offset):
                            move = (color, int(piece), r, f, r - offset[1], f + offset[0])
                            if (self.isValidMove(move)):
                                tmp_origin = self.board[move[2], move[3]]
                                tmp_target = self.board[move[4]][move[5]]
                                tmp_king_origin = self.king_pos[color]

                                if (abs(move[1]) == 6):
                                    self.king_pos[color] = move[4], move[5]

                                self.board[move[4]][move[5]] = tmp_origin
                                self.board[move[2], move[3]] = 0
                                if len(self.checkScan(color, self.king_pos[color][1], self.king_pos[color][0])) != 0:
                                    self.board[move[4]][move[5]] = tmp_target
                                    self.board[move[2]][move[3]] = tmp_origin
                                    self.king_pos[color] = tmp_king_origin
                                    continue
                                self.board[move[4]][move[5]] = tmp_target
                                self.board[move[2]][move[3]] = tmp_origin
                                self.king_pos[color] = tmp_king_origin
                                legal_moves.append(move)
        print(legal_moves)
        return legal_moves
    
    

    def isValidMove(self,
                    move: tuple) -> bool:
        self.function_count['board.isValidMove'] += 1
        target_square = self.board[move[4]][move[5]]
        # Trying to capture a friendly piece.
        if (
            ((move[0] == st.PLAYER_WHITE) and (target_square > 0)) or
            ((move[0] == st.PLAYER_BLACK) and (target_square < 0))
        ):
            return False
        offset = (move[5] - move[3], move[2] - move[4])
        offset_key = abs(move[1]) if move[1] != st.BLACK_PAWN else -1
        # Invalid pawn captures.
        if (
            (abs(move[1]) == 1) and
            ((offset[0] != 0) and (target_square == 0)) or
            ((offset [0] == 0) and (target_square != 0))
        ):
            return False
        if offset in self.offsets[offset_key]:
            return self.willNotCollide(move, self.offsets[offset_key], offset)
        return False
    

    def willNotCollide(self,
                        move: tuple,
                        vectors: list,
                        offset: tuple
    ) -> bool:
        """ isValidMove() helper function.

    Returns True if no collisions are detected.

    Pieces checked:
        - Pawn
        - Bishop
        - Rook
        - Queen
    """
        
        self.function_count['board.willNotCollide'] += 1
        if move[1] == 3:
            return True
        path = []
        if (offset[0] == 0) and (offset[1] < 0):                                                # Up
            path = [x for x in vectors if (x[0] == 0) and (offset[1] < x[1] < 0)]
        elif (offset[0] == 0) and (offset[1] > 0):                                              # Down
            path = [x for x in vectors if (x[0] == 0) and (0 < x[1] < offset[1])]
        elif (offset[0] < 0) and (offset[1] < 0):                                               # Right Up
            path = [x for x in vectors if (offset[0] < x[0] < 0) and (offset[1] < x[1] < 0)]
        elif (offset[0] > 0) and (offset[1] < 0):                                               # Left up
            path = [x for x in vectors if (0 < x[0] < offset[0]) and (offset[1] < x[1] < 0)]
        elif (offset[0] < 0) and (offset[1] == 0):                                              # Right
            path = [x for x in vectors if (offset[0] < x[0] < 0) and (x[1] == 0)]
        elif (offset[0] > 0) and (offset[1] == 0):                                              # Left
            path = [x for x in vectors if (0 < x[0] < offset[0]) and (x[1] == 0)]
        elif (offset[0] < 0) and (offset[1] > 0):                                               # Right Down
            path = [x for x in vectors if (offset[0] < x[0] < 0) and (0 < x[1] < offset[1])]
        elif (offset[0] > 0) and (offset[1] > 0):                                               # Left Down
            path = [x for x in vectors if (0 < x[0] < offset[0]) and (0 < x[1] < offset[1])]
        
        for x in path:
            if self.board[move[2] - x[1]][move[3] + x[0]] != 0:
                return False
        return True
    

    def isValidOffset(
        self,
        piece_rank: int,
        piece_file: int,
        offset: tuple
    ) -> bool:
        """ Returns true if an offset moves a piece within the board
    """
        self.function_count['board.isValidOffset'] += 1
        if (
            (0 <= (piece_rank - offset[1]) <= 7) and
            (0 <= (piece_file + offset[0]) <= 7)
        ):
            return True
        return False

    
    def checkScan(self,
                  color: int,
                  king_x: list,
                  king_y: list
    ) -> list:
        """ Scans for opponent's pieces using their respective movement vectors.

        Starts from king and moves out.
        Iterates over each vector individually.
    """
        self.function_count['board.checkScan'] += 1
        diagonal = [[]] * 4
        straight = [[]] * 4
        knight = list()

        for i, vector in enumerate(self.offsets[7][1]):
            tmp = []
            for offset in vector:
                if (
                    (self.isValidOffset(king_y, king_x, offset))
                ):
                    tmp.append(offset)
            diagonal[i] = tmp
        for i, vector in enumerate(self.offsets[7][0]):
            tmp = []
            for offset in vector:
                if (
                    (self.isValidOffset(king_y, king_x, offset))
                ):
                    tmp.append(offset)
            straight[i] = tmp
        for offset in self.offsets[st.WHITE_KNIGHT]:
            
            if (
                (self.isValidOffset(king_y, king_x, offset))
            ):
                knight.append(offset)
#         print(f'''
# ===== Board.checkScan() =====
# {self.active_color[1][color]} CHECK LIST
# DIAGONAL: {diagonal}
# STRAIGHT: {straight}
# KNIGHT: {knight}
# ''')
        checked_by = []
        for offset in knight:
            #print(offset)
            target_square = self.board[king_y - offset[1]][king_x + offset[0]]
            rf_index = ((king_y - offset[1]), (king_x + offset[0]))
            if target_square == (-3 if color == st.PLAYER_WHITE else 3):
                #print("KNIGHT")
                checked_by.append(rf_index)

        for vector in straight:
            for offset in vector:
                target_square = self.board[king_y - offset[1]][king_x + offset[0]]
                rf_index = ((king_y - offset[1]), (king_x + offset[0]))
                if (
                    (offset in [
                        (0, 1), (0, -1), (1, 0), (-1, 0)
                    ]) and
                    (target_square in [
                        -6 if color == st.PLAYER_WHITE else 6
                    ])
                ):
                    #print("KING")
                    checked_by.append(rf_index)
                    
                if target_square in [
                    -4 if color == st.PLAYER_WHITE else 4,
                    -5 if color == st.PLAYER_WHITE else 5
                ]:
                    #print("RQ")
                    checked_by.append(rf_index)
                elif target_square != 0:
                    break

        for vector in diagonal:
            for offset in vector:
                target_square = self.board[king_y - offset[1]][king_x + offset[0]]
                rf_index = ((king_y - offset[1]), (king_x + offset[0]))
                if (
                    (offset in [
                        (1, 1), (1, -1), (-1, 1), (-1, -1)
                    ]) and
                    (target_square in [
                        -6 if color == st.PLAYER_WHITE else 6,
                        -1 if color == st.PLAYER_WHITE else 1
                    ])
                ):
                    #print("KP")
                    checked_by.append(rf_index)
                elif target_square in [
                    -2 if color == st.PLAYER_WHITE else 2, 
                    -5 if color == st.PLAYER_WHITE else 5
                    ]:
                    #print('BQ')
                    checked_by.append(rf_index)
                elif target_square != 0:
                    break
        #print(f'CHECK LIIIIIIST: {checked_by}')
        return checked_by
        
        #print('==================')
    
    
    def startTurn(
            self,
            color: int
    ) -> None:
        os.system('clear')
        print(f'FUNCTION COUNT: {self.function_count}')
        self.function_count = defaultdict(int)
        if color == st.PLAYER_WHITE:
            self.move_number += 1
        self.active_color = color
        self.opposite_color = color * -1
        self.legal_moves = self.getLegalMoves(color)

        print(f'ACTIVE COLOR: {self.active_color}\nFIFTYMOVE: {self.fifty_move_count}\nMOVE: {self.move_number}')
        if len(self.legal_moves) == 0:
            if self.in_check[color] == 1:
                print("MATE")
            else:
                print("STALEMATE")


    def incrementFiftyMoveCounter(
            self,
            target_piece: int
        ) -> None:
        self.function_count['board.incrementFiftyMoveCounter'] += 1
        if target_piece != 0:
            self.fifty_move_count = 0
        else:
            self.fifty_move_count += 1

    """
    *** NOT IN USE ***
    *** OUTPUTS OLD MOVE TUPLE FORMAT ***

    --- Standardizes algebraic notation inputs for use in the program ---
    ** Base function

    Algorithm:
    - Takes an input string *(move_str) in the form of algebraic notation.
    - Removes 'x' from capturing moves, adds 'p' to pawn moves.
    - Determines the type of move using regular expressions.
    - Returns a standardized tuple containing the integer equivalents
        of the data provided in (move_str).
        - If (move_str) is invalid, returns an empty tuple.

    Functionality:
        - All basic piece moves.
        - Ambiguous moves.
        - Resignation and draw offers.
        - Castling.
        - Invalid or empty move strings.

    Output -> move(tuple(int)):
        Index   Meaning
        0       white/black (0/1) 
        1       piece 
        2       file 
        3       rank 
        4       disambiguation (rank) / pawn capture
        5       disambiguation (file)

    Examples:
    e4 -> pe4 -> (x, 0, 4, 4, 69, 69)
    nxf6 -> nf6 -> (x, 2, 5, 2, 0)

    """
    def moveStrConvert(self,
                       move_str: str) -> tuple:
        move = move_str.lower().replace('x', '')
        if re.match('[a-h][1-8]', move):
            move = 'p' + move
        if re.match('[pbnrkq][a-h][1-8]', move):
            return (self.active_color[0], self.piece_numbers[move[:1]], self.file_letters[move[1:2]], 8 - int(move[2:3]), 69, 69, 0)
        elif re.match('[a-h][a-h][1-8]', move):
            return (self.active_color[0], 1, self.file_letters[move[1:2]], 8 - int(move[2:3]), 69, self.file_letters[move[:1]], 11)
        elif re.match('[a-h][1-8][a-h][1-8]', move):
            return (self.active_color[0], self.piece_numbers[move[:1]], self.file_letters[move[2:3]], 8 - int(move[3:4]), 8 - int(move[1:2]), 69, 0)
        elif re.match('[a-h][a-h][a-h][1-8]', move):
            return (self.active_color[0], self.piece_numbers[move[:1]], self.file_letters[move[2:3]], 8 - int(move[3:4]), 69, self.file_letters[move[1:2]], 0)
        elif re.match('[a-h][a-h][1-8][a-h][1-8]', move):
            return (self.active_color[0], self.piece_numbers[move[:1]], self.file_letters[move[3:4]], 8 - int(move[4:5]), 8 - int(move[2:3]), self.file_letters[move[1:2]], 0)
        elif move == 'resign':
            return (self.active_color[0], 0, 0, 0, 0, 0, 99)
        elif move == 'draw':
            return (self.active_color[0], 0, 0, 0, 0, 0, 98)
        elif move == 'o-o':
            return (self.active_color[0], 0, 0, 0, 0, 0, 20)
        elif move == 'o-o-o':
            return (self.active_color[0], 0, 0, 0, 0, 0, 30)
        else:
            return (0, 0, 0, 0, 0, 0, 97)




