# Tetris AI 9000
# backstory
Ever since high school, me and a friend of mine have been competing to get the high score in a version of online Tetris, specifically [this version](https://tetris.com/play-tetris/).

Since then, I haven't gotten much better at the game (worst in fact), but I have gained some more experience in computer programming. Thats why I decided to start my dive into AI and machine learning by creating a Tetris AI that can finally beat my friend's high score in the game (and also to gain a better understand in modern software technology-but mostly the first thing).

# specific info on the project
The program first takes a screenshot of my screen, and converts it into a numpy array the computer can understand by analyzing the color of certain pixels on the game board in specific locations (using mss, pillow, OpenCV, & numpy). By reading the image, the program has info on the game-state (the position of the tetriminos), as well as the next 3 pieces that will be available for every game-frame. 

This data will then be fed into a [this genetic algorithm](https://theailearner.com/2018/11/09/snake-game-with-genetic-algorithm/) used to train the AI using a weights-and-biases method. The heuristics and fitness function used for this program are inspired by another Tetris AI made by Yiyuan Lee, which can be [found here](https://codemyroad.wordpress.com/2013/04/14/tetris-ai-the-near-perfect-player/), with some changes since this is playing off an official online version rather than one made from scratch (which I will also do at some point). The genetic algorithm trains by playing the game over and over again, and based on the value of the weights will decide what course of action to take in the game, getting better over time.

# to-do list
- [x] allow the program to capture the game's image data from the screen
- [x] allow the program a way to control the game
- [x] add feature to convert the image data of the game-state to a format readable by the program
- [x] add feature to allow the program to know what piece(s) are coming next
- [x] build basic genetic algorithm
- [ ] edit algorithm with proper heuristics, fitness function, proper inputs and outputs
- [ ] train genetic algorithm
- [ ] crush all opponents in Tetris

This was just an idea for a fun project I could do to finally start learning about AI and machine learning. Hopefully it can also help you undestand it better if you're just starting out too.
