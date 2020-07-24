from pynput import mouse
import json

## RUN BEFORE RUNNING MAIN ##
# use this file to configure the programs display
# of the game on your specific device

config = []

# returns click coordinates and stops listener
def on_click(x, y, button, pressed):
    if pressed:
        config.append((int(x),int(y)))
    else:
        return False

# mouse click steps to determine size of game board on device display
steps = [
    'Welcome to Display Configuration Helper. Click anywhere to begin.',
    '\nStep 1. Adjust windows so game and terminal are both visible. \
    \nThen put the game on the pause menu. Click anywhere once done.',
    '\nstep 2. Click the top left corner of the game board (inner border)',
    '\nstep 3. Click the bottom right corner of the game board (inner border)',
    '\nstep 4. Click the center of the top-left most box',
    '\nstep 5. Click anywhere on the resume button.'
]

# goes through each step and records all mouse click coordinates for each step
for step in steps:
    print(step)
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()

# converts mouse coordinates to all variables needed for program
print(
    f'\nConfiguration Complete.\
    \nTOP = {config[2][1]}\
    \nLEFT = {config[2][0]}\
    \nWIDTH = {config[3][0] - config[2][0]}\
    \nHEIGHT = {config[3][1] - config [2][1]}\
    \nBOX_START_X = {config[4][0]}\
    \nBOX_Y = {config[4][1]}\
    \nRESUME = {config[5]}\n'
)

# saves settings to JSON
output = {
    'TOP': config[2][1], 
    'LEFT': config[2][0], 
    'WIDTH': config[3][0] - config[2][0],
    'HEIGHT': config[3][1] - config [2][1],
    'BOX_START_X': config[4][0],
    'BOX_Y': config[4][1],
    'RESUME': config[5]
}

with open('display_config.txt', 'w') as json_file:
  json.dump(output, json_file)