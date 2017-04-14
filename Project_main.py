import sys
import pygame as pg
from settings import *

# What each module does
# sys - This will set the recursion limit so that algorithms won't run on forever.
# settings - This will import the settings file in the current directory.

# Importing the GameState which will be used purely as the GUI for the application. As it
# As it stands right now, we draw the GUI information from a mix of this file and
# the GameState
from Project_GameState import GameState as DisplayState

# The basic Checkers class.
class Checkers:
    # The init function where we initalize important information about pygame.
    def __init__(self):
        pg.init() # This initializes pygame, must be done.
        pg.display.set_caption(TITLE) # Sets title of the window as defined in settings.

        # This is the gamestate method which contains information about the board, later
        # on this will contain information about the AI.
        self.display_state = DisplayState(BOARD_ROWS, BOARD_COLS) 
        self.width  = self.display_state.cols() * TILESIZE # Width of screen.
        self.height = self.display_state.rows() * TILESIZE + 40 # Height of screen.

        self.flip_color = True # Used to switch colors when drawing the board.

        # Initializes all the red and black pieces to there starting positions.
        self.red_piece_list = STARTING_RED_POSITIONS
        self.black_piece_list = STARTING_BLACK_POSITIONS

        # This initializes the size of the screen.
        self.screen = pg.display.set_mode( (self.width, self.height) ) 
        # self.display_state = DisplayState(BOARD_ROWS, BOARD_COLS)

    # The main game loop of the application
    def update(self):
        self.draw()

    # This will draw everything on the screen.
    def draw(self):
        self.draw_board() # Draw the basic checkerboard for the background.
        self.draw_piece_list(self.screen, self.red_piece_list, RED, 2) # Draw all the red pieces.
        self.draw_piece_list(self.screen, self.black_piece_list, BLACK, 2) # Draw all the black pieces.
        pg.display.flip() # Paint the graphics to the screen.

    # This will just draw the checkered background of the checkers screen.
    def draw_board(self):
        self.screen.fill(BLACK) # Fill the Background black.

        # This must always be reinitialized or else colors will constantly be flashing.
        self.flip_color = True
        
        # Draw all the tiles on the screen.
        # NOTE: We don't use drawrect to create a rectangle but we instead fill part
        # of the screen(like paintbucket in MS Paint/Photoshop) to fill in the checkerboard
        # desgin.
        for c in range(self.display_state.cols()):
            for r in range(self.display_state.rows()):
                if (self.flip_color == True):
                    self.screen.fill(BROWN, (c*TILESIZE, r*TILESIZE, TILESIZE*1, TILESIZE*1))
                    self.flip_color = False # Draw the next tile a different color.
                else:
                    self.screen.fill(CORNSILK, (c*TILESIZE, r*TILESIZE, TILESIZE*1, TILESIZE*1))
                    self.flip_color = True # Draw the next tile a different color.

            # Flip the color again so the next column starts with a different color.
            self.flip_color = not self.flip_color 

    # This will draw a list of pieces on a board using a list of tuples.
    def draw_piece_list(self, surface, tile_list, color, border):
        for tile in tile_list:
            row, col = self.display_state.rows() - 1 - tile[0], tile[1]
            pg.draw.circle(self.screen, color, (col*TILESIZE+TILESIZE//2, row*TILESIZE+TILESIZE//2), TILESIZE//2-PIECEPAD)

    # This will do a basic move when passed an action.
    def do_move(self, tile_list, index, action):
        temp_piece = tile_list[index]

        # The new postion of the piece.
        new_row = temp_piece[0] + action[0]
        new_col = temp_piece[1] + action[1]
        temp_piece = (new_row, new_col)
        tile_list[index] = temp_piece # The position is now updated.

# This is the main executable part of the program.
sys.setrecursionlimit(10000) # Can't go past 10000 recursive depth.

# This is the basic game object
game_object = Checkers()
game_loop = True

# This is the "game loop" of the program, it is an infinite loop that runs the game.
while game_loop:
    game_object.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_loop = False
        # Check if a key is pressed down.
        if event.type == pg.KEYDOWN:
            # If left key pressed, move a black piece.
            if event.key == pg.K_LEFT:
                game_object.do_move(game_object.black_piece_list, 9, LEGAL_BLACK_ACTIONS[1])

            # If left key pressed, move a red piece.
            if event.key == pg.K_RIGHT:
                game_object.do_move(game_object.red_piece_list, 9, LEGAL_RED_ACTIONS[1])
                
pg.quit()
quit()
