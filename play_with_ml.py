import numpy as np
import time
from game_config import *
from get_game_data import *

score_per_line = 100
stay_alive_score = 0.1

def run_game(pop, display=False):
    # general initializations
    last_time = time.time()
    fitness = 0
    lines_cleared = 0
    press_key('space')
    time.sleep(3.5)

    while True:
        game_data, next_val_dict = get_raw_data()
        direction = left_or_right(game_data)
        opp_direction = OPP_DIR[direction]
        moves = ['up',opp_direction]

        scores = [0]
        # loop through all possible moves
        for i in range(4):
            for move in moves:
                # breaks loop if game over
                for val in next_val_dict:
                    if not (val in tetromino_str):
                        return int(fitness)

                # get FPS and increase fitness score for staying alive
                fps = 1/(time.time()-last_time)
                last_time = time.time()
                fitness += stay_alive_score

                # check is line clears
                cleared_now = check_line_clear(game_data)
                if cleared_now > 0:
                    print('Cleared Line!')
                    lines_cleared += cleared_now
                    fitness += score_per_line * cleared_now
                    time.sleep(1)
                    break

                # calculate heuristic and store score of move
                heuristics = calc_heuristics(game_data, lines_cleared)
                scores.append(calc_score(heuristics,pop))

                #displays game data in terminal
                if display == True:
                    print(display_game(game_data, fps, next_val_dict, tetromino_str, lines_cleared))
                    print(calc_heuristics(game_data,lines_cleared))

                # move on to next move and get data
                press_key(move)
                game_data, next_val_dict = get_raw_data()
            if cleared_now > 0:
                break
        # get the best move and recreate it
        best = scores.index(max(scores))
        if best % 2 == 1:
            press_key('up')
        for i in range(best//2):
            press_key(opp_direction)
            
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

def get_all_permutations(game_data, next_val_dict):
    pass

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

'''
# DIAGNOSTICS: Display screen capture
if SHOW_GAME:
    cv2.namedWindow('main_game', cv2.WINDOW_NORMAL)
    cv2.moveWindow('main_game',800,50)
    cv2.imshow('main_game', cv2.cvtColor(np.array(img_main), cv2.COLOR_BGR2RGB))

# deactivate screen display
if cv2.waitKey(25) & 0xFF == ord('q'):
    cv2.destroyAllWindows()
    break
'''