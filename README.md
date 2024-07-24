# pygame
A game made with pygame - Pacman like, high score, randomised game map, fun animation
and toxic green blobs (static and not animated) to avoid.

Please feel free to clone, rip off, use and abuse.

This was written in VS Code with Codium installed for reasonable AI code completion suggestions.

To run:
- check the versions in pyproject.toml and make sure you have the same or greater for those python packages
- python3 pacman.py

There is a video screengrab of a couple of short games being played in drmalcs_pikmon_game_screengrab.webm
Navigate to it in a web browser to play (or type something like file://path/to/file/)

Commands:
q to quit
r to restart

The highscore will be remembered until you quit the game

I've not yet tested the poetry setup which would setup a python enviromment for you with the correct python and python package versions.

I can't remember where I got the fire animation and the accompanying sprite sheets. It was free to use and abuse. The player character is my own horrible animation.

TODO:
- split into more functions or classes
- possibly put some things in separate files
- generate doc strings once code split up into more functions
- BUG: try having non-equal numbers of rows and columns of tiles...
- BUG: player won't move forever with a direction key held down
- TODO: animate the green blobs with a sprite map, like the fire/pill pop
- TODO: make the end of game text cleaner/more readable
- TODO: animate HIGH SCORE
