import numpy as np
import regex as re
import config
import setup as st


class Board():
    def __init__(self, 
                 fen = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"):
        self.position = re.split('[/ ]', fen)
        self.move_number = int(self.position[12]) - 1
        self.fifty_move_count = int(self.position[11])
        self.active_color = [0 if self.position[8] == 'w' else 1, 
                            {0: "White's Turn", 1: "Black's Turn"}]
        self.can_castle = {(0, 'o-o'): True if 'K' in self.position[9] else False,       # White kingside
                           (0, 'o-o-o'): True if 'Q' in self.position[9] else False,     # White queenside
                           (1, 'o-o'): True if 'k' in self.position[9] else False,       # Black kingside
                           (1, 'o-o-o'): True if 'q' in self.position[9] else False}     # Black queenside
        self.board = np.zeros((8, 8))
        self.file_letters = {'a': 0, 'b': 1, 'c': 2, 'd': 3,
                             'e': 4, 'f': 5, 'g': 6, 'h': 7}
        self.piece_numbers = {'p': 1, 'b': 2, 'n': 3, 
                              'r': 4, 'q': 5, 'k': 6}
        self.en_passant_target = (0, 0) if self.position[10] == '-' else (self.file_letters[self.position[10][0]], 8 - int(self.position[10][1]))

        self.populateBoard()
    

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
                #print(i, f)
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
    # def movePiece(self,
    #               playermove: tuple,
    #               offset: tuple):

    #     self.incrementFiftyMoveCounter(playermove)

    #     # Move Piece and set starting square to empty.
    #     if playermove[0] == 0:
    #         self.board[playermove[3]][playermove[2]] = playermove[1]
    #         self.board[playermove[3] - offset[1]][playermove[2] + offset[0]] = 0
    #     elif playermove[0] == 1:
    #         self.board[playermove[3]][playermove[2]] = -playermove[1]
    #         self.board[playermove[3] + offset[1]][playermove[2] - offset[0]] = 0
        
    #     self.changeColor()
    #     self.incrementMove()

    def movePiece(self,
                playermove: tuple
                ):

        self.incrementFiftyMoveCounter(playermove)

        # Move Piece and set starting square to empty.
        self.board[playermove[4]][playermove[5]] = playermove[1]
        self.board[playermove[2]][playermove[3]] = 0
        
        self.changeColor()
        self.incrementMove()
        
    """
    --- Converts initial and target move squares to a move tuple ---

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
        return (
            self.active_color[0], 
            self.board[initial[0]][initial[1]],
            initial[0],
            initial[1],
            target[0],
            target[1]
            )
        

    """
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


    """
    --- Locates the requested piece ---

    Algorithm:
    - Takes the output tuple from moveStrConvert() as input *(move).
    - Determines which list of move vectors to use based on the type
        of piece specified in (move) and assigns the list to *(vectors).
    - Starts from the square that the player wants to move a piece to,
        looks for all pieces of the same type as the one requested that
        can reach this target square using (vectors) and adds their offset 
        from it to a list *(res).                                   (x, y)
    - In most cases, (res) will have only one element.  If the piece to be moved
        is ambiguous and the length of (res) is greater than one,
        iterate over (res) and prune elements that do not match the
        disambiguation flags provided in (move[4]) and/or (move[5]).
    - Res will have exactly one element, which is then returned.

    Functionality:
        - All basic piece moves.
        - Pawn captures.
        - Returns invalid inputs as empty 
            tuples to signal a loop continuation.
        - Passes resignations and draw offers through
            to break the while loops.
    """
    def moveScan(self,
                 move: tuple):
        if (
            (move[6] == 99) or
            (move[6] == 98)
        ):
            return move
        
        lines = {
            'vertical': [(0, x) for x in range(-7, 8) if x != 0],
            'horizontal': [(x, 0) for x in range(-7, 8) if x != 0],
            'diagonal_1': [(x, x) for x in range(-7, 8) if x != 0],
            'diagonal_2': [(x, -x) for x in range(-7, 8) if x != 0]
        }
        vector_dict = {
            11: [(1, 1) if self.active_color[0] == 1 else (1, -1),      # Pawn capture
                 (-1, 1) if self.active_color[0] == 1 else (-1, -1)],
            1: [(0, 1) if self.active_color[0] == 1 else (0, -1),       # Pawn
                (0, 2) if self.active_color[0] == 1 else (0, -2)],
            2: lines['diagonal_1'] +                                    # Bishop
                 lines['diagonal_2'],
            3: [(1, 2), (-1, 2), (1, -2), (-1, -2),                     # Knight
                (2, 1), (2, -1), (-2, 1), (-2, -1)],
            4: lines['horizontal'] +                                    # Rook
                 lines['vertical'],
            5: lines['vertical'] +                                      # Queen
                 lines['horizontal'] +
                 lines['diagonal_1'] +
                 lines['diagonal_2'],
            6: [(0, 1), (1, 1), (1, 0), (1, -1),                        # King
                (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        }
        if move[6] == 11:
            vectors = vector_dict[11]
        else:
            vectors = vector_dict[move[1]]

        res = []
        for v in vectors:
            # Ignore moves that place pieces off of the board.
            if (
                (v[0] > 0 and move[2] + v[0] > 7) or 
                (v[0] < 0 and move[2] + v[0] < 0) or 
                (v[1] > 0 and move[3] - v[1] < 0) or 
                (v[1] < 0 and move[3] - v[1] > 7)
            ):
                continue

            # Scan for requested piece from destination square.
            elif (
                (move[0] == 0) and
                (self.board[move[3] - v[1]][move[2] + v[0]] == move[1])
            ):
                res.append((v[0], v[1]))
            elif (
                (move[0] == 1) and
                (self.board[move[3] - v[1]][move[2] + v[0]] == -move[1])
            ):
                res.append((-v[0], -v[1]))
        if len(res) == 0:
            return res
        # Disambiguation pruning.
        elif len(res) > 1:
            for x in res:
                if (move[5] != 69) and (abs(x[0]) == move[5]):
                    res.remove(x)
                if (move[4] != 69) and (abs(x[0]) == move[4]):
                    res.remove(x)
        
        if move[1] in (1, 2, 4, 5):
            if self.checkCollisions(move,
                                    move[1],
                                    vector_dict[move[1]],
                                    res[0]):
                return ()
        return res[0]
    

    """
    ** moveScan() helper function.

    Pieces checked:
        - Pawn
        - Bishop
        - Rook
        - Queen
    """
    def checkCollisions(self,
                        move: tuple,
                        piece: str,
                        vectors: list,
                        offset: tuple) -> bool:
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
        
        if self.active_color[0] == 0:
            for x in path:
                if self.board[move[3] - x[1]][move[2] + x[0]] != 0:
                    return True
        else:
            for x in path:
                if self.board[move[3] + x[1]][move[2] - x[0]] != 0:
                    return True
        return False
    
    def changeColor(self):
        if self.active_color[0] == 0:
            self.active_color[0] = 1
        else:
            self.active_color[0] = 0

    def incrementMove(self):
        if self.active_color[0] == 1:
            self.move_number += 1

    def incrementFiftyMoveCounter(self,
                              playermove: tuple):
        if self.board[playermove[4]][playermove[5]] != 0:
            self.fifty_move_count = 0
        else:
            self.fifty_move_count += 1


