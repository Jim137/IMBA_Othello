import numpy as np
from .util.game import game
from algorithm.ML import *

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


def load_from_txt(fn, output=False):
    color, row, col = np.loadtxt(fn, dtype=int, unpack=True)
    for i in range(len(color)):
        if color[i] == 0:
            color[i] = -1
    match = game()
    round = 0
    # match.print_board()
    board = [match.get_board().copy()]
    while match.end == False:
        if round == len(color):
            print('Check file', fn, 'for invalid number of moves (Game does not end).')
            return
        if match.turn == color[round]:
            if match.to_place([row[round], col[round]]):
                # match.print_board()
                board.append(match.get_board().copy())
                round += 1
            else:
                print('Check file', fn, 'for invalid move at round =.',round+1)
                return
        else:
            print('Check file', fn, 'for invalid turn at round =.',round+1)
            return
    print('Game over. The winner is', match.winner())
    return board

def GreedyBot(strategy=1):
    '''
    GreedyBot plays against the player.
    strategy = 1: GreedyBot plays the move that flips the most pieces.
    strategy = 2: GreedyBot plays the move that gives the least actions to the player.
    '''
    match = game()
    match.print_board()
    while match.end == False:
        if match.turn == -1:
            print('Your turn')
            print('Your valid moves:', str(
                match.pos_name(match.valid_move_black())).upper())
            pos = input(
                'Please enter the position you want to place a piece: ').lower().strip()
        else:
            if strategy == 1:
                valid_moves = match.valid_move_white()
                number_of_flips = []
                for i in valid_moves:
                    number_of_flips.append(len(match.pseudo_flip_white(i)))
                pos = valid_moves[number_of_flips.index(max(number_of_flips))]
                
            elif strategy == 2:
                valid_moves = match.valid_move_white()
                number_of_actions = []
                for i in valid_moves:
                    tmp_match = game()
                    tmp_match.set_board(match.get_board())
                    tmp_match.turn = 1
                    tmp_match.to_place(i)
                    number_of_actions.append(len(tmp_match.valid_move_black()))
                pos = valid_moves[number_of_actions.index(min(number_of_actions))]
            else:
                print('Invalid strategy.')
                return
        print('...',pos)
        if match.to_place(pos):
            match.print_board()
        else:
            print('Invalid position. Please try again.')
    print('Game over. The winner is', match.winner())

def ML_process():
    boards = load_from_txt('train_data/15x1_w.txt')
    white_turn_boards = []
    black_turn_boards = []
    for i in range(len(boards)):
        if i%2 == 0: #black
            black_turn_boards.append(boards[i])
        elif i%2 == 1: #white
            white_turn_boards.append(boards[i])

    #train white model
    white_x = generate_x(white_turn_boards)
    white_y = generate_white_y(white_turn_boards, white_x, 1)
    
    KNR(white_x,white_y,'model_white')

    #train black model
    black_x = generate_x(black_turn_boards)
    black_y = generate_black_y(black_turn_boards, black_x, 1)
    KNR(black_x,black_y,'model_black')
    return

def IsingModel(strategy=1):
    '''
    GreedyBot plays against the player.
    strategy = 1: GreedyBot plays the move that flips the most pieces.
    strategy = 2: GreedyBot plays the move that gives the least actions to the player.
    '''
    match = game()
    match.print_board()
    while match.end == False:
        if match.turn == -1:
            print('Your turn')
            print('Your valid moves:', str(
                match.pos_name(match.valid_move_black())).upper())
            pos = input(
                'Please enter the position you want to place a piece: ').lower().strip()
        else:
            if strategy == 1:
                valid_moves = match.valid_move_white()
                number_of_flips = []
                for i in valid_moves:
                    number_of_flips.append(len(match.pseudo_flip_white(i)))
                pos = valid_moves[number_of_flips.index(max(number_of_flips))]
                
            elif strategy == 2:
                valid_moves = match.valid_move_white()
                number_of_actions = []
                for i in valid_moves:
                    tmp_match = game()
                    tmp_match.set_board(match.get_board())
                    tmp_match.turn = 1
                    tmp_match.to_place(i)
                    number_of_actions.append(len(tmp_match.valid_move_black()))
                pos = valid_moves[number_of_actions.index(min(number_of_actions))]
            else:
                print('Invalid strategy.')
                return

        if match.to_place(pos):
            
            match.print_board()
        else:
            print('Invalid position. Please try again.')
    print('Game over. The winner is', match.winner())