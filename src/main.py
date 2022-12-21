from algorithm.ML import *
from othello.othello import pvp, load_from_txt, GreedyBot

def ML_process():
    boards = load_from_txt('train_data/15x1_w.txt')
    x = generate_x(boards)
    y = generate_y(boards)
    KNR(x,y)

if __name__ == "__main__":
    # pvp()
    # boards = load_from_txt('train_data/15x1_w.txt')
    # GreedyBot(2)
    ML_process()