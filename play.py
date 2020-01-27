import numpy as np
import time
from functions import *
from random import choice

# scoring variables
score_per_line = 100
stay_alive_score = 1

# mouse controller variables
GAME_DIM = (20,10)
BOX_START_X = 284
BOX_END_X = 518
BOX_Y = 185
BOX_DIST = 26
JUMP_DIST = 2 * BOX_DIST
JUMP_DIST_REV = -1 * JUMP_DIST
TIME_GAP = 0.05
RESUME = (410,375)

# moveset for interchanging scanning direction
MOVE_SET = [(BOX_START_X,JUMP_DIST,BOX_END_X,-1),(BOX_END_X,JUMP_DIST_REV,BOX_START_X,1)]

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

def run_game(pop, play_mode=False, display = False):
    # general initializations
    fitness = 0
    lines_cleared = 0
    side = 0
    
    # start game at right time
    if play_mode == False:
        press_space()
        time.sleep(2)
    elif play_mode == True:
        mouse_set(RESUME)
        mouse_click()
        mouse_click()
        time.sleep(TIME_GAP)

    game_data, next_val_dict = get_raw_data()
    last_val_dict = next_val_dict

    while True:
        #skips animations & breaks loop
        while last_val_dict == next_val_dict:
            last_val_dict = next_val_dict
            
            # breaks loop if game over
            for val in next_val_dict:
                if not (val in tetromino_str):
                    return int(fitness)
            game_data, next_val_dict = get_raw_data()

            # correct occasional issue with next piece detection
            check = []
            for i in range(3):
                check.append(last_val_dict[i] != next_val_dict[i])
            if sum(check) == 1 or sum(check) == 2:
                next_val_dict = last_val_dict

        # initialization for every piece
        mouse_set((MOVE_SET[side][0],BOX_Y))
        time.sleep(TIME_GAP)
        game_data, next_val_dict = get_raw_data()
        last_val_dict = next_val_dict
        scores = []
        skip_check = False
        fitness += stay_alive_score

        # loop through all possible moves
        while MOVE_SET[side][3]*(mouse_pos()[0] - MOVE_SET[side][2]) > 0:

            # breaks loop if game over
            for val in next_val_dict:
                if not (val in tetromino_str):
                    return int(fitness)

            # checks for overlap issue
            if next_val_dict != last_val_dict:
                skip_check = True
                break

            # calculate heuristic and store score of move
            cleared_now = check_line_clear(game_data)
            heuristics = calc_heuristics(game_data, cleared_now)
            scores.append(calc_score(heuristics,pop))

            #displays game data in terminal
            if display == True:
                print(display_game(game_data, next_val_dict, tetromino_str, lines_cleared))
                print(calc_heuristics(game_data,cleared_now))
                print(f'Score: {calc_score(heuristics,pop)}')

            # move on to next move and get data
            mouse_move((MOVE_SET[side][1],0))
            time.sleep(TIME_GAP)
            game_data, next_val_dict = get_raw_data()
        
        # get the best move and recreate it
        if skip_check == False:
            heuristics = calc_heuristics(game_data, cleared_now)
            scores.append(calc_score(heuristics,pop))

            # get the best score (choose randomly if multiple best scores)
            max_score = max(scores)
            best_scores = []
            for i in range(len(scores)):
                if scores[i] == max_score:
                    best_scores.append(i)
            best = choice(best_scores)

            # move mouse to best score position and check for line clears
            mouse_set((MOVE_SET[side][0]+(MOVE_SET[side][1]*best),BOX_Y))
            time.sleep(TIME_GAP)
            game_data, next_val_dict = get_raw_data()
            cleared_now = check_line_clear(game_data)
            if cleared_now > 0:
                lines_cleared += cleared_now
                fitness += score_per_line * cleared_now
            
            # place the tetrimino
            mouse_click()
            last_val_dict = next_val_dict
        
        # change scan direction
        side = (side + 1) % 2
            
    # returns lines cleared as the fitness score
    return int(fitness)