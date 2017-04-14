# Color Settings
BLACK       = (  53,   53,   53)
WHITE       = (255, 255, 255)
RED         = (255,   78,   78)
YELLOW      = (255, 255,   0)
BROWN       = (126,  87,  78) # Background colour 1
CORNSILK    = (237, 221, 204) # Background colour 2
PIECECOLOR  = [YELLOW, RED, WHITE, WHITE] # I’m not 100% what this does. From A2 settings file.

# Game Settings
TITLE     = "COMP 4752 - Checkers"
TILESIZE  = 80 # used to draw the board.

# Lists containing the default positions of checker locations
STARTING_RED_POSITIONS = [(0,1), (0,3), (0,5), (0,7), (1,0), (1,2), (1,4), (1,6), (2,1), (2,3), (2,5), (2,7) ]
STARTING_BLACK_POSITIONS = [ (7,0), (7,2), (7,4), (7,6), (6,1), (6,3), (6,5), (6,7), (5,0), (5,2), (5,4), (5,6) ]

# All the legal actions a red piece can do.
LEGAL_RED_ACTIONS = [ (1, -1), (1, 1) ]

# All the legal actions a black piece can do.                        
LEGAL_BLACK_ACTIONS = [ (-1, 1), (-1, -1) ]

# Checkers Settings, only PIECEPAD is used right now I believe. Will be used later for AI
# algorithm stuff.
PLAYER_ONE  = 0
PLAYER_TWO  = 1
PLAYER_NONE = 2
DRAW        = 3
BOARD_ROWS  = 8
BOARD_COLS  = 8
PIECEPAD    = 5
