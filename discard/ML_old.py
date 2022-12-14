#generate [x]
import sys 
sys.path.append('../')
from othello.util.game import game

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
import pickle
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from ..src.algorithm.vmap import *

def generate_x(boards): #load a file of boards
    output_x = np.zeros((len(boards),64))
    for n, board in enumerate(boards):
        x = np.array(board) 
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
        xixj = xixj.flatten()
        output_x[n][:] = xixj
    return output_x

def generate_white_y(boards, output_x, mobility=10.):
    output_y = np.zeros(len(boards))
    valid_move = 0    

    for n, board in enumerate(boards):
        b = game()
        b.set_board(board)

        valid_move = len(b.valid_move_black()) #think about this
        valid_move = mobility * valid_move 

        for i, x in enumerate(output_x[n]):
            output_y[n] += x * vmap_flat[i]

        output_y[n] -= valid_move
    return output_y

def generate_black_y(boards, output_x, mobility=10.):
    output_y = np.zeros(len(boards))
    valid_move = 0  

    for n, board in enumerate(boards):
        b = game()
        b.set_board(board)

        valid_move = len(b.valid_move_white())
        valid_move = mobility * valid_move

        for i, x in enumerate(output_x[n]):
            output_y[n] += x * vmap_flat[i] 

        output_y[n] += valid_move

    return output_y 

def KNR(x,y,model_name=str):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2 )

    ktable = {'k':[], 'fscore':[], 'accuracy':[], 'precision':[], 'recall':[]}
    
    knr = KNeighborsRegressor(n_neighbors=4, weights="uniform", algorithm="auto", 
        leaf_size=30, p=1, metric="minkowski", metric_params=None, n_jobs=None)
    knr.fit(x_train,y_train)

    prediction = knr.predict(x_test)
    # print('ytest= ', y_test, 'prediction=', prediction)

    pickle.dump(knr,open('model/'+model_name+'.pickle',"wb"))
    return 
    
