import time
import numpy as np
import pynput.keyboard as pyk
from functions import *

# global variables
NEXT_PIECES = {"top": TOP, "left": LEFT+WIDTH*1.3, "width": 1, "height": HEIGHT} # coords on screen
HOR_RANGE = [i for i in range(-5,6)]
LOADING_SCREEN = np.array(11 * [[0]*10] + 3 * [[1]*10] + 6 * [[0]*10], dtype=np.float64)
REST = 0.05
LOOK_AHEAD = 0 # requires BEEFY computer

# scoring variables
score_per_line = 100
stay_alive_score = 1

# keyboard controller variables
keyboard = pyk.Controller()

# run the game using AI
def run_game(pop, play_mode=False, display = False):
    # general initializations
    fitness = 0
    lines_cleared = 0
    turns_alive = 0

    # start bot at right time and get initial game data
    game_data = get_raw_data()
    while not (game_data == LOADING_SCREEN).all():
        game_data = get_raw_data()
    while (game_data == LOADING_SCREEN).all():
        game_data = get_raw_data()
    
    game_data = clean_game_data(game_data)
    next_piece_list = get_next_pieces()

    keyboard.press(pyk.Key.space)
    keyboard.release(pyk.Key.space)

    while True:
        # get the best score using next pieces and calculate no. of lines cleared 
        best = calc_best_score(next_piece_list[:LOOK_AHEAD+1], game_data, pop)
        position = move_down(move_hor(rotations[best[1]][best[2]],best[3]), game_data)
        game_data = put_on_board(position,game_data)
        lines_cleared += check_line_clear_jstris(game_data)
        turns_alive += stay_alive_score
        
        # prints game board to stdout if display is true
        if display:
            print(display_game(game_data,lines_cleared))
        
        # moves and rotates tetrimino in game to correct position
        for i in range(best[2]):
            keyboard.press(pyk.Key.up)
            keyboard.release(pyk.Key.up)
        if best[3] < 0:
            for i in range(best[3] * -1):
                keyboard.press(pyk.Key.left)
                keyboard.release(pyk.Key.left)
        else:
            for i in range(best[3]):
                keyboard.press(pyk.Key.right)
                keyboard.release(pyk.Key.right)

        # updates game state and next pieces and locks move
        time.sleep(REST)
        game_data = clean_game_data(get_raw_data())
        next_piece_list = get_next_pieces()

        keyboard.press(pyk.Key.space)
        keyboard.release(pyk.Key.space)

    return int(lines_cleared * 100 + turns_alive)

# calculates the best score
def calc_best_score(next_piece_list, game_data, pop):
    moves = []
    # get max score of each rotation and position
    for piece in next_piece_list[0]:
        for rotation in rotations[piece]:
            for pos in HOR_RANGE:
                position = move_hor(rotations[piece][rotation],pos)
                if valid_position(position,game_data):
                    position = move_down(position,game_data)
                    new_state = put_on_board(position,game_data)
                    scores = []
                    look_ahead_score(next_piece_list[1:],new_state,pop,scores)
                    score = max(scores)
                    moves.append([score, piece, rotation, pos])
    return max(moves)

# enhances move choice by looking ahead at future pieces
def look_ahead_score(next_piece_list, game_data, pop, scores):
    # calculates score of gameboard if no next pieces left
    if len(next_piece_list) == 0:
        lines_cleared = check_line_clear_jstris(game_data)
        h = calc_heuristics(game_data,lines_cleared)
        score = calc_score(h,pop)
        scores.append(score)
    # check all rotations and positions of next piece
    else:
        for piece in next_piece_list[0]:
            for rotation in rotations[piece]:
                for pos in HOR_RANGE:
                    position = move_hor(rotations[piece][rotation],pos)
                    if valid_position(position,game_data):
                        position = move_down(position,game_data)
                        new_state = put_on_board(position,game_data)
                        look_ahead_score(next_piece_list[1:],new_state,pop, scores)

# returns list of next tetriminos
def get_next_pieces():
    # screen capture main game area and next piece area and get game data
    sct = mss()
    sct_main = sct.grab(NEXT_PIECES)
    img_data = np.array(Image.frombytes("RGB", sct_main.size, sct_main.bgra, "raw", "BGRX"))
    output = []
    i = 0
    # searches a vertical strip of the screenshot to see colors
    while i < img_data.shape[0]:
        if img_data[i][0][0] in PIECE_COLOR['ALL']:
            # when colors matching the pieces are found, add them to output list
            output.append(PIECE_COLOR['ALL'][img_data[i][0][0]])
            while (img_data[i][0] != EMPTY_SPACE).all() and i < img_data.shape[0]:
                i += 1
        else:
            i += 1
    return output

# removes non-ghost piece for proper processing
def clean_game_data(game_data):
    i = 0
    while (game_data[i] == EMPTY_ROW).all():
        i += 1
        if i >= GAME_DIM[0]:
            exit()
    while not (game_data[i] == EMPTY_ROW).all():
        game_data[i] = EMPTY_ROW
        i += 1
        if i >= GAME_DIM[0]:
            exit()
    return game_data

# moves a tetrimino object on the game board in a certain direction
def move_hor(position, direction):
    output = [[0,0],[0,0],[0,0],[0,0]]
    for i in range(len(position)):
        output[i][0] = position[i][0]
        output[i][1] = position[i][1] + direction
    return output

# moves the tetrimino object down until it hits the game floor or other blocks
def move_down(position, game_data):
    obj_pos = [x[:] for x in position]
    while True:
        temp = [x[:] for x in obj_pos]
        for coords in temp:
            coords[0] += 1
        if valid_position(temp, game_data):
            for coords in obj_pos:
                coords[0] += 1
        else:
            break
    return obj_pos

# checks if the current position of the tetrimino is valid
def valid_position(position, game_data):
    for coords in position:
        # checks if piece position is out of bounds
        if coords[0] < 0 or coords[1] < 0:
            return False
        if coords[0] >= GAME_DIM[0]:
            return False
        if coords[1] >= GAME_DIM[1]:
            return False
        # check if piece intersects with other blocks already on the board
        if game_data[coords[0]][coords[1]] == 1:
            return False
    return True

# permanentally places a piece into the game board
def put_on_board(position, game_data):
    new_state = np.copy(game_data)
    for coords in position:
        new_state[coords[0]][coords[1]] = 1
    return new_state

# check for line clears
def check_line_clear_jstris(game_data):
    lines_cleared = 0
    if np.array_equal(game_data, FULL_BOX) or np.array_equal(game_data, EMPTY_BOX):
        return 0
    for i in range(GAME_DIM[0]):
        if np.array_equal(game_data[i],FULL_ROW):
            lines_cleared += 1
            game_data[1:i+1] = game_data[0:i]
            game_data[0] = EMPTY_ROW
    return lines_cleared

# tetrimino data

# the color of each tetrimino type on Jstris
PIECE_COLOR = {
    'L': [212,99,40], 
    'J': [33,70,191],
    'I': [66,154,210], 
    'S': [112,174,52],
    'Z': [198,46,61],
    'O': [218,161,55],
    'T': [161,56,135],
    'ALL': {212:'L',33:'J',66:'I',112:'S',198:'Z',218:'O',161:'T'}
}

# starting position of each tetrimino type in every rotation
rotations = {
    'O': {
        0: [[0,4],[0,5],[1,4],[1,5]]
    },
    'I': {
        0: [[0,3],[0,4],[0,5],[0,6]],
        1: [[0,5],[1,5],[2,5],[3,5]]
    },
    'T': {
        0: [[0,4],[1,3],[1,4],[1,5]],
        1: [[0,4],[1,4],[1,5],[2,4]],
        2: [[0,3],[0,4],[0,5],[1,4]],
        3: [[0,4],[1,3],[1,4],[2,4]]
    },
    'S': {
        0: [[0,4],[0,5],[1,3],[1,4]],
        1: [[0,4],[1,4],[1,5],[2,5]]
    },
    'Z': {
        0: [[0,3],[0,4],[1,4],[1,5]],
        1: [[0,5],[1,4],[1,5],[2,4]]
    },
    'J': {
        0: [[0,3],[1,3],[1,4],[1,5]],
        1: [[0,4],[0,5],[1,4],[2,4]],
        2: [[0,3],[0,4],[0,5],[1,5]],
        3: [[0,4],[1,4],[2,3],[2,4]]
    },
    'L': {
        0: [[0,5],[1,3],[1,4],[1,5]],
        1: [[0,4],[1,4],[2,4],[2,5]],
        2: [[0,3],[0,4],[0,5],[1,3]],
        3: [[0,3],[0,4],[1,4],[2,4]]
    }
}