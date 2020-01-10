import numpy as np
from PIL import Image
import cv2
import time
from pynput.keyboard import Key, Controller
from mss import mss

# initalizing screen capture locations and misc.

main_game = {"top": 169, "left": 265, "width": 269, "height": 529}
next_piece = {"top": 232, "left": 595, "width": 123, "height": 213}

sct = mss()
last_time = time.time()

# main screen recording loop
while True:
    # scren capture main game area & next piece area and convert to readable image
    sct_main = sct.grab(main_game)
    sct_next = sct.grab(next_piece)
    img_main = Image.frombytes("RGB", sct_main.size, sct_main.bgra, "raw", "BGRX")
    img_next = Image.frombytes("RGB", sct_next.size, sct_next.bgra, "raw", "BGRX")
    # diagnostic only, used to check frames-per-second (FPS)
    print('loop took {} seconds'.format(time.time()-last_time))
    last_time = time.time()
    # show screen capture
    cv2.namedWindow('main_game', cv2.WINDOW_NORMAL)
    cv2.imshow('main_game', cv2.cvtColor(np.array(img_main), cv2.COLOR_BGR2RGB))
    cv2.namedWindow('next_piece', cv2.WINDOW_NORMAL)
    cv2.imshow('next_piece', cv2.cvtColor(np.array(img_next), cv2.COLOR_BGR2RGB))
    # deactivate screen capture
    if cv2.waitKey(25) & 0xFF == ord('q'):
        cv2.destroyAllWindows()
        break

# keyboard controlling commands for next phase
''' keyboard = Controller()
    keyboard.press(Key.left)
    keyboard.release(Key.left)
    keyboard.press(Key.up)
    keyboard.release(Key.up)
    keyboard.press(Key.right)
    keyboard.release(Key.right)'''