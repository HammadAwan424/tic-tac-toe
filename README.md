# What it does?
Assign a score, either 0, 1 or -1 to each empty cell (actually, to each resulting board), which tells the user how
optimal each move for that particular game board, 
where 0 leads to a draw,
1 leads to maximizing player winning while -1 leads to 
minimizing player winning the game. It allows
manually setting up turns and game board to simulate different scenarios.

# Working Explained

## Initial Setup
Basically, the way it works is, it takes a game board (in a 3x3 numpy matrix) in a more user friendly form. Where:
- O is the minimizing player moves
- X is the maximizing player moves
- _'s represent cells not played

To represent and manipulate game board easily and efficiently, 
what I did first was, converted the string array/matrix into 8-bit signed integer
to have a more predictable memory usage (strings involve their own encodings and stuff).


## Core Logic
The calculations are done by calculating all possible set of moves the opponent can play, 
(if 5 cells were empty, this will create 5 child nodes)
and in turn cacluating all the possible moves to each move the opponent can play
(each of the 5 nodes will get 4 child nodes)
and so on (for each non-terminated branch) until having  the whole tree in memory recursively.

If we imagine the tree with root at the top, the tree will have a certain level of depth and each depth level/row is assigned
the "PLAYER" tag, which identifies the player for all those possible moves at that level. The identification of PLAYER is 
necessary at each level as that helps in deciding the game state {1, 0, -1} when there are multiple actions to choose from. 


If its the maximizing player's turn, it would choose the option which would lead to the maximum game state 
(picture in mind a scenario where there could be two moves played by X, one leading to O winning, and
other leading to a draw, X choose between 0 and -1, and choose the state with state = max(0. -1])).


This whole calculation could be part of O choosing between 3 different moves, and trying to approximate how
X will react to each of them, since one of the actions taken by O leads to aforementioned state which in turn
leads to draw, O will run the calculation for the two remaining cells, and if any of them leads to -1,
aka min([0, -1]), O will go down that route to maximize its chances of winning.
