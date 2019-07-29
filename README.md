# learning-tilemaps

## Installation

* Needs `Python 3` and Python package `pyglet`.

* The `master` branch is the testing branch. The `stable` branch should be bug-free. The stable branch is recommended 
for playing (reminder: switch to it with `git checkout stable`).

* Run with `python3 main.py`.

## Instructions for playing

* Move your character with WASD keys (all keyboard key references are lower case), hold left shift key to sprint.

* Select interaction from bottom menu by clicking the corresponding number on the keyboard, clicking the icon with the 
mouse, or scrolling the mouse wheel. Deselect by pressing Q on the keyboard. Click with the mouse on the screen to use 
the interaction. It will only work within a small interaction range (i.e. distances from your character).  

* If you are touched by an enemy, you will die. Restart the game by closing the window and running the program again.

## TODO

* env_objs should only have logic calculated and be rendered if they are on screen. Load all in the window at start up
and add new ones as they come on screen, as with tiles?
* Similarly for mobiles?