import numpy as np
from PIL import Image
import cv2
import time
from pynput.keyboard import Key, Controller
from mss import mss

def main():
    # configurations for main game screen capture and data logging
    main_game = {"top": 172, "left": 270, "width": 261, "height": 521} # coords on screen
    GAME_DIM = (20,10) # 20x10 grid
    EMPTY_SPACE = [0,0,0] # RGB color value of empty box
    START_POS = 26 # xy coordinate of first box
    BOX_DIST = 52 # pixels

    # configurations for next_piece screen capture and data logging
    next_piece = {"top": 235, "left": 600, "width": 115, "height": 65}
    NUM_NEXT = 3 # number of visible next pieces
    NEXT_HEIGHT = next_piece['height'] # height between next pieces
    NEXT_START = next_piece['top'] # position of first next piece
    MAX_PAL = 600 # maxium color values for next pieces

    # number of color values for each tetromino piece 
    tetromino_vals = {
        571 : 'Straight Piece',
        543 : 'Square Piece',
        548 : 'T Piece',
        563 : 'J Piece',
        533 : 'L Piece',
        510 : 'S Piece',
        387 : 'Z Piece',
        1   : 'Empty'
    }

    # other initalizations
    sct = mss()
    last_time = time.time()
    keyboard = Controller()

    while True:
        # scren capture main game area and display on screen
        sct_main = sct.grab(main_game)
        img_main = np.array(Image.frombytes("RGB", sct_main.size, sct_main.bgra, "raw", "BGRX"))
        
        # screen capture next piece area and identify type of piece
        next_val_dict = [1,1,1]
        for i in range(NUM_NEXT):
            sct_next = sct.grab(next_piece)
            img_next = Image.frombytes("RGB", sct_next.size, sct_next.bgra, "raw", "BGRX")
            # uses the number of unique color values for each piece to identify which piece it is
            next_val_dict[i] = len(img_next.getcolors(MAX_PAL))
            next_piece['top'] += NEXT_HEIGHT
        next_piece['top'] = NEXT_START

        # encode image data into digital reconstruction of game
        game_data = np.zeros(GAME_DIM)
        game_coords = (START_POS,START_POS)
        for i in range(GAME_DIM[0]):
            for j in range(GAME_DIM[1]):
                if (img_main[game_coords] == EMPTY_SPACE).all():
                    game_data[i][j] = 0
                else:
                    game_data[i][j] = 1
                game_coords = (game_coords[0],game_coords[1]+BOX_DIST)
            game_coords = (game_coords[0]+BOX_DIST,START_POS)

        # DIAGNOSTICS: Display screen capture, calculate FPS, & display game data in terminal
        cv2.namedWindow('main_game', cv2.WINDOW_NORMAL)
        cv2.moveWindow('main_game',800,50)
        cv2.imshow('main_game', cv2.cvtColor(np.array(img_main), cv2.COLOR_BGR2RGB))
        fps = 1/(time.time()-last_time)
        last_time = time.time()
        print(display_game(game_data, fps, next_val_dict, tetromino_vals))
        
        # deactivate screen capture
        if cv2.waitKey(25) & 0xFF == ord('q'):
            cv2.destroyAllWindows()
            break

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

if __name__ == "__main__":
    main()