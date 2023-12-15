from collections import defaultdict

from Board import Board
import boardtests
import config


board = Board(config.starting_position)


while True:
    player_turn = board.active_color[0]
    if player_turn == 0:
        board.move_number += 1
    print(f'\n======= Move {board.move_number} =======')
    print(board.board)
    print(board.active_color[1][player_turn])
    playermove = input("Enter a move: ")
    if playermove == 'q':
        break
    else:
        board.movePiece(playermove)
        
    
    if player_turn == 0:
        board.active_color[0] = 1
    else:
        board.active_color[0] = 0

