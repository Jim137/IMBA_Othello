#generate [x]
from othello import load_from_txt
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.neighbors import KNeighborsRegressor

import pickle
from sklearn.metrics import accuracy_score, f1_score, recall_score, precision_score
class ML:
    def __init__(self):
        return 

    def generate_x(self,boards):
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

    def generate_y(self, boards):
        output_y = np.zeros(len(boards))
        for i, board in enumerate(boards):
            output_y[i] = self.get_lead(board) * 224

        return output_y 

    def get_lead(self, board): #white -1 black 1
            board = np.array(board).flatten()
            black_count = 0
            white_count = 0
            for i in board:
                if i == 1:
                    black_count += 1
                elif i == -1:
                    white_count += 1

            if black_count > white_count:
                return 1
            elif white_count > black_count:
                return -1
            else:
                return 0

    def KNR(self, x,y):
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.2 )

        ktable = {'k':[], 'fscore':[], 'accuracy':[], 'precision':[], 'recall':[]}
        
        knr = KNeighborsRegressor(n_neighbors=2, weights="uniform", algorithm="auto", 
            leaf_size=30, p=1, metric="minkowski", metric_params=None, n_jobs=None)
        knr.fit(x_train,y_train)

        prediction = knr.predict(x_test)
        print(y_test, prediction)

        pickle.dump(knr,open('model.pickle',"wb"))
        return 
        # df_ktable = df_ktable.append({
        #     'fscore':f1_score(y_test, prediction), 
        #     'accuracy':accuracy_score(y_test, prediction),
        #     'precision':precision_score(y_test, prediction,zero_division= 0),
        #     'recall':recall_score(y_test, prediction)
        # },ignore_index=True)

if __name__ == "__main__":
    
    # boards = [-np.ones((8,8)),np.zeros((8,8)),np.ones((8,8)),-np.ones((8,8)),np.ones((8,8))]
    # x = ML.generate_x(boards)
    # y = ML.generate_y(boards)
    # ML.KNR(x,y)
    boards = load_from_txt('train_data/15x1_w.txt')
    print(boards[0])
    """
    boards = load_from_txt('train_data/15x1_w.txt')
    x = generate_x(boards)
    y = generate_y(boards)
    KN(x,y)
    """
