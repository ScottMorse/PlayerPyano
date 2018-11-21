# PlayerPyano
This is a personal project mainly for my own enjoyment and learning, and it demonstrates a bit of how PyMusician can be used along with other libraries.

## Project structure
This project is simple, just a main file importing from some modules.  Main.py will run Pyglet eventually in order to supply something visual for show.

## synthesizer.py
This file runs the synth.  In the spirit of the project, each time the file runs, several options that affect the synth's timbre are randomized to give variety in tonal quality.

## ideas.py
This file contains the strategies that will be used to generate harmony and melody for the music generator.

## playerpyano.py
This creates a randomized musical environment and sends and receives data from ideas.py to use synthesizer.py to play the musical data (given in PyMusician objects).

## main.py
Will be used with Pyglet to create a visual.
