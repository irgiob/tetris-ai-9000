import numpy as np
from mss import mss
from PIL import Image
import cv2
import time
from pynput.keyboard import Key, Controller
from game_config import *
from get_game_data import *

score_per_line = 100
stay_alive_score = 0.1

def run_game(pop, display=False):
    # general initializations
    sct = mss()
    last_time = time.time()
    last_val = [0,0,0]
    
    fitness = 0
    lines_cleared = 0

    press_key('space')
    time.sleep(3.5)

    while True:
        # scren capture main game area and next piece area
        sct_main = sct.grab(main_game)
        img_main = np.array(Image.frombytes("RGB", sct_main.size, sct_main.bgra, "raw", "BGRX"))
        next_img_list = [0,0,0]
        for i in range(NUM_NEXT):
            sct_next = sct.grab(next_piece)
            next_img_list[i] = Image.frombytes("RGB", sct_next.size, sct_next.bgra, "raw", "BGRX")
            next_piece['top'] += NEXT_HEIGHT
        next_piece['top'] = NEXT_START

        # get game data (game-state, next pieces, lines cleared, and FPS)
        game_data, next_val_dict = image_to_game_data(img_main, next_img_list)
        fps = 1/(time.time()-last_time)
        last_time = time.time()

        # breaks loop if game over
        for val in next_val_dict:
            if not (val in tetromino_str):
                return int(fitness)
        
        cleared_now = check_line_clear(game_data)
        lines_cleared += cleared_now
        fitness += score_per_line * cleared_now + stay_alive_score

        heuristics = calc_heuristics(game_data, lines_cleared)
        decision = make_decision(pop, heuristics, next_val_dict)
        press_key(decision)

        #displays game data in terminal
        if display == True:
            print(display_game(game_data, fps, next_val_dict, tetromino_str, lines_cleared))
            print(calc_heuristics(game_data,lines_cleared))
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

# keyboard controlling commands for next phase
def press_key(key):
    keyboard = Controller()
    if key == 'left':
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif key == 'up':
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif key == 'right':
        keyboard.press(Key.right)
        keyboard.release(Key.right)
    elif key == 'space':
        keyboard.press(Key.space)
        keyboard.release(Key.space)

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