from game_config import *
from mss import mss
from PIL import Image
import cv2
import numpy as np
import pynput.keyboard as pyk
import pynput.mouse as pym
from math import tan

def get_raw_data():
    # scren capture main game area and next piece area and get game data
    sct = mss()
    sct_main = sct.grab(main_game)
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

# calculate the score of potential move based on heuristics and weights
def calc_score(h, p):
    score=p[0]*h['H']+p[1]*h['AH']+p[2]*h['LC']+p[3]*h['B']
    score = round(score,2)
    return score

# calc heuristics for identifying whether a certain move is good or bad
def calc_heuristics(game_data, lines_cleared):
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