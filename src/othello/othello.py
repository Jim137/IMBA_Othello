import numpy as np
from .util.game import game


def pvp():
    match = game()
    match.print_board()
    while match.end == False:
        if match.turn == -1:
            print('Black\'s turn')
            print('Valid moves for black:', str(
                match.pos_name(match.valid_move_black())).upper())
        else:
            print('White\'s turn')
            print('Valid moves for white:', str(
                match.pos_name(match.valid_move_white())).upper())
        pos = input(
            'Please enter the position you want to place a piece: ').lower().strip()
        if match.to_place(pos):
            match.print_board()
        else:
            print('Invalid position. Please try again.')
    print('Game over. The winner is', match.winner())


def load_from_txt(fn):
    color, row, col = np.loadtxt(fn, dtype=int, unpack=True)
    for i in range(len(color)):
        if color[i] == 0:
            color[i] = -1
    match = game()
    round = 0
    match.print_board()
    board = [match.get_board()]
    while match.end == False:
        if round == len(color):
            print('Check file', fn, 'for invalid number of moves (Game does not end).')
            return
        if match.turn == color[round]:
            if match.to_place([row[round], col[round]]):
                match.print_board()
                board.append(match.get_board())
                round += 1
            else:
                print('Check file', fn, 'for invalid move at round =.',round+1)
                return
        else:
            print('Check file', fn, 'for invalid turn at round =.',round+1)
            return
    print('Game over. The winner is', match.winner())
    return board
