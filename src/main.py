from othello.othello import pvp, load_from_txt, GreedyBot,ML_process, IsingModel_black, IsingModel_white
from algorithm.Minimax import Min_Player, Max_Player
from othello.util.game import game



if __name__ == "__main__":
    # pvp()
    # boards = load_from_txt('train_data/15x1_w.txt')
    # GreedyBot(1)
    file = ['train_data/15x1_w.txt','train_data/15x2_w.txt']
    ML_process(file, 10) #mobility parameter
    # IsingModel_black(5)
    # IsingModel_white(5)