Cindy Xiong (cindyxio)
# 15-112 Term Project - Monopoly (Fantasy ver.)
# Note: Also called "Fantasy Monopoly" at times for the sake of shortening

## Description
Monopoly (Fantasy ver.) is a single-player simplified game of Monopoly against 
an AI. Unlike the original Monopoly games which have 28 properties that include 
railroads and utilities in addition to streets, this game has 14 properties 
which are all color-coded streets with 6 different colors. The user is the 
white piece and the AI is the black piece. Both players start off with the 
same amount of money and the players move around the board by rolling two dice. 
If a player lands on a not owned property, they can buy it. They also have the 
choice to sell, trade, or build on their turns if these moves are legal. There 
are also various other ways to lose and gain money: the “Chance” spaces, which 
causes a random event out of a list of events to occur, and the “Magic Tax” 
spaces, which causes the player to lose $200. If you go to Jail, you stay for one 
turn and get out then by paying $50. The aim of the game for the user is to 
bankrupt the AI by making it lose all of its money and the user loses if they go 
bankrupt. However, the game will also end in 20 minutes if bankruptcy is not 
achieved, with the game going to whoever has more money.

## How to Run
This game was created in Python 3.8.5. To run the game, first download all of 
the files and make sure that all of the files are in the same folder. The files 
that should be present besides the main fantasy_monopoly.py are piece.py, 
property.py, words.py, and cmu_112_graphics_monopoly.py. Then, open 
fantasy_monopoly.py and press command+b on a Mac to run it if you are using 
VSCode. If you are using a different editor or IDE, run the file how it is 
normally done. The game should start immediately.

## Additional Information
There are no required libraries that need to be installed nor are there shortcut
commands that exist that will not be mentioned in the game itself.