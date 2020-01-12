from game_config import *
import numpy as np

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

def game_data_to_ml_input():
    pass

def calc_heuristics():
    pass