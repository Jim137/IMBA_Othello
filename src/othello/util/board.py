'''
Board class for the game.
'''
import numpy as np
from .dict import pos_sheet, row_inverse_sheet, col_inverse_sheet


class Board(object):
    '''The board class is used to represent the board of the game.'''

    def __init__(self):
        '''
        The constructor of the board class.

        By default: board properties include:
            - board: a 8x8 numpy array.
                - 1 for white.
                - -1 for black.
                - 0 for empty.
        '''
        self._board = np.zeros((8, 8), dtype=int)
        self._board[3, 3] = 1
        self._board[4, 4] = 1
        self._board[3, 4] = -1
        self._board[4, 3] = -1

    @staticmethod
    def valid_pos_list(pos):
        if (type(pos) == list):
            pass
        elif (type(pos) == str):
            if (len(pos) != 2):
                return False
            if (pos[0] not in pos_sheet or pos[1] not in pos_sheet):
                return False
            pos = [pos_sheet[pos[0]], pos_sheet[pos[1]]]
        else:
            return False
        return pos

    @staticmethod
    def pos_name(pos):
        '''Returns a list of postion names in the form of strings.'''
        name = []
        for p in pos:
            name.append(
                row_inverse_sheet[p[0]] + col_inverse_sheet[p[1]])
        return name

    def get_board(self):
        '''Returns the board.'''
        return self._board

    def set_board(self, board):
        '''Sets the board.'''
        for i, j in np.ndindex(board.shape):
            self._board[i, j] = board[i, j]

    def __getpiece__(self, pos):
        '''Returns the color piece at a given position.'''
        return self._board[pos[0], pos[1]]

    def __setpiece__(self, pos, color):
        '''
        Sets the piece at a given position.
        '''
        self._board[pos[0], pos[1]] = color

    def _check_valid_move_white(self, i, j):
        '''Checks if a move is valid for white.'''
        if (self.__getpiece__([i, j]) != 0):
            return False
        for m in [-1, 0, 1]:
            for n in [-1, 0, 1]:
                if (m == 0 and n == 0):
                    continue
                if (i+m < 0 or i+m > 7 or j+n < 0 or j+n > 7):
                    continue
                if (self.__getpiece__([i+m, j+n]) == -1):
                    for k in range(2, 8):
                        if (i+k*m < 0 or i+k*m > 7 or j+k*n < 0 or j+k*n > 7):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == 0):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == 1):
                            return True
        return False

    def valid_move_white(self):
        '''Returns a list of valid moves for white.'''
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if (self._check_valid_move_white(i, j)):
                    valid_moves.append([i, j])
        return valid_moves

    def _check_valid_move_black(self, i, j):
        '''Checks if a move is valid for black.'''
        if (self.__getpiece__([i, j]) != 0):
            return False
        for m in [-1, 0, 1]:
            for n in [-1, 0, 1]:
                if (m == 0 and n == 0):
                    continue
                if (i+m < 0 or i+m > 7 or j+n < 0 or j+n > 7):
                    continue
                if (self.__getpiece__([i+m, j+n]) == 1):
                    for k in range(2, 8):
                        if (i+k*m < 0 or i+k*m > 7 or j+k*n < 0 or j+k*n > 7):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == 0):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == -1):
                            return True
        return False

    def valid_move_black(self):
        '''Returns a list of valid moves for black.'''
        valid_moves = []
        for i in range(8):
            for j in range(8):
                if (self._check_valid_move_black(i, j)):
                    valid_moves.append([i, j])
        return valid_moves

    def _flip_white(self, i, j):
        '''Flips the pieces for white.'''
        for m in [-1, 0, 1]:
            for n in [-1, 0, 1]:
                if (m == 0 and n == 0):
                    continue
                if (i+m < 0 or i+m > 7 or j+n < 0 or j+n > 7):
                    continue
                if (self._board[i+m, j+n] == -1):
                    for k in range(2, 8):
                        if (i+k*m < 0 or i+k*m > 7 or j+k*n < 0 or j+k*n > 7):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == 0):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == 1):
                            for l in range(1, k):
                                self.__setpiece__([i+l*m, j+l*n], 1)
                            break

    def place_white(self, pos):
        '''Places a white piece on the board.'''
        self.__setpiece__([pos[0], pos[1]], 1)
        self._flip_white(pos[0], pos[1])

    def _flip_black(self, i, j):
        '''Flips the pieces for black.'''
        for m in [-1, 0, 1]:
            for n in [-1, 0, 1]:
                if (m == 0 and n == 0):
                    continue
                if (i+m < 0 or i+m > 7 or j+n < 0 or j+n > 7):
                    continue
                if (self._board[i+m, j+n] == 1):
                    for k in range(2, 8):
                        if (i+k*m < 0 or i+k*m > 7 or j+k*n < 0 or j+k*n > 7):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == 0):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == -1):
                            for l in range(1, k):
                                self.__setpiece__([i+l*m, j+l*n], -1)
                            break

    def place_black(self, pos):
        '''Places a black piece on the board.'''
        self.__setpiece__([pos[0], pos[1]], -1)
        self._flip_black(pos[0], pos[1])

    def pseudo_flip_white(self, pos: list):
        '''
        Counting how many flips can make for white.

        Returns a list of positions that would be flipped.
        '''
        i = pos[0]
        j = pos[1]
        can_place = []
        for m in [-1, 0, 1]:
            for n in [-1, 0, 1]:
                if (m == 0 and n == 0):
                    continue
                if (i+m < 0 or i+m > 7 or j+n < 0 or j+n > 7):
                    continue
                if (self._board[i+m, j+n] == -1):
                    for k in range(2, 8):
                        if (i+k*m < 0 or i+k*m > 7 or j+k*n < 0 or j+k*n > 7):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == 0):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == 1):
                            for l in range(1, k):
                                can_place.append([i+l*m, j+l*n])
                            break
        return can_place

    def pseudo_flip_black(self, pos):
        '''
        Counting how many flips can make for black.

        Returns a list of positions that would be flipped.
        '''
        i = pos[0]
        j = pos[1]
        can_place = []
        for m in [-1, 0, 1]:
            for n in [-1, 0, 1]:
                if (m == 0 and n == 0):
                    continue
                if (i+m < 0 or i+m > 7 or j+n < 0 or j+n > 7):
                    continue
                if (self._board[i+m, j+n] == 1):
                    for k in range(2, 8):
                        if (i+k*m < 0 or i+k*m > 7 or j+k*n < 0 or j+k*n > 7):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == 0):
                            break
                        if (self.__getpiece__([i+k*m, j+k*n]) == -1):
                            for l in range(1, k):
                                can_place.append([i+l*m, j+l*n])
                            break
        return can_place

    def print_board(self):
        '''Prints the board.'''
        labelsx = ['1', '2', '3', '4', '5', '6', '7', '8']
        labelsy = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']

        print('  ', end='')
        for i in range(8):
            print(labelsx[i], end=' ')
        print()
        for i in range(8):
            print(labelsy[i], end=' ')
            for j in range(8):
                if (self.__getpiece__([i, j]) == -1):
                    print('○', end=' ')
                elif (self.__getpiece__([i, j]) == 1):
                    print('●', end=' ')
                else:
                    print('.', end=' ')
            print()
        print()

    def __repr__(self):
        return self.print_board()
