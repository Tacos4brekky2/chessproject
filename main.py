from Class.Board import Board
import boardtests
import config
import os


board = Board(config.starting_position)


while True:
    #os.system('clear')
    player_turn = board.active_color[0]
    playermove = tuple()
    if player_turn == 0:
        board.move_number += 1

    print(f'\n======= Move {board.move_number} =======')
    print(board.board)
    print(board.active_color[1][player_turn])

    while True:
        playermove = board.moveStrConvert(input("Enter a move: "))
        
        if board.moveScan(playermove):
            break
        
    if playermove[6] == 99:
            #os.system('clear')
            if board.active_color[0] == 0:
                    print('Winner: Black')
            else:
                    print('Winner: White')
            break        

    board.movePiece(playermove)
        
    
    if player_turn == 0:
        board.active_color[0] = 1
    else:
        board.active_color[0] = 0

