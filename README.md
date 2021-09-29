# [learning-tilemaps](https://github.com/eidoom/learning-tilemaps)

## Installation

* Needs `Python>=3.6` and Python package `pyglet`. 
  With `Python` installed, just `source sourceme` to setup a virtual environment with the supported version of `pyglet`.

* The `master` branch is the testing branch. 
  The `stable` branch should be bug-free. 
  `master` should be fine for playing, but if there're any problems, please report them on the [bug tracker](https://github.com/eidoom/learning-tilemaps/issues) and use `stable` for now (reminder: switch to this branch with `git checkout stable`).

* Run with `./main.py`.

## Instructions for playing

* Navigate main menu with `Arrow` keys and `Enter`. Enter main menu any time with `Esc`.

* Move your character with `wasd` keys (all keyboard key references are lower case), hold left `Shift` key to sprint.

* Select interaction from bottom menu by clicking the corresponding number on the keyboard, clicking the icon with the 
mouse, or scrolling the mouse wheel. Deselect by pressing `q` on the keyboard. Click with the mouse on the screen to use 
the interaction. It will only work within a small interaction range (i.e. small distances from your character).

* If you are touched by an enemy, you will die. Restart the game by closing the window and running the program again.

## Ad

Only you can free the land of the wicked ghouls that terrorise it!
You have been divinely gifted with the power to stop these ethereal monsters!
Be sure to smite with the appropriate spell!

Return this place to its former pastoral glory!
Just remember you can't swim!

### P.S.

The locals don't appreciate you freezing their flora.
Ignore anyone claiming the spirits are misunderstood peaceful refugees.

## TODO

* env_objs should only have logic calculated and be rendered if they are on screen. Load all in the window at start up
and add new ones as they come on screen, as with tiles?
* Similarly for mobiles?
