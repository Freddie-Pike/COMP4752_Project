import sys, time, random, copy
from settings import *

# This handles the actual game aspect of checkers.
class GameState:
    def __init__(self, rows, cols):
        self.__rows  = rows         # number of rows in the board
        self.__cols = cols          # number of columns in the board
        self.__pieces = [0]*cols    # __pieces[c] = number of pieces in a column c
        self.__player = 1           # the current player to move, 0 = Player One, 1 = Player Two
        self.__board   = [[PLAYER_NONE]*cols for r in range(rows)]

        # Initializes all the variables that help with putting and moving pieces.
        self.selected_piece = (-1, -1) # Used for highlighting potential moves.
        self.red_piece_list = copy.deepcopy(BLACK_CAN_BECOME_KING_R) # All red pieces at bottom. # STARTING_RED_POSITIONS
        self.black_piece_list = copy.deepcopy(BLACK_CAN_BECOME_KING_B) # All black pieces at top. # STARTING_BLACK_POSITIONS

        # List of all kings on the board
        self.red_king_piece_list = [] # copy.deepcopy(RED_CAN_BECOME_KING_KING_LIST_R)
        self.black_king_piece_list = [] # copy.deepcopy(BLACK_CAN_BECOME_KING_KING_LIST_B)
        
        self.red_piece_potential_move_list = [] # No potential red moves at init.
        self.black_piece_potential_move_list = [] # No potential black moves at init.
        self.black_pieces_to_remove_list = [] # Used to remove black pieces when a red piece does a jump.
        self.red_pieces_to_remove_list = [] # Used to remove red pieces when a black piece does a jump
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
        print("do_move ------------------------------------")
        # If the move is illegal, then return.
        if not self.is_legal(new_pos):
            print("DOING ILLEGAL MOVE")
            return

        # Used to determine the action direction the move took.
        action_taken = ( new_pos[0] - self.selected_piece[0],
                         new_pos[1] - self.selected_piece[1])

        # If positive row action, action_direction_row is 1.
        if action_taken[0] < 0:
            action_direction_row = -1
        else:
            action_direction_row = 1

        # If positive column action, action_direction_col is 1.
        if action_taken[1] < 0:
            action_direction_col = -1
        else:
            action_direction_col = 1

        # Used to remove a black piece off a board after a jump.
        action_direction = (action_direction_row, action_direction_col)
        
        print("action_taken is ", action_taken)
        # print("do_move player is ", self.__player)

        # If the player is red then execute his move.
        if (self.__player == 0):
            # If a jump was executed, removed all elements jumped.
            for piece in self.black_pieces_to_remove_list:
                print("piece[0] value is", piece[0])
                print("piece[1] value is", piece[1])
                # If the piece's action to get there is the same as we used to get here
                # then remove it.
                if piece[1] == action_direction:
                    self.black_piece_list.remove(piece[0]) # Remove from board.
                
            self.black_pieces_to_remove_list = [] # Reinitialize list.
                
            # print("red piece list is ", self.red_piece_list)
            piece_index = self.red_piece_list.index(self.selected_piece)

            # If piece is a king, must update it's location in red_king_piece_list.
            if self.red_piece_list[piece_index] in self.red_king_piece_list:
                print("A king was moved, update neccessary")
                king_piece_index = self.red_king_piece_list.index(self.selected_piece)
                self.red_king_piece_list[king_piece_index] = new_pos

            # If piece is about to become a king, then add it to the list.
            if new_pos in RED_CAN_BECOME_KING:
                print("--- KING ME")
                # We don't want duplicates.
                if new_pos not in self.red_king_piece_list:
                    self.red_king_piece_list.append(new_pos)
                    print("new king")
            print("red king list is ", self.red_king_piece_list)
                
            self.red_piece_list[piece_index] = new_pos
            self.red_piece_potential_move_list = []

        # If the player is black then execute his move.
        if (self.__player == 1):
            # If a jump was executed, removed all elements jumped.
            for piece in self.red_pieces_to_remove_list:
                print("piece[0] value is", piece[0])
                print("piece[1] value is", piece[1])
                # If the piece's action to get there is the same as we used to get here
                # then remove it.
                if piece[1] == action_direction:
                    self.red_piece_list.remove(piece[0]) # Remove from board.
                
            self.red_pieces_to_remove_list = [] # Reinitialize list.
            
            piece_index = self.black_piece_list.index(self.selected_piece)

            # If piece is a king, must update it's location in red_king_piece_list.
            if self.black_piece_list[piece_index] in self.black_king_piece_list:
                print("A king was moved, update neccessary")
                king_piece_index = self.black_king_piece_list.index(self.selected_piece)
                self.black_king_piece_list[king_piece_index] = new_pos

            # If piece is about to become a king, then add it to the list.
            if new_pos in BLACK_CAN_BECOME_KING:
                print("--- KING ME")
                # We don't want duplicates.
                if new_pos not in self.black_king_piece_list:
                    self.black_king_piece_list.append(new_pos)
                    print("new king")
            print("red king list is ", self.red_king_piece_list)
            
            self.black_piece_list[piece_index] = new_pos
            self.black_piece_potential_move_list = []

        # Swap players so the next player gets the turn.
        self.__player = self.opponent(self.__player)

    
    # When a player selects a piece, this function will highlight all the potential moves around it.
    def highlight_potential_moves(self, tile):
        # We don't don't want multiple red/black potential pieces on board, so reinitialize.
        print("---------------------------------------- HIGHLIGHT")
        self.red_piece_potential_move_list = [] 
        self.black_piece_potential_move_list = []
        self.red_pieces_to_remove_list = []
        self.black_pieces_to_remove_list = []

        print("highlight_pm player is ", self.__player)

        # Grab potential_moves depending on the player.
        # Red piece player
        if (self.__player == 0):
            # If the tile pressed isn't red, then return.
            if tile not in self.red_piece_list:
                print("Didn't click on red tile")
                return

            self.selected_piece = tile # Used to possibly move to this postion later.

        
            # Grab all legal actions and put it in the legal action list.
            action_list = []

            # If the tile is a king then grab all king actions, if not then grab usual red piece actions.
            if tile in self.red_king_piece_list:
                for action in LEGAL_KING_ACTIONS:
                    action_list.append(action)
            else:
                for action in LEGAL_RED_ACTIONS:
                    action_list.append(action)

            # Loop through all legal red actions to add them as potential moves.
            for action in action_list:
                print("-------- action")
                # The new postion of the piece.
                print("tile is ", tile)
                print("action is ", action)
                new_row = tile[0] + action[0]
                new_col = tile[1] + action[1]
                temp_piece = (new_row, new_col)
                print("temp_piece is ", temp_piece)

                # new_action = (action[0] * 2, action[1] * 2)

                # If the temp location is on a black piece, check if jump exists.
                if temp_piece in self.black_piece_list:
                    
                    # The possible jump column will change depending on the action taken.
                    # possible jump row will remain the same.
                    possible_jump_row = temp_piece[0] + action[0]
                    possible_jump_col = temp_piece[1] + action[1]

                    
                    # Where we'll be jumping to if the spot is legal.
                    possible_jump = (possible_jump_row, possible_jump_col)
                    print("possible jump is ", possible_jump)
                    if self.is_legal(possible_jump):
                        
                        print("jump is legal")
                        # It's now a potential move
                        self.red_piece_potential_move_list.append(possible_jump)
                        
                        # We remove the jumped piece by using this list.
                        self.black_pieces_to_remove_list.append( (temp_piece, action))

                        # Add new potential jumps to list.
                        # new_action_1 = (action[0] * 3, action[1] * 3)
                        # new_action_2 = (action[0] * 3, action[1])
                        # action_list.append(new_action_1)
                        # action_list.append(new_action_2)
                    continue
                else:
                    # The temp_piece is now added to list.
                    self.red_piece_potential_move_list.append(temp_piece)

        # Black piece player
        if (self.__player == 1):
            # If the tile pressed isn't black, then return.
            if tile not in self.black_piece_list:
                return

            self.selected_piece = tile # Used to possibly move to this postion later.

            # Grab all legal actions and put it in the legal action list.
            action_list = []

            # If the tile is a king then grab all king actions, if not then grab usual red piece actions.
            if tile in self.black_king_piece_list:
                for action in LEGAL_KING_ACTIONS:
                    action_list.append(action)
            else:
                for action in LEGAL_BLACK_ACTIONS:
                    action_list.append(action)
            
            # Loop through all legal black actions to add them as potential moves.
            for action in action_list:
                # The new postion of the piece.
                print("tile is ", tile)
                print("action is ", action)
                new_row = tile[0] + action[0]
                new_col = tile[1] + action[1]
                temp_piece = (new_row, new_col)
                print("temp_piece is ", temp_piece)
                new_action = (action[0] + action[0], action[1] + action[1])
                print("new_action is ", new_action)

                # If the temp location is on a black piece, check if jump exists.
                if temp_piece in self.red_piece_list:
                    # The possible jump column will change depending on the action taken.
                    # possible jump row will remain the same.
                    possible_jump_row = temp_piece[0] + action[0]
                    possible_jump_col = temp_piece[1] + action[1]

                    # Where we'll be jumping to if the spot is legal.
                    possible_jump = (possible_jump_row, possible_jump_col)
                    print("possible jump is ", possible_jump)
                    if self.is_legal(possible_jump):
                        print("jump is legal")
                        # It's now a potential move
                        self.black_piece_potential_move_list.append(possible_jump)

                        # We remove the jumped piece by using this list.
                        self.red_pieces_to_remove_list.append( (temp_piece, action))
                    continue
                else:
                    # The temp_piece is now added to list.
                    self.black_piece_potential_move_list.append(temp_piece)

        # This will later be used to determine the winner. Should contain something like
        # black_piece_list.length == 0, the red player winner and vice versa.
        def winner(self):
            print("A winner is you!")

        # The Heuristic will be put in this function.
        def eval(self, player):
            print("Heuristic calculated")

# This will later will be used to implement alphabeta.
class Player_AlphaBeta:
    def __init__(self):
        print("init")
