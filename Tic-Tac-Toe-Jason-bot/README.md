# Tic Tac Toe Jason bot
 Creating a BDI agent to play tic tac toe against other agents

This is the logical flow that was intended for the Tic Tac Toe myPlayer:

/*
<start game>
Mark the centre cell
	- if centre cell is taken mark, check how many cells opponent has
		- if opponent has only 1 cell, mark random corner cell
		- if opponent has 2 or more cells, check if there is winning move for myPlayer
			- if there is a winning move for the myPlayer, mark the winning cell
			- if there is no winning move for myPlayer, check if there is winning move for opponent
				- if there is a winning move for the opponent, block the opponent's winning cell
				- if there is no winning move for the opponent, mark a random corner cell

*/
