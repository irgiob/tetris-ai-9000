from mss import mss
from PIL import Image
import numpy as np

## DISPLAY CONFIG ##
# display configuration variables (adjust position of game elements on your specific device)
TOP = 172
LEFT = 270
WIDTH = 261
HEIGHT = 521
BOX_START_X = 284
BOX_Y = 185
RESUME = (410,375)

# other game position variables (do not edit)
MAIN_GAME = {"top": TOP, "left": LEFT, "width": WIDTH, "height": HEIGHT} # coords on screen
START_POS = JUMP_DIST = round(WIDTH / 10)
BOX_DIST = JUMP_DIST * 2
BOX_END_X = LEFT + WIDTH - round(JUMP_DIST / 2)

# game-state variables
GAME_DIM = (20,10) # 20x10 grid
EMPTY_SPACE = [0,0,0] # RGB color value of empty box
FULL_ROW = [1,1,1,1,1,1,1,1,1,1]
EMPTY_ROW = [0,0,0,0,0,0,0,0,0,0]
EMPTY_BOX = np.zeros(GAME_DIM)
FULL_BOX = np.ones(GAME_DIM)
GAME_OVER = np.array(17 * [[0]*10] + 3 * [[1,0,0,0,0,0,0,0,0,1]], dtype=np.float64)
TIME_GAP = 0.02

def get_raw_data():
    # screen capture main game area and next piece area and get game data
    sct = mss()
    sct_main = sct.grab(MAIN_GAME)
    img_data = np.array(Image.frombytes("RGB", sct_main.size, sct_main.bgra, "raw", "BGRX"))
    # encode image data into digital reconstruction of game
    game_data = np.zeros(GAME_DIM)
    game_coords = (START_POS,START_POS)
    for i in range(GAME_DIM[0]):
        for j in range(GAME_DIM[1]):
            if (img_data[game_coords] == EMPTY_SPACE).all():
                game_data[i][j] = 0
            else:
                game_data[i][j] = 1
            game_coords = (game_coords[0],game_coords[1]+BOX_DIST)
        game_coords = (game_coords[0]+BOX_DIST,START_POS)
    return game_data

# prints game status to terminal in a readable format
def display_game(game_data, lines_cleared):
    game_disp = ''
    for row in game_data:
        for col in row:
            if col == 0:
                game_disp += '  '
            elif col == 1:
                game_disp += 'X '
        game_disp += '\n'
    game_disp += f'Lines Cleared: {lines_cleared}\n'
    return game_disp

# check if there is a line clear
def check_line_clear(game_data):
    lines_cleared = 0
    if np.array_equal(game_data, FULL_BOX) or np.array_equal(game_data, EMPTY_BOX):
        return 0
    for i in range(GAME_DIM[0]-1,-1,-1):
        if np.array_equal(game_data[i],FULL_ROW):
            lines_cleared += 1
    return lines_cleared

# calculate the score of potential move based on heuristics and weights
def calc_score(h, p):
    score=p[0]*h['H']+p[1]*h['AH']+p[2]*h['LC']+p[3]*h['B']
    return score

# calc heuristics for identifying whether a certain move is good or bad
def calc_heuristics(game_data, lines_cleared):
    if lines_cleared > 0:
        game_data = get_cleared_data(game_data)
    
    holes = 0
    heights = [0,0,0,0,0,0,0,0,0,0]
    for col in range(GAME_DIM[1]):
        reach_first = False
        for row in range(GAME_DIM[0]):
            if reach_first == False and game_data[row][col] == 1:
                reach_first = True
            if reach_first == True:
                heights[col] += 1
                if game_data[row][col] == 0:
                    holes += 1
    aggregate_height = sum(heights)
    bumpiness = calc_bumpiness(heights)
    return {'H': holes, 'AH': aggregate_height, 'LC': lines_cleared, 'B':bumpiness}

# calculate bumpiness of game data
def calc_bumpiness(heights):
    bumpiness = 0
    for i in range(len(heights)-1):
        bumpiness += abs(heights[i] - heights[i+1])
    return bumpiness

# get data after line clear
def get_cleared_data(game_data):
    for row in range(GAME_DIM[0]):
        if (game_data[row] == FULL_ROW).all():
            game_data[1:row+1] = game_data[0:row]
            game_data[0] = EMPTY_ROW
    return game_data