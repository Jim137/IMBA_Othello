from othello.othello import pvp, load_from_txt, GreedyBot,ML_process
from algorithm.Minimax import Min_Player, Max_Player
from othello.util.game import game

def IsingModel_white():
    match = game()
    match.print_board()
    while match.end == False:
        if match.turn == 1:
            pos = Max_Player(match, 3)
        else:
            print('Your turn')
            print('Your valid moves:', str(
                match.pos_name(match.valid_move_black())).upper())
            pos = input(
                'Please enter the position you want to place a piece: ').lower().strip()

        if match.to_place(pos):
            match.print_board()
        else:
            print('Invalid position. Please try again.')
    print('Game over. The winner is', match.winner())
    return

def IsingModel_black():
    match = game()
    match.print_board()
    while match.end == False:
        if match.turn == -1:
            pos = Min_Player(match, 1)
        else:
            print('Your turn')
            print('Your valid moves:', str(
                match.pos_name(match.valid_move_white())).upper())
            pos = input(
                'Please enter the position you want to place a piece: ').lower().strip()

        if match.to_place(pos):
            match.print_board()
        else:
            print('Invalid position. Please try again.')
    print('Game over. The winner is', match.winner())
    return

if __name__ == "__main__":
    # pvp()
    # boards = load_from_txt('train_data/15x1_w.txt')
    # GreedyBot(1)
    # ML_process()
    IsingModel_black()
    # IsingModel_white()