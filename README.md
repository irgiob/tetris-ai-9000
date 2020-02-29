# Tetris AI 9000

## backstory
Ever since high school, me and a friend of mine have been competing to get the high score in a version of online Tetris, specifically [this version](https://tetris.com/play-tetris/).

Since then, I haven't gotten much better at the game (worst in fact), but I have gained some more experience in computer programming. Thats why I decided to start my dive into AI and machine learning by creating a Tetris AI that can finally beat my friend's high score in the game (and also to gain a better understand in modern software technology-but mostly the first thing).

The goal was to get the AI to clear at least 200 Lines, (enough line clears to beat my and my friend's high score) but after 6 iterations of the game, the program is actually able to reach the maximum of 300 line clears.

## specific info on the project
The program first takes a screenshot of my screen, and converts it into a numpy array the computer can understand by analyzing the color of certain pixels on the game board in specific locations (using mss, pillow, & numpy). By reading the image, the program has info on the game-state (the position of the tetriminos) for every game-frame. 

This data will then be fed into [this genetic algorithm](https://theailearner.com/2018/11/09/snake-game-with-genetic-algorithm/) used to train the AI using a weights-and-biases method. The heuristics and fitness function used for this program are inspired by another Tetris AI made by Yiyuan Lee, which can be [found here](https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/), with some changes since this is playing off an official online version rather than one made from scratch (which I will also do at some point). The genetic algorithm trains by playing the game over and over again, and based on the value of the weights will decide what course of action to take in the game, getting better over time.

<p align="center"><img src=images/gameplay.gif alt="Game During Play" width=500></p>

## training and winning
The AI was trained at level 25 of the game to increase training speed. The program basically moves the mouse across the game board, causing the tetrimino to move, and gives a score for the new game state for each potential position the piece can go, with the scoring using the weights from the G.A and the heuristics. The only downside of this method is the AI can't play lower levels, since earlier levels start with the tetrimino in the air and that messes up the AI's ability to play.

After training the AI for almost 3000 games and going through 6 versions of the program, The AI can now get to the max level (level 30) every single time. Since the AI can't play lower levels, I played like I normally do until things started speeding up at level 15. Then I let the AI takeover to play the levels I can't normally play. From there I just watched the AI clear line after line until it reached the High Level Barrier (again, see issues section below), where by that point I had beaten my high-score. The final score was around 700,000, compared to my original high-score of around 560,00. With over 250 line clears, I finally accomplished the original goal, and have beaten my (and my friends) score in Online Tetris.

<p align="center"><img src=images/scores_screen.png alt="High Score Page" width=500></p>

Though I still want to improve the AI to the point where it could reach a score of 1 Million, the main goal has been reached. The AI can now basically complete the game every time. The only problem is the moves it makes aren't the most efficient, as it will just go for any type of line clear instead of going for line clears that give the most scores, like triple or quadruple line clears. I will try to improve this in the future by training the AI with higher rewards for better-scoring line clears, and perhaps training the AI to use the hold-piece mechanic.

## how to use the program
1. Open the Tetris game website and python script, and arrange your window so both the game and whatever app you're using to run the python program are both fully visible. Set the Tetris game to be on the pause menu. 
2. Run the display_config.py script and follow the instructions to get the variables needed to run the program on your specific device.
3. Copy paste the indicated output from display_config.py into its proper place under DISPLAY CONFIG in functions.py.
4. If you want to use the already trained AI, all the settings are already set for that. Simply run the main.py program.
5. If you want to train the AI yourself, set MODE in main.py to 'TRAIN' instead of 'PLAY'. Then you can set whether you'll be starting from scratch or continuing from previous generation data. You can also just specific genetic algorithm variables such as population and mating pool.

## version history
Version 1: The genetic algorithm was used to choose a specific move; each frame the genetic algorithm would calculate a score for going left, right or rotate, and choose the move that had the highest score. This version did very poorly, achieving only a high score of 3 lines even with 25 generations.

Version 2: The program would start the piece on the most left side and move its way to the right while also rotating using keyboard commands, getting the score of each position as it passed it. This was a better strategy, however the high score was still only 3 lines even after the same amount of generations.

Version 3: This version switched from using keys to play the game to using the mouse. When using the mouse, the game automatically orients the piece to the best orientation based on which column the mouse is in, so I didn't have to worry about testing different orientation. It also allowed the piece to get across the entire board, even if there were pieces blocking the path. This version had much better results, with a high score 18 lines after 32 generations

Version 4: Version 3 had bugs where it would sometimes return to the wrong column, or completely skip over some pieces, due to the program taking too long causing the piece to set in place. Changing the program to check the score every 2 columns instead of every single column managed to fix this issue, reaching an even higher score. After further tinkering, Version 3 reached a high score of 150 line clears.

Version 5: Just a slightly optimized and cleaner version of version 4. This is the current final version of the program.

Version 6: Removed next piece visibility, to improve the speed. Also changed it so the program scans every line instead of every two lines. With numerous other small optimizations, the program can now reach the max level without any issues every time.

## libraries used
- numpy: generally important for any AI or machine learning program to create arrays
- time: in some areas the program worked faster than the game, so time.sleep was used to compensate
- random: randint was used to pick a move in the event of multiple equally good moves
- mss: screen capturing library, much faster than PIL 
- PIL: although not used for screen capturing, it was still used to convert the image data into a numpy array
- Pynput: keyboard and mouse controlling library

## whats next?
At this point the program is pretty much finished and fully operational, even with configuration options so you can use it on your own devices. The program however was only designed to get as many line clears as possible, instead of getting the most high-scoring line clears as possible.

If I were to continue working on the Tetris AI, I would try to train the AI to make smarter decisions that lead to more points. This would include adding more heuristics, a better scoring system, utilizing the look-ahead pieces, and adding a button to use the hold mechanic.

This was just an idea for a fun project I could do to finally start learning about AI and machine learning. Hopefully it can also help you understand it better if you're just starting out too.
