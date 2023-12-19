from Class.Board import Board
import boardtests
import config
import os


board = Board(config.starting_position)

def playerTurn():
    player_turn = board.active_color[0]
    playermove = tuple()

    while True:
        os.system('clear')
        print(f'\n======= Move {board.move_number} =======')
        print(board.board)
        print(board.active_color[1][player_turn])
        playermove = board.moveStrConvert(input("Enter a move: "))
        if playermove is None:
             continue
        elif playermove[6] == 97:
             continue
        elif board.moveScan(playermove):
            offset = board.moveScan(playermove)
            break

    match playermove[6]:
        case 99:
            #os.system('clear')
            if board.active_color[0] == 0:
                    print('Winner: Black')
            else:
                    print('Winner: White')
        case 98:
            #Draw
            pass

    board.movePiece(playermove, offset)

