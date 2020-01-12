import numpy as np
from mss import mss
from PIL import Image
import cv2
import time
from pynput.keyboard import Key, Controller, Listener
from game_config import *
from get_game_data import *

def run_game():
    # general initializations
    sct = mss()
    last_time = time.time()
    keyboard = Controller()
    SHOW_GAME = False

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

        # get game data and display it
        game_data, next_val_dict = image_to_game_data(img_main, next_img_list)
        fps = 1/(time.time()-last_time)
        last_time = time.time()
        print(display_game(game_data, fps, next_val_dict, tetromino_vals))

# prints game status to terminal in a readable format
def display_game(game_data, fps, next_val_dict, tetromino_vals):
    game_disp = ''
    for row in game_data:
        for col in row:
            if col == 0:
                game_disp += '  '
            elif col == 1:
                game_disp += 'X '
        game_disp += '\n'
    game_disp += f'Current FPS: {fps:.2f}\n'
    game_disp += f'Next:{tetromino_vals[next_val_dict[0]]} | {tetromino_vals[next_val_dict[1]]} | {tetromino_vals[next_val_dict[2]]}\n'
    return game_disp

# keyboard controlling commands for next phase
def press_key(key):
    if key == 'left':
        keyboard.press(Key.left)
        keyboard.release(Key.left)
    elif key == 'up':
        keyboard.press(Key.up)
        keyboard.release(Key.up)
    elif key == 'right':
        keyboard.press(Key.right)
        keyboard.release(Key.right)

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