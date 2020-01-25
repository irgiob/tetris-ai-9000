import numpy as np
import time
from game_config import *
from get_game_data import *
from random import choice

score_per_line = 100
stay_alive_score = 1

# mouse controller variables
BOX_START_X = 284
BOX_END_X = 518
BOX_Y = 185
BOX_DIST = 26
JUMP_DIST = 2 * BOX_DIST
JUMP_DIST_REV = -1 * JUMP_DIST
TIME_GAP = 0.05

# moveset for interchanging scanning direction
MOVE_SET = [(BOX_START_X,JUMP_DIST,BOX_END_X,-1),(BOX_END_X,JUMP_DIST_REV,BOX_START_X,1)]

def run_game(pop, display=False):
    # general initializations
    fitness = 0
    lines_cleared = 0
    side = 0
    
    # start game at right time
    press_space()
    time.sleep(2)
    game_data, next_val_dict = get_raw_data()
    last_val_dict = next_val_dict

    while True:
        #skips animations
        while last_val_dict == next_val_dict:
            last_val_dict = next_val_dict
            game_data, next_val_dict = get_raw_data()
            while next_val_dict[0] == last_val_dict[0] and next_val_dict[1] == last_val_dict[1] and next_val_dict[2] != last_val_dict[2]:
                game_data, next_val_dict = get_raw_data()

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
                '''print(display_game(game_data, next_val_dict, tetromino_str, lines_cleared))
                print("ERROR")
                return'''
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

            # move mouse to best score position
            mouse_set((MOVE_SET[side][0]+(MOVE_SET[side][1]*best),BOX_Y))
            time.sleep(2*TIME_GAP)

            # check for line clears
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

# check if there is a line clear
def check_line_clear(game_data):
    lines_cleared = 0
    if np.array_equal(game_data, FULL_BOX) or np.array_equal(game_data, EMPTY_BOX):
        return 0
    for i in range(GAME_DIM[0]-1,-1,-1):
        if np.array_equal(game_data[i],FULL_ROW):
            lines_cleared += 1
    return lines_cleared

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