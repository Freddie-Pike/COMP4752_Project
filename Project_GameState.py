import sys, time, random, copy
from settings import *

# This handles the actual game aspect of checkers.
class GameState:
    def __init__(self, rows, cols):
        self.__rows  = rows         # number of rows in the board
        self.__cols = cols          # number of columns in the board
        self.__pieces = [0]*cols    # __pieces[c] = number of pieces in a column c
        self.__player = 0           # the current player to move, 0 = Player One, 1 = Player Two
        self.__board   = [[PLAYER_NONE]*cols for r in range(rows)]

        # Initializes all the variables that help with putting and moving pieces.
        self.selected_piece = (-1, -1) # Used for highlighting potential moves.
        self.red_piece_list =  [(0,1), (0,3), (0,5), (0,7), (1,0), (1,2), (1,4), (1,6), (2,1), (2,3), (2,5), (2,7) ] # All red pieces at bottom. # STARTING_RED_POSITIONS
        print("rpl ----- ", self.red_piece_list)
        self.black_piece_list = [ (7,0), (7,2), (7,4), (7,6), (6,1), (6,3), (6,5), (6,7), (5,0), (5,2), (5,4), (5,6) ] # All black pieces at top. # STARTING_BLACK_POSITIONS
        self.red_piece_potential_move_list = [] # No potential red moves at init.
        self.black_piece_potential_move_list = [] # No potential black moves at init.
        print("GameState init completed")

    # These are getter functions used to get private variables such as self.__rows.
    def get(self, r, c):        return self.__board[r][c]   # piece type located at (r,c)
    def cols(self):             return self.__cols          # number of columns in board
    def rows(self):             return self.__rows          # number of rows in board
    def player_to_move(self):   return self.__player        # the player to move next
    def opponent(self, player): return (player + 1) % 2 # return the opponent's value
    

    # Check if a move is legal.
    def is_legal(self, move):
        # If the move is on tile with a red piece, then it's not legal.
        if move in self.red_piece_list:
            print("move is in red piece list")
            return False

        # If the move is on tile with a black piece, then it's not legal.
        if move in self.black_piece_list:
            print("move is in black piece list")
            return False

        # Check if the row position is within bounds.
        if (move[0] < 0 or move[0] >= BOARD_ROWS):
            print("row location is out of bounds")
            return False

        # Check if the column position is within bounds.
        if (move[1] < 0 or move[1] >= BOARD_COLS):
            print("column location is out of bounds")
            return False

        # Previously checks were false so tile must be legal.
        return True

    # This will execute a move when passed a new row/column location.
    def do_move(self, new_pos):
        # If the move is illegal, then return.
        if not self.is_legal(new_pos):
            print("DOING ILLEGAL MOVE")
            return

        print("do_move player is ", self.__player)

        # If the player is red then execute his move.
        if (self.__player == 0):
            print("red piece list is ", self.red_piece_list)
            piece_index = self.red_piece_list.index(self.selected_piece)
            print("index is ", piece_index)
            self.red_piece_list[piece_index] = new_pos
            self.red_piece_potential_move_list = []

        # If the player is black then execute his move.
        if (self.__player == 1):
            piece_index = self.black_piece_list.index(self.selected_piece)
            print("index is ", piece_index)
            self.black_piece_list[piece_index] = new_pos
            self.black_piece_potential_move_list = []

        # Swap players so the next player gets the turn.
        self.__player = self.opponent(self.__player)


    # When a player selects a piece, this function will highlight all the potential moves around it.
    def highlight_potential_moves(self, tile):
        # We don't don't want multiple red/black potential pieces on board, so reinitialize.
        self.red_piece_potential_move_list = [] 
        self.black_piece_potential_move_list = []

        print("highlight_pm player is ", self.__player)

        # Grab potential_moves depending on the player.
        if (self.__player == 0):
            # If the tile pressed isn't red, then return.
            if tile not in self.red_piece_list:
                return

            self.selected_piece = tile # Used to possibly move to this postion later.

            # Loop through all legal red actions to add them as potential moves.
            for action in LEGAL_RED_ACTIONS:
                # The new postion of the piece.
                new_row = tile[0] + action[0]
                new_col = tile[1] + action[1]
                temp_piece = (new_row, new_col)
                self.red_piece_potential_move_list.append(temp_piece)

        if (self.__player == 1):
            # If the tile pressed isn't black, then return.
            if tile not in self.black_piece_list:
                return

            self.selected_piece = tile # Used to possibly move to this postion later.
            
            # Loop through all legal black actions to add them as potential moves.
            for action in LEGAL_BLACK_ACTIONS:
                # The new postion of the piece.
                new_row = tile[0] + action[0]
                new_col = tile[1] + action[1]
                temp_piece = (new_row, new_col)
                self.black_piece_potential_move_list.append(temp_piece)
