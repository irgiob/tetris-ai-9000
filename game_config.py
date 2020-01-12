# Configuration Data based on screen and game position    
 
# configurations for main game screen capture and data logging
main_game = {"top": 172, "left": 270, "width": 261, "height": 521} # coords on screen
GAME_DIM = (20,10) # 20x10 grid
EMPTY_SPACE = [0,0,0] # RGB color value of empty box
START_POS = 26 # xy coordinate of first box
BOX_DIST = 52 # pixels

# configurations for next_piece screen capture and data logging
next_piece = {"top": 235, "left": 600, "width": 115, "height": 65}
NUM_NEXT = 3 # number of visible next pieces
NEXT_HEIGHT = next_piece['height'] # height between next pieces
NEXT_START = next_piece['top'] # position of first next piece
MAX_PAL = 600 # maxium color values for next pieces

# number of color values for each tetromino piece 
tetromino_vals = {
    571 : 'Straight Piece',
    543 : 'Square Piece',
    548 : 'T Piece',
    563 : 'J Piece',
    533 : 'L Piece',
    510 : 'S Piece',
    387 : 'Z Piece',
    1   : 'Empty'
}