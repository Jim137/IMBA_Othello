from othello.othello import *
from algorithm.ML import *
import glob

def ML_process(mobility=10.):
    fns = "train_data/[0-9][0-9]x[0-9][0-9]_w.txt"
    fns = glob.glob(fns)
    fns.sort()
    boards = []
    turns = []
    winners = []
    n = 0
    for fn in fns:
        board,turn,winner = load_from_txt(fn)
        boards.extend(board)
        turns.extend(turn)
        winners.extend([winner]*len(board))
        n += 1
    white_turn_boards = []
    black_turn_boards = []
    for i in range(len(boards)):
        if turns[i] == -1: #black
            if winners[i] == 'Black':
                black_turn_boards.append(boards[i])
        elif turns[i] == 1: #white
            if winners[i] == 'White':
                white_turn_boards.append(boards[i])

    #train white model
    white_x = generate_x(white_turn_boards)
    white_y = generate_white_y(white_turn_boards, white_x, mobility)

    KNR(white_x,white_y,'model_white')

    #train black model
    black_x = generate_x(black_turn_boards)
    black_y = generate_black_y(black_turn_boards, black_x, mobility)
    KNR(black_x,black_y,'model_black')
    return

if __name__ == "__main__":
    # pvp()
    # boards = load_from_txt('train_data/15x1_w.txt')
    # GreedyBot(1)
    # ML_process()
    ML(depth=5)
    # Ising_vs_greedy(strategy=2,depth=5)