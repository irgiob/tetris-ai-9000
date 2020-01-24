import numpy as np
import time
from game_config import *
from get_game_data import *

score_per_line = 100
stay_alive_score = 1

def run_game(pop, display=False):
    # general initializations
    last_time = time.time()
    fitness = 0
    lines_cleared = 0
    press_space()
    time.sleep(2)

    game_data, next_val_dict = get_raw_data()
    last_val_dict = next_val_dict
    while last_val_dict == next_val_dict:
        last_val_dict = next_val_dict
        game_data, next_val_dict = get_raw_data()

    while True:
        col = 1
        # initialization for every piece
        mouse_set((284,265))
        time.sleep(0.05)
        game_data, next_val_dict = get_raw_data()
        last_val_dict = next_val_dict
        scores = []
        skip_check = False
        fitness += stay_alive_score

        # loop through all possible moves
        for i in range(9):

            # breaks loop if game over
            for val in next_val_dict:
                if not (val in tetromino_str):
                    return int(fitness)

            # checks for overlap issue
            if next_val_dict != last_val_dict:
                skip_check = True
                break

            # get FPS
            fps = 1/(time.time()-last_time)
            last_time = time.time()

            # check is line clears
            cleared_now = check_line_clear(game_data)
            if cleared_now > 0:
                lines_cleared += cleared_now
                fitness += score_per_line * cleared_now
                skip_check = True
                mouse_click()
                time.sleep(0.05)
                break

            # calculate heuristic and store score of move
            heuristics = calc_heuristics(game_data, cleared_now)
            scores.append(calc_score(heuristics,pop))

            #displays game data in terminal
            if display == True:
                print(display_game(game_data, fps, next_val_dict, tetromino_str, lines_cleared))
                print(calc_heuristics(game_data,cleared_now))

            # move on to next move and get data
            mouse_move((26,0))
            time.sleep(0.05)
            game_data, next_val_dict = get_raw_data()
        
        heuristics = calc_heuristics(game_data, cleared_now)
        scores.append(calc_score(heuristics,pop))

        # get the best move and recreate it
        if skip_check == False:
            best = scores.index(max(scores))
            mouse_set((284+26*best,265)) 
            mouse_click()
            time.sleep(0.05)
            
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
    # time delay to skip over the line disappearing animation
    if lines_cleared > 0:
        time.sleep(0.5)
    return lines_cleared

# prints game status to terminal in a readable format
def display_game(game_data, fps, next_val_dict, tetromino_str, lines_cleared):
    game_disp = ''
    for row in game_data:
        for col in row:
            if col == 0:
                game_disp += '  '
            elif col == 1:
                game_disp += 'X '
        game_disp += '\n'
    game_disp += f'Current FPS: {fps:.2f}\n'
    game_disp += f'Lines Cleared: {lines_cleared}\n'
    game_disp += f'Next:{tetromino_str[next_val_dict[0]]} | '
    game_disp += f' {tetromino_str[next_val_dict[1]]} | '
    game_disp += f' {tetromino_str[next_val_dict[2]]}\n'
    return game_disp