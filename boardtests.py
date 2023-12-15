from Board import Board

# Switchboard
board_attributes = 0
movePiece = 0



# Logic
if board_attributes == 1:
    print(
f"""\n ======= Board Attributes =======\n
Starting position: {Board().position}
Move number: {Board().move_number}
Halfmove clock: {Board().fifty_move_count}
En passant target: {Board().en_passant_target}
Active color: {Board().active_color[0]}
Castling rights:
    (White): Kingside = {Board().can_castle[(0, 'o-o')]} | Queenside = {Board().can_castle[(0, 'o-o-o')]}
    (Black): Kingside = {Board().can_castle[(1, 'o-o')]} | Queenside = {Board().can_castle[(1, 'o-o-o')]}
"""
)