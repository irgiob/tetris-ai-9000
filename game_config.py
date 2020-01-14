# Configuration Data based on screen and game position  
import numpy as np  
 
# configurations for main game screen capture and data logging
main_game = {"top": 172, "left": 270, "width": 261, "height": 521} # coords on screen
GAME_DIM = (20,10) # 20x10 grid
EMPTY_SPACE = [0,0,0] # RGB color value of empty box
FULL_ROW = [1,1,1,1,1,1,1,1,1,1]
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
MAX_PAL = 600 # maxium color values for next pieces

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

last_gen = [[-0.951,0.73,0.46,-0.149],
[-1.591,-0.81,1.065,-0.534],
[0.756,0.73,-0.75,-0.074],
[-0.26,-0.204,-0.804,-0.534],
[-0.15,0.73,0.46,-1.003],
[-0.95,0.05,-0.209,0.63],
[-0.15,1.275,0.793,-0.358],
[0.611,0.73,-0.41,-0.358],
[-0.95,-0.577,1.065,-0.534],
[-0.26,-1.809,0.47,-0.534],
[-0.15,1.321,0.793,-0.68],
[-0.26,0.341,1.065,0.7]]

'''
straight = [([(0,0),(0,1)(0,2)(0,3)], 6),([(0,0),(1,0),(2,0),(3,0)], 10)]
square = [([(0,0),(0,1),(1,0),(1,1), 9])]
t = [([(1,0),(1,1),(0,1),(1,2)],8), ]'''