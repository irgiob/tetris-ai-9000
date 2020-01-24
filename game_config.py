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

# miscellaneous data

last_gen = [[-0.859,-2.064,-0.502,-0.413],
[-0.561,-1.481,-0.137,-0.661],
[-0.859,-2.724,-0.622,-0.534],
[-1.576,-2.589,0.182,-0.661],
[-0.859,-2.064,-0.1,-0.413],
[-0.219,-1.398,-0.745,-0.661],
[-0.219,-1.042,-0.137,-0.235],
[-1.576,-1.921,0.271,-0.661],
[-0.219,-1.398,0.182,-0.661],
[-0.26,-2.46,-0.633,-1.429],
[-0.974,-2.064,-0.745,-0.661],
[-0.607,-1.921,0.271,-1.618]]

square = [['left'] * (i+1) for i in range(4)] + [['right'] * (i+1) for i in range(4)]
line =  [['left'] * (i+1) for i in range(3)] + \
        [['right'] * (i+1) for i in range(3)] + \
        [['up']+['left'] * (i+1) for i in range(5)] + \
        [['up']+['right'] * (i+1) for i in range(4)]
s = [['left'] * (i+1) for i in range(3)] + \
    [['right'] * (i+1) for i in range(4)] + \
    [['up']+['left'] * (i+1) for i in range(4)] + \
    [['up']+['right'] * (i+1) for i in range(4)]
z = s
j = [['left'] * (i+1) for i in range(3)] + \
    [['right'] * (i+1) for i in range(4)] + \
    [['up']+['left'] * (i+1) for i in range(4)] + \
    [['up']+['right'] * (i+1) for i in range(4)] + \
    [['up']*2+['left'] * (i+1) for i in range(3)] + \
    [['up']*2+['right'] * (i+1) for i in range(4)] + \
    [['up']*3+['left'] * (i+1) for i in range(3)] + \
    [['up']*3+['right'] * (i+1) for i in range(5)] 
l = j
t = j