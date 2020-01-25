# Configuration Data based on screen and game position  
import numpy as np  
 
# configurations for main game screen capture and data logging
main_game = {"top": 172, "left": 270, "width": 261, "height": 521} # coords on screen
GAME_DIM = (20,10) # 20x10 grid
EMPTY_SPACE = [0,0,0] # RGB color value of empty box
FULL_ROW = [1,1,1,1,1,1,1,1,1,1]
EMPTY_ROW = [0,0,0,0,0,0,0,0,0,0]
EMPTY_BOX = np.zeros(GAME_DIM)
FULL_BOX = np.ones(GAME_DIM)
START_POS = 26 # xy coordinate of first box
BOX_DIST = 52 # pixels
OPP_DIR = {'right': 'left','left':'right'}

# configurations for next_piece screen capture and data logging
next_piece = {"top": 235, "left": 600, "width": 115, "height": 65}
NUM_NEXT = 3 # number of visible next pieces
NEXT_HEIGHT = next_piece['height'] # height between next pieces
NEXT_START = next_piece['top'] # position of first next piece
MAX_PAL = 600 # maximum color values for next pieces

# number of color values for each tetromino piece 
tetromino_str = {
    571 : 'Straight Piece',
    543 : 'Square Piece',
    548 : 'T Piece',
    563 : 'J Piece',
    533 : 'L Piece',
    510 : 'S Piece',
    387 : 'Z Piece',
    1   : 'Empty'
}

# Last Generation Data

last_gen = [[-2.556,-0.665,2.194,-0.326],
[-2.105,-0.244,2.194,-0.501],
[-2.556,-1.88,2.194,-1.303],
[-2.517,-0.102,0.733,-0.501],
[-2.897,-3.031,2.503,-0.777],
[-0.815,-3.031,2.385,-1.003]]