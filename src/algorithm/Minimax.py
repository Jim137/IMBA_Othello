from collections import deque
import sys
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
import pickle
 
sys.path.append('../')
from othello.util.game import game
from othello.util.board import Board


class Node():
    def __init__(self, board, turn):
        self.board = board
        self.turn = turn #-1 or 1
        
        self.pos = list() #the move till this board
        self.parent = None #parent node
        self.depth = 0
        # self.checked = False

        self.value = 0 #best_value
        # self.max = sys.maxsize
        # self.min = -sys.maxsize
        return

def Black_Player(Game:game, Depth):
    pos = list()
    board = Board()
    board.set_board(Game.get_board().copy())
    
    valid_moves = board.valid_move_black()
    for move in valid_moves:
        for corner in [[0,0],[0,7],[7,0],[7,7]]:
            if move == corner:
                return move
    
    start_node = Node(board, -1)
    if Depth %2 ==0: Depth +=1

    queue = [start_node]
    min_value = (sys.maxsize,Node(board, -1))

    while(queue):
        current_node = queue.pop()
        if (check_endgame(current_node) and current_node.turn == -1) or (current_node.board.valid_move_black() == [] and current_node.turn == -1) or (current_node.board.valid_move_white() == [] and current_node.turn == 1):
            while True:
                if current_node.depth > 1:
                    current_node = current_node.parent
                elif current_node.depth == 1:
                    pos = current_node.pos
                    break
            return pos

        if current_node.depth < Depth: #odd number
            if current_node.turn == -1:#black
                for move in current_node.board.valid_move_black():
                    next_board = Board()
                    next_board.set_board(current_node.board.get_board().copy())
                    next_board.place_black(move)
                    next_node = Node(next_board, turn=1)
                    next_node.pos = move
                    next_node.parent = current_node
                    next_node.depth = current_node.depth + 1
                    queue.append(next_node)
                    
            elif current_node.turn == 1: #white
                for move in current_node.board.valid_move_white():
                    next_board = Board()
                    next_board.set_board(current_node.board.get_board().copy())
                    next_board.place_white(move)
                    next_node = Node(next_board, turn=-1)
                    next_node.pos = move
                    next_node.parent = current_node
                    next_node.depth = current_node.depth + 1
                    queue.append(next_node)

        else: #get value
            for move in current_node.board.valid_move_black():
                next_board = Board()
                next_board.set_board(current_node.board.get_board().copy())
                next_board.place_black(move)
                value = get_black_value(next_board.get_board().copy())

                if value < min_value[0]:
                    min_value = (value, current_node)
    
    #pick the best node
    choose_node = min_value[1]
    while True:
        if choose_node.depth > 1:
            choose_node = choose_node.parent
        elif choose_node.depth == 1:
            pos = choose_node.pos
            break

    return pos

def White_Player(Game:game, Depth):
    pos = list()
    board = Board()
    board.set_board(Game.get_board().copy())
    
    valid_moves = board.valid_move_white()
    for move in valid_moves:
        for corner in [[0,0],[0,7],[7,0],[7,7]]:
            if move == corner:
                return move
    
    start_node = Node(board, 1)
    if Depth %2 ==0: Depth +=1

    queue = [start_node]
    max_value = (-sys.maxsize,start_node)

    while(queue):
        current_node = queue.pop()
        if (check_endgame(current_node) and current_node.turn == 1) or (current_node.board.valid_move_black() == [] and current_node.turn == -1) or (current_node.board.valid_move_white() == [] and current_node.turn == 1):
            while True:
                if current_node.depth > 1:
                    current_node = current_node.parent
                elif current_node.depth == 1:
                    pos = current_node.pos
                    break
            return pos

        if current_node.depth < Depth: #odd number
            if current_node.turn == -1:#black
                for move in current_node.board.valid_move_black():
                    next_board = Board()
                    next_board.set_board(current_node.board.get_board().copy())
                    next_board.place_black(move)
                    next_node = Node(next_board, turn=1)
                    next_node.pos = move
                    next_node.parent = current_node
                    next_node.depth = current_node.depth + 1
                    queue.append(next_node)
                    
            elif current_node.turn == 1: #white
                for move in current_node.board.valid_move_white():
                    next_board = Board()
                    next_board.set_board(current_node.board.get_board().copy())
                    next_board.place_white(move)
                    next_node = Node(next_board, turn=-1)
                    next_node.pos = move
                    next_node.parent = current_node
                    next_node.depth = current_node.depth + 1
                    queue.append(next_node)

        else: #get value
            for move in current_node.board.valid_move_white():
                next_board = Board()
                next_board.set_board(current_node.board.get_board().copy())
                next_board.place_white(move)
                value = get_white_value(next_board.get_board().copy())

                if value > max_value[0]:
                    max_value = (value, current_node)
    
    #pick the best node
    choose_node = max_value[1]
    while True:
        if choose_node.depth > 1:
            choose_node = choose_node.parent
        elif choose_node.depth == 1:
            pos = choose_node.pos
            break

    return pos

def check_endgame(current_node:Node):
    EndGame = game()
    EndGame.set_board(current_node.board.get_board())
    EndGame.check_next_turn()
    return EndGame.end

def get_white_value(board):
    x = np.array(board).flatten()
    xixj = np.zeros(len(x)) #sum

    for i in range(len(x)):
        for j in range(len(x)):
            if i == j:
                continue
            else:
                xixj[i] += x[i]*x[j]
    xixj = xixj *1
    model = pickle.load(open("model/model_white.pickle","rb"))
    y = model.predict([xixj])
    return y

def get_black_value(board):
    x = np.array(board).flatten()
    xixj = np.zeros(len(x)) #sum

    for i in range(len(x)):
        for j in range(len(x)):
            if i == j:
                continue
            else:
                xixj[i] += x[i]*x[j]
    xixj = xixj *-1
    model = pickle.load(open("model/model_black.pickle","rb"))
    y = model.predict([xixj])
    return y

