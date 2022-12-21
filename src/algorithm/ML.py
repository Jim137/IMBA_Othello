#generate [x]
from othello.othello import load_from_txt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor
from othello.util.game import game
import pickle
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score

def generate_x(boards):
        output_x = np.array(np.zeros((len(boards),64)))
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

def generate_y(boards):
    output_y = np.zeros(len(boards))
    for i, board in enumerate(boards):
        b = game()
        b.set_board(board)
        output_y[i] = b.get_lead() * 224
    return output_y 

def KNR(x,y):
    x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2 )

    ktable = {'k':[], 'fscore':[], 'accuracy':[], 'precision':[], 'recall':[]}
    
    knr = KNeighborsRegressor(n_neighbors=2, weights="uniform", algorithm="auto", 
        leaf_size=30, p=1, metric="minkowski", metric_params=None, n_jobs=None)
    knr.fit(x_train,y_train)

    prediction = knr.predict(x_test)
    print(y_test, prediction)

    pickle.dump(knr,open('model/model.pickle',"wb"))
    return 
    # df_ktable = df_ktable.append({
    #     'fscore':f1_score(y_test, prediction), 
    #     'accuracy':accuracy_score(y_test, prediction),
    #     'precision':precision_score(y_test, prediction,zero_division= 0),
    #     'recall':recall_score(y_test, prediction)
    # },ignore_index=True)

if __name__ == "__main__":
    boards = load_from_txt('train_data/15x1_w.txt')
    x = generate_x(boards)
    y = generate_y(boards)
    KNR(x,y)
