import sys
import pygame as pg
from settings import *

# What each module does
# sys - This will set the recursion limit so that algorithms won't run on forever.
# settings - This will import the settings file in the current directory

# Importing the GameState to use purely as the GUI for the application.
from Project_GameState import GameState as DisplayState

# The basic Checkers class, will be ran 
class Checkers:
    # The init function where we do the following:
    # pg.init - This initializes pygame, must be done.
    # pg.display.set_caption(TITLE) - This sets the title of the window to
    # TITLE as defined in settings.
    def __init__(self):
        pg.init()
        pg.display.set_caption(TITLE)
        self.display_state = DisplayState(BOARD_ROWS, BOARD_COLS)
        self.width  = self.display_state.cols() * TILESIZE
        
        print("init")
        print(self.display_state.rows)
        self.screen = pg.display.set_mode( (800, 600) ) # This initialize the look of the screen.
        # self.display_state = DisplayState(BOARD_ROWS, BOARD_COLS)

    # The main game loop of the application
    def update(self):
        # print("Hello world")
        self.draw()

    def draw(self):
        self.draw_board()
        # print("Hey")
        pg.display.flip()

    def draw_board(self):
        self.screen.fill(BLACK)
        for c in range(self.display_state.cols()):
            for r in range(self.display_state.rows()):
                self.draw_piece(self.screen, (r,c), PIECECOLOR[self.display_state.get(r,c)], 2)

    # draw a tile (r,c) location with given parameters
    def draw_piece(self, surface, tile, color, border):
        row, col = self.display_state.rows() - 1 - tile[0], tile[1]
        # pg.draw.rect(self.screen, color, [col*TILESIZE+TILESIZE//2, row*TILESIZE+TILESIZE//2, TILESIZE//2-PIECEPAD, TILESIZE//2-PIECEPAD] )
        pg.draw.rect(self.screen, RED, [col*TILESIZE+TILESIZE//2, row*TILESIZE+TILESIZE//2, TILESIZE/2, TILESIZE//2-PIECEPAD+border])

# This is the main executable part of the program.

sys.setrecursionlimit(10000) # Can't go past 10000 recursive depth.

# This is the basic game object
game_object = Checkers()
game_loop = True
# game_object.update()

# This is the "game loop" of the program, it is an infinite loop that runs the game.
while game_loop:
    game_object.update()
    for event in pg.event.get():
        if event.type == pg.QUIT:
            game_loop = False

pg.quit()
quit()
            

