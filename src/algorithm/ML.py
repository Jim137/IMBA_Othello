import sys 
sys.path.append('../')
from othello.util.game import game

import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
import pickle
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
from .vmap import *

def generate_white_x(boards): #load a file of boards
    output_xs = np.zeros((len(boards),64))
    for n, board in enumerate(boards): #each board
        x = np.array(board).flatten()

        xixj = np.zeros(len(x)) #sum

        for i in range(len(x)):
            for j in range(len(x)):
                if i == j:
                    continue
                else:
                    xixj[i] += x[i]*x[j]
        output_xs[n][:] = xixj *1

    return output_xs

def generate_black_x(boards): #load a file of boards
    output_xs = np.zeros((len(boards),64))
    for n, board in enumerate(boards): #each board
        x = np.array(board).flatten()

        xixj = np.zeros(len(x)) #sum

        for i in range(len(x)):
            for j in range(len(x)):
                if i == j:
                    continue
                else:
                    xixj[i] += x[i]*x[j]
        output_xs[n][:] = xixj *-1

    return output_xs

def generate_white_y(boards, output_x, mobility=10.):
    output_y = np.zeros(len(boards))
    valid_move = 0  

    for n, board in enumerate(boards):
        b = game()
        b.set_board(board)

        valid_move = len(b.valid_move_white())
        valid_move = mobility * valid_move
        
        for i, s in enumerate(output_x[n]):
            output_y[n] += s * vmap_flat[i]

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
        
        for i, s in enumerate(output_x[n]):
            output_y[n] += s * vmap_flat[i]

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
    
