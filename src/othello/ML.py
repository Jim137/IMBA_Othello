#generate [x]
from othello import load_from_txt
import numpy as np

board = load_from_txt('train_data/15x1_w.txt')
print(board[0])
def generate_x(board=board[0]):
    x = np.array(board) #[0,1,2,3...6,7],[8,9,11,12]
    xixj = np.array(board)
    for i in range(len(board)):
        for j in range(len(board[i])):
            xij = 0
            if i-1 > -1:
                xij += x[i-1][j]*x[i][j]
            if i+1 <8:
                xij += x[i+1][j]*x[i][j]
            if j-1 > -1:
                xij += x[i][j-1]*x[i][j]
            if j+1 < 8:
                xij += x[i][j+1]*x[i][j]
            xixj[i][j] = xij

    xixj = x.flatten()
    return xixj

print(generate_x())