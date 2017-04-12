import sys, time, random, copyfrom settings import *

# This handles the actual game aspect of checkers.
class GameState:
    def __init__(self, rows, cols):
        self.__rows  = rows         # number of rows in the board
        self.__cols = cols          # number of columns in the board
        self.__pieces = [0]*cols    # __pieces[c] = number of pieces in a column c
        self.__player = 0           # the current player to move, 0 = Player One, 1 = Player Two
        self.__board   = [[PLAYER_NONE]*cols for r in range(rows)]
        print("GameState init completed")

    # These are getter functions used to get private variables such as self.__rows.
    def get(self, r, c):        return self.__board[r][c]   # piece type located at (r,c)
    def cols(self):             return self.__cols          # number of columns in board
    def rows(self):             return self.__rows          # number of rows in board
