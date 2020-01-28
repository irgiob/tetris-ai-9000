import time
from random import choice
import numpy as np
import pynput.keyboard as pyk
import pynput.mouse as pym
from functions import *

# scoring variables
score_per_line = 100
stay_alive_score = 1

# mouse controller variables
keyboard = pyk.Controller()
mouse = pym.Controller()
GAME_DIM = (20,10)
BOX_START_X = 284
BOX_END_X = 518
BOX_Y = 185
JUMP_DIST = 26
JUMP_DIST_REV = -1 * JUMP_DIST
TIME_GAP = 0.02
RESUME = (410,375)

# moveset for interchanging scanning direction
MOVE_SET = [(BOX_START_X,JUMP_DIST,BOX_END_X,-1),(BOX_END_X,JUMP_DIST_REV,BOX_START_X,1)]

GAME_OVER = np.array(17 * [[0]*10] + 3 * [[1,0,0,0,0,0,0,0,0,1]], dtype=np.float)

def run_game(pop, play_mode=False, display = False):
    # general initializations
    fitness = 0
    lines_cleared = 0
    side = 0
    
    # start game at right time
    if play_mode == False:
        keyboard.press(pyk.Key.space)
        keyboard.release(pyk.Key.space)
    elif play_mode == True:
        mouse.position = RESUME
        time.sleep(TIME_GAP)
        for i in range(2):
            mouse.press(pym.Button.left)
            mouse.release(pym.Button.left)
    time.sleep(2)

    # skip count down animation
    game_data = get_raw_data()
    while (game_data[-1] == EMPTY_ROW).all():
        game_data = get_raw_data()
    n_filled = np.sum(game_data)

    while True:
        #skips animations & breaks loop
        while n_filled == np.sum(game_data):
            # breaks loop if game over
            if np.array_equal(game_data, FULL_BOX) or \
            np.array_equal(game_data, GAME_OVER):
                return int(fitness)

            n_filled = np.sum(game_data) 
            game_data = get_raw_data()
        n_filled = np.sum(game_data)

        # initialization for every piece
        mouse.position = (MOVE_SET[side][0],BOX_Y)
        time.sleep(TIME_GAP)
        game_data = get_raw_data()
        scores = []
        skip_check = False
        fitness += stay_alive_score

        # loop through all possible moves
        while MOVE_SET[side][3]*(mouse.position[0] - MOVE_SET[side][2]) > 0:
            # breaks loop if game over
            if np.array_equal(game_data, FULL_BOX):
                return int(fitness)

            # checks for overlap issue
            if np.sum(game_data) != n_filled:
                skip_check = True
                break

            # calculate heuristic and store score of move
            cleared_now = check_line_clear(game_data)
            heuristics = calc_heuristics(game_data, cleared_now)
            scores.append(calc_score(heuristics,pop))

            #displays game data in terminal
            if display == True:
                print(display_game(game_data, lines_cleared))
                print(calc_heuristics(game_data,cleared_now))
                print(f'Score: {calc_score(heuristics,pop)}')

            # move on to next move and get data
            mouse.move(MOVE_SET[side][1],0)
            time.sleep(TIME_GAP)
            game_data = get_raw_data()

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
            mouse.position = (MOVE_SET[side][0]+(MOVE_SET[side][1]*best),BOX_Y)
            time.sleep(TIME_GAP)
            game_data = get_raw_data()

            # set piece and add line clear info
            cleared_now = check_line_clear(game_data)
            mouse.press(pym.Button.left)
            mouse.release(pym.Button.left)
            if cleared_now > 0:
                lines_cleared += cleared_now
                fitness += score_per_line * cleared_now
                while np.sum(game_data) == n_filled:
                    game_data = get_raw_data()
        
        # change scan direction
        side = (side + 1) % 2
            
    # returns lines cleared as the fitness score
    return int(fitness)