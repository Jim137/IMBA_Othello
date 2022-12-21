'''
The game class is used to represent the game process of othello.
'''
import numpy as np
from .board import Board


class game(Board):
    '''
    The game class is used to represent the game of othello.

    The game class inherits the board class.
    '''

    def __init__(self):
        '''
        The constructor of the game class.

        By default: game properties include:
            - board: a 8x8 numpy array.
                - 1 for white.
                - -1 for black.
                - 0 for empty.
            - turn: -1 for black and 1 for white.
            - end: False for not ended and True for ended.

        '''
        super().__init__()
        self._turn = -1
        self.end = False

    @property
    def turn(self):
        return self._turn

    @turn.setter
    def turn(self, turn):
        self._turn = turn

    def check_next_turn(self):
        '''Checks the next turn and whether the game is end.'''
        if self.valid_move_black() == [] and self.valid_move_white() == []:
            self.end = True
            return
        elif self.turn == -1 and self.valid_move_white() == []:
            return
        elif self.turn == 1 and self.valid_move_black() == []:
            return
        else:
            self.turn *= -1
            return

    def to_place(self, pos):
        '''Places a piece at a given valid position.'''
        pos = self.valid_pos_list(pos)
        if (pos == False):
            return False
        if self.turn == -1:
            valid = self.valid_move_black()
            if (pos in valid):
                self.place_black(pos)
                self.check_next_turn()
                return True
            else:
                return False
        elif self.turn == 1:
            valid = self.valid_move_white()
            if (pos in valid):
                self.place_white(pos)
                self.check_next_turn()
                return True
            else:
                return False

    def count_black(self):
        '''Returns the number of black pieces.'''
        return np.count_nonzero(self.get_board() == -1)

    def count_white(self):
        '''Returns the number of white pieces.'''
        return np.count_nonzero(self.get_board() == 1)

    def get_lead(self):
        '''Returns side of the lead.'''
        if self.count_black() > self.count_white():
            return -1
        elif self.count_black() < self.count_white():
            return 1
        else:
            return 0 

    def winner(self):
        '''Returns the winner.'''
        if self.end == True:
            if self.count_black() > self.count_white():
                return 'Black'
            elif self.count_black() < self.count_white():
                return 'White'
            else:
                return 'Draw'
        else:
            return False
