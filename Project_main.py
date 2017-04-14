import sys
import pygame as pg
from settings import *

# What each module does
# sys - This will set the recursion limit so that algorithms won't run on forever.
# settings - This will import the settings file in the current directory.

# Importing the GameState which will be used purely as the GUI for the application. As it
# As it stands right now, we draw the GUI information from a mix of this file and
# the GameState. In the next update the DisplayState will have more of that responsibility.
from Project_GameState import GameState as DisplayState

# The basic Checkers class.
class Checkers:
    # The init function where we initalize important information about pygame and checkers.
    def __init__(self):
        pg.init() # This initializes pygame, must be done.
        pg.display.set_caption(TITLE) # Sets title of the window as defined in settings.
        self.clock = pg.time.Clock() # Used to set the FPS.

        # This is the gamestate method which contains information about the board, later
        # on this will contain information about the AI.
        self.display_state = DisplayState(BOARD_ROWS, BOARD_COLS) 
        self.width  = self.display_state.cols() * TILESIZE # Width of screen.
        self.height = self.display_state.rows() * TILESIZE + 40 # Height of screen.
        self.screen = pg.display.set_mode( (self.width, self.height) ) # Window Size.
        self.screen.fill(BLACK) # Fill the Background black.
        self.flip_color = True # Used to switch background colors when drawing the board.

        # For now player one is a String, in future we'll be using the settings
        # file variables to set which player is which.
        self.player_one = "RED" 

        # Initializes all the variables that help with putting and moving pieces.
        self.selected_piece = (-1, -1) # Used for highlighting potential moves.
        self.red_piece_list = STARTING_RED_POSITIONS # All red pieces at bottom.
        self.black_piece_list = STARTING_BLACK_POSITIONS # All black pieces at top.
        self.red_piece_potential_move_list = [] # No potential red moves at init.
        self.black_piece_potential_move_list = [] # No potential black moves at init.

        # display_state will later be used for doing turns and implementing AI.
        # self.display_state = DisplayState(BOARD_ROWS, BOARD_COLS)

    # The main game update loop of the application
    def update(self):
        # This sets a limit on how fast our computers process the drawing code.
        self.dt = self.clock.tick(FPS) / 1000
        self.events() # This will check for any input.
        self.draw() # Draw everything on the screen.

    # This will draw everything on the screen.
    def draw(self):
        self.draw_board() # Draw the basic checkerboard for the background.
        self.draw_piece_list(self.screen, self.red_piece_list, RED, 2) # Draw all the red pieces.
        self.draw_piece_list(self.screen, self.black_piece_list, BLACK, 2) # Draw all the black pieces.

        # If a player has pressed down on a piece then highlight potential moves.
        self.draw_piece_list(self.screen, self.red_piece_potential_move_list, WHITE, 2) # Draw all potential red moves on board.
        self.draw_piece_list(self.screen, self.black_piece_potential_move_list, WHITE, 2) # Draw all potential red moves on board.
        pg.display.flip() # Paint the graphics to the screen.

    # This will draw the checkered background of the checkers screen.
    def draw_board(self):
        # This must always be reinitialized or else colors will constantly be flashing.
        self.flip_color = True
        
        # Draw all the tiles on the screen.
        # NOTE: We don't use drawrect to create a rectangle but we instead fill the part
        # of the screen(like paintbucket in MS Paint/Photoshop) to fill in the checkerboard
        # design.
        for c in range(self.display_state.cols()):
            for r in range(self.display_state.rows()):
                # Draw a colored tile on the screen depending on flip_color value.
                if (self.flip_color == True):
                    self.screen.fill(BG_COLOR_1, (c*TILESIZE, r*TILESIZE, TILESIZE*1, TILESIZE*1))
                    self.flip_color = False # Draw the next tile a different color.
                else:
                    self.screen.fill(BG_COLOR_2, (c*TILESIZE, r*TILESIZE, TILESIZE*1, TILESIZE*1))
                    self.flip_color = True # Draw the next tile a different color.

            # Flip the color again so the next column starts with a different color.
            self.flip_color = not self.flip_color 

    # This will draw a list of pieces on a board using a list of tuples.
    def draw_piece_list(self, surface, piece_list, color, border):
        # For every piece in given list, draw a piece at that row and column.
        for piece in piece_list:
            row, col = self.display_state.rows() - 1 - piece[0], piece[1]
            pg.draw.circle(surface, color, (col*TILESIZE+TILESIZE//2, row*TILESIZE+TILESIZE//2), TILESIZE//2-PIECEPAD)

    # When a player selects a piece, this function will highlight all the potential moves around it.
    def highlight_potential_moves(self, player, tile):
        # We don't don't want multiple red/black potential pieces on board, so reinitialize.
        self.red_piece_potential_move_list = [] 
        self.black_piece_potential_move_list = []

        # Grab potential_moves depending on the player.
        if (player == "RED"):
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

        if (player == "BLACK"):
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

    # This will do a basic move when passed an action and an index.
    # NOTE - This is mainly used for debugging for moving pieces.
    def do_move_by_index(self, tile_list, index, action):
        # Get the new postion of the piece.
        temp_piece = tile_list[index]
        new_row = temp_piece[0] + action[0]
        new_col = temp_piece[1] + action[1]
        temp_piece = (new_row, new_col)        
        print("temp_piece location is ", temp_piece)
        
        # If the move is illegal, then return.
        if not self.is_legal(temp_piece):
            print("DOING ILLEGAL MOVE")
            return
        
        tile_list[index] = temp_piece # The position is now updated.

    # This will execute a move when passed a new row/column location.
    def do_move(self, player, new_pos):
        # If the move is illegal, then close the program.
        if not self.is_legal(new_pos):
            print("DOING ILLEGAL MOVE")
            return

        # If the player is red then execute his move.
        if (player == "RED"):
            piece_index = self.red_piece_list.index(self.selected_piece)
            print("index is ", piece_index)
            self.red_piece_list[piece_index] = new_pos
            self.red_piece_potential_move_list = []

        # If the player is black then execute his move.
        if (player == "BLACK"):
            piece_index = self.black_piece_list.index(self.selected_piece)
            print("index is ", piece_index)
            self.black_piece_list[piece_index] = new_pos
            self.black_piece_potential_move_list = []

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
            
    # Returns the tile (r,c) on the grid underneath a given mouse position in pixels
    def get_tile(self, mpos):
        return (mpos[1] // TILESIZE, mpos[0] // TILESIZE)

    # This function will handle all user input handling.
    def events(self):
        # Loop through every event occuring.
        for event in pg.event.get():
            # If user hit the X button on window, then quit.
            if event.type == pg.QUIT:
                pg.quit()
                quit()
                
            # Check if a key is pressed down.
            if event.type == pg.KEYDOWN:
                # ALL DEBUGGING STUFF.
                # If left key pressed, move a black piece.
                if event.key == pg.K_LEFT:
                    self.do_move_by_index(self.black_piece_list, 9, LEGAL_BLACK_ACTIONS[1])

                # If left key pressed, move a red piece.
                if event.key == pg.K_RIGHT:
                    self.do_move_by_index(self.red_piece_list, 9, LEGAL_RED_ACTIONS[1])

                # If D is pressed down, print debuging information
                if event.key == pg.K_d:
                    print("Debugging is cool")

            # Check if a mousebutton is pressed down.
            if event.type == pg.MOUSEBUTTONDOWN:
                if pg.mouse.get_pressed()[0]:
                    move = self.get_tile(event.pos)
                    repositioned_row = move[0] - (BOARD_ROWS - 1)
                    move = (abs(repositioned_row), move[1])
                    print("Move pressed is ", move)

                    # If the player is RED, then check for potential moves.
                    if (self.player_one == "RED"):
                        # If player clicked on a potential move then go to that postion.
                        if move in self.red_piece_potential_move_list:
                            self.do_move(self.player_one, move)
                            continue

                        # If player didn't click on potential move then show them instead.
                        self.highlight_potential_moves(self.player_one, move)

                    if (self.player_one == "BLACK"):
                        # If player clicked on a potential move then go to that postion.
                        if move in self.black_piece_potential_move_list:
                            self.do_move(self.player_one, move)
                            continue
                
                        # If player didn't click on potential move then show them instead.
                        self.highlight_potential_moves(self.player_one, move)
        
# This is the main executable part of the program.
sys.setrecursionlimit(10000) # Can't go past 10000 recursive depth.

# This is the basic game object
game_object = Checkers()

# This is the "game loop" of the program, it is an infinite loop that runs the game.
while True:
    game_object.update()
                
