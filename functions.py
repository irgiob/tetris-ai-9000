from mss import mss
from PIL import Image
import numpy as np
import pynput.keyboard as pyk
import pynput.mouse as pym
import time

# configurations for main game screen capture and data logging
MAIN_GAME = {"top": 172, "left": 270, "width": 261, "height": 521} # coords on screen
GAME_DIM = (20,10) # 20x10 grid
EMPTY_SPACE = [0,0,0] # RGB color value of empty box
FULL_ROW = [1,1,1,1,1,1,1,1,1,1]
EMPTY_ROW = [0,0,0,0,0,0,0,0,0,0]
EMPTY_BOX = np.zeros(GAME_DIM)
FULL_BOX = np.ones(GAME_DIM)
START_POS = 26 # xy coordinate of first box
BOX_DIST = 52 # pixels

# configurations for next_piece screen capture and data logging
next_piece = {"top": 235, "left": 600, "width": 115, "height": 65} # coords on screen
NUM_NEXT = 3 # number of visible next pieces
NEXT_HEIGHT = next_piece['height'] # height between next pieces
NEXT_START = next_piece['top'] # position of first next piece
MAX_PAL = 600 # maximum color values for next pieces

def get_raw_data():
    # screen capture main game area and next piece area and get game data
    sct = mss()
    sct_main = sct.grab(MAIN_GAME)
    img_main = np.array(Image.frombytes("RGB", sct_main.size, sct_main.bgra, "raw", "BGRX"))
    next_img_list = [0,0,0]
    for i in range(NUM_NEXT):
        sct_next = sct.grab(next_piece)
        next_img_list[i] = Image.frombytes("RGB", sct_next.size, sct_next.bgra, "raw", "BGRX")
        next_piece['top'] += NEXT_HEIGHT
    next_piece['top'] = NEXT_START
    game_data, next_val_dict = image_to_game_data(img_main, next_img_list)
    return game_data, next_val_dict

def image_to_game_data(img_data, next_img_list):
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
    # uses the number of unique color values for each piece to identify which piece it is
    next_val_dict = [len(img.getcolors(MAX_PAL)) for img in next_img_list]
    return game_data, next_val_dict

# prints game status to terminal in a readable format
def display_game(game_data, next_val_dict, tetromino_str, lines_cleared):
    game_disp = ''
    for row in game_data:
        for col in row:
            if col == 0:
                game_disp += '  '
            elif col == 1:
                game_disp += 'X '
        game_disp += '\n'
    game_disp += f'Lines Cleared: {lines_cleared}\n'
    game_disp += f'Next:{tetromino_str[next_val_dict[0]]} | '
    game_disp += f' {tetromino_str[next_val_dict[1]]} | '
    game_disp += f' {tetromino_str[next_val_dict[2]]}\n'
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

# keyboard & mouse controlling commands
def press_space():
    keyboard = pyk.Controller()
    keyboard.press(pyk.Key.space)
    keyboard.release(pyk.Key.space)

def mouse_set(coordinates):
    mouse = pym.Controller()
    mouse.position = coordinates

def mouse_move(offset):
    mouse = pym.Controller()
    mouse.move(offset[0],offset[1])

def mouse_click():
    mouse = pym.Controller()
    mouse.press(pym.Button.left)
    mouse.release(pym.Button.left)

def mouse_pos():
    mouse = pym.Controller() 
    return mouse.position