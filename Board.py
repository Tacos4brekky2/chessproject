import numpy as np
import regex as re


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
    Generates the initial board position from the input starting position list.
    ex.
        Input (FEN, Default position) = ['rnbqkbnr', 'pppppppp', '8', '8', '8', '8', 'PPPPPPPP', 'RNBQKBNR', 'w', 'KQkq', '-', '0', '1']

    TODO: Only populates empty ranks (8)
          Can't understand something like 4PPPP
    """
    def populateBoard(self):
        for r in range(7, -1, -1):
            for f in range(0, 8):
                if 49 <= ord(self.position[r][f:f+1]) <= 56:
                    for i in range(f, int(self.position[r][f:f+1])):
                        self.board[r][i] = 0
                    break
                if f > (len(self.position[r]) - 1):
                    break
                if 65 <= ord(self.position[r][f:f+1]) <= 90:
                    self.board[r][f] = self.piece_numbers[self.position[r][f:f+1].lower()]
                else:
                    self.board[r][f] = -self.piece_numbers[self.position[r][f:f+1].lower()]


        

    def movePiece(self, 
                  move_str: str):

        playermove = self.moveStrConvert(move_str)
        piece_pos = self.moveScan(playermove)

        print(f'piece_pos = {piece_pos}')

        # Set starting square to empty
        if playermove[0] == 0:
            self.board[playermove[3]][playermove[2]] = playermove[1]
            self.board[playermove[3] - piece_pos[1]][playermove[2] + piece_pos[0]] = 0
        elif playermove[0] == 1:
            self.board[playermove[3]][playermove[2]] = -playermove[1]
            self.board[playermove[3] + piece_pos[1]][playermove[2] - piece_pos[0]] = 0
        print(f'piece_pos = {piece_pos}')
        
        
    """
    (white/black (1/0), piece, file, rank, disambiguation (rank), disambiguation (file))

    e4 -> pe4 -> (x, 0, 4, 4, 0)
    nxf6 -> nf6 -> (x, 2, 5, 2, 0)

    """
    def moveStrConvert(self,
                       move_str: str) -> tuple:
        move = move_str.lower().replace('x', '')
        if len(move) == 2:
            move = 'p' + move

        # Pawn captures
        if re.match('[a-h][a-h][1-8]', move):
            res = (self.active_color[0], 1, self.file_letters[move[1:2]], 8 - int(move[2:3]), 11, self.file_letters[move[:1]])

        # Disambiguation parsing
        elif re.match('[a-h][1-8][a-h][1-8]', move):
            res = (self.active_color[0], self.piece_numbers[move[:1]], self.file_letters[move[2:3]], 8 - int(move[3:4]), 8 - int(move[1:2]), 69)
        elif re.match('[a-h][a-h][a-h][1-8]', move):
            res = (self.active_color[0], self.piece_numbers[move[:1]], self.file_letters[move[2:3]], 8 - int(move[3:4]), 69, self.file_letters[move[1:2]])
        elif re.match('[a-h][a-h][1-8][a-h][1-8]', move):
            res = (self.active_color[0], self.piece_numbers[move[:1]], self.file_letters[move[3:4]], 8 - int(move[4:5]), 8 - int(move[2:3]), self.file_letters[move[1:2]])
        else:
            res = (self.active_color[0], self.piece_numbers[move[:1]], self.file_letters[move[1:2]], 8 - int(move[2:3]), 69, 69)

        if move == 'o-o':
            return (self.active_color[0], 20)
        elif move == 'o-o-o':
            return (self.active_color[0], 30)
        
        return res
    

    def isValidMove(self,
                    move_str: str) -> bool:
        move = move_str.lower().replace('x', '')
        castle = ['o-o', 'o-o-o']
        if move in castle:
            return True
        for x in move:
            if (97 <= ord(x) <= 122) and (x in self.piece_numbers.keys() or x in self.file_letters.keys()):
                continue
            elif 49 <= ord(x) <= 56:
                continue
            else:
                return False
        return True
    

    def moveScan(self,
                 move: tuple):
        lines = {
            'vertical': [(0, x) for x in range(-7, 8) if x != 0],
            'horizontal': [(x, 0) for x in range(-7, 8) if x != 0],
            'diagonal_1': [(x, x) for x in range(-7, 8) if x != 0],
            'diagonal_2': [(x, -x) for x in range(-7, 8) if x != 0]
        }
        vector_dict = {
            11: [(1, 1) if self.active_color[0] == 1 else (1, -1),
                 (-1, 1) if self.active_color[0] == 1 else (-1, -1)],
            1: [(0, 1) if self.active_color[0] == 1 else (0, -1), 
                (0, 2) if self.active_color[0] == 1 else (0, -2)],
            2: lines['diagonal_1'] +
                 lines['diagonal_2'],
            3: [(1, 2), (-1, 2), (1, -2), (-1, -2), 
                (2, 1), (2, -1), (-2, 1), (-2, -1)],
            4: lines['horizontal'] + 
                 lines['vertical'],
            5: lines['vertical'] +
                 lines['horizontal'] +
                 lines['diagonal_1'] +
                 lines['diagonal_2'],
            6: [(0, 1), (1, 1), (1, 0), (1, -1), 
                (0, -1), (-1, -1), (-1, 0), (-1, 1)]
        }
        if move[4] == 11:
            vectors = vector_dict[11]
        else:
            vectors = vector_dict[move[1]]

        piece_scan = []
        print(f'\nMove: {move}')
        for v in vectors:
            print(v)
            # Ignore moves that place pieces off of the board.
            if (
                (v[0] > 0 and move[2] + v[0] > 7) or 
                (v[0] < 0 and move[2] + v[0] < 0) or 
                (v[1] > 0 and move[3] - v[1] < 0) or 
                (v[1] < 0 and move[3] - v[1] > 7)
            ):
                continue
            # Scan for requested piece from destination square
            elif (
                (move[0] == 0) and
                (self.board[move[3] - v[1]][move[2] + v[0]] == move[1])
            ):
                piece_scan.append((v[0], v[1]))
            elif (
                (move[0] == 1) and
                (self.board[move[3] - v[1]][move[2] + v[0]] == -move[1])
            ):
                piece_scan.append((-v[0], -v[1]))
        # Check for collisions (pawn, bishop, rook, queen)
        if len(piece_scan) > 1:
            for x in piece_scan:
                if (move[5] != 69) and (abs(x[0]) == move[5]):
                    piece_scan.remove(x)
                if (move[4] != 69) and (abs(x[0]) == move[4]):
                    piece_scan.remove(x)
                
        print(f'Scanned Pieces: {piece_scan}\n')
        return piece_scan[0]