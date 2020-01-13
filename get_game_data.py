from game_config import *
import numpy as np
from math import tan

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

def make_decision(p, h, n):
    decision_map = {0:'left',1:'up',2:'right',3:'none'}
    decision = [0,0,0,0]
    index = 0
    for i in range(0,len(p),7):
        decision[index]+=p[i]*h['H']+p[i+1]*h['AH']+p[i+2]*h['LC']+p[i+3]*h['B']+p[i+4]*tan(n[0])+p[i+5]*tan(n[1])+p[i+6]*tan(n[2])
        index += 1
    return decision_map[decision.index(max(decision))]

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

def calc_bumpiness(heights):
    bumpiness = 0
    for i in range(len(heights)-1):
        bumpiness += abs(heights[i] - heights[i+1])
    return bumpiness