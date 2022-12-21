from collections import deque
import sys
import numpy as np
from sklearn.neighbors import KNeighborsRegressor
import pickle
from othello.util.game import game
from .ML import *

depth = 5 #assign in game engine
class Node():
    def __init__(self, board):
        self.state = board
        self.max = sys.maxsize
        self.min = 0
        self.parent = None
        self.depth = 0
        return

def Minimax(match:game, max_turn=True): #depth of five

    if max_turn and depth%2 == 1:
        deep = depth -1
    elif max_turn and depth%2 == 0:
        deep = depth -1
    else:
        deep = depth -2

    node = Node(match.get_board()) #state, minH, maxH
    queue = deque()
    states_in_max_depth = deque() #node
    while len(queue):
        currentnode = queue.pop(0)
        for successor_state in get_next_states(currentnode.state, max_turn):
            successor = Node(successor_state)
            
            if successor_state.depth < deep:
                successor.depth += 1
                successor.parent = node
                queue.append(successor)
            else:
                states_in_max_depth.append(successor)

    best_state = states_in_max_depth[0]
    for node.state in states_in_max_depth:
        if node.state.H > best_state.H:
            best_state = node

    while best_state.depth != 0:
        best_state = best_state.parent

    return best_state.state

def get_value(board): #get hamilitonium
    x = np.array(board).flatten()
    model = pickle.load(open("model/model.pickle","rb"))
    y = model.predict(x)
    return y

def get_next_states(state, max_turn=True):#vailded moves to play
    return
