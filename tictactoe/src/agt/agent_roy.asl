/*

Implementation of a Tic-Tac-Toe player that just plays random moves.

When the agent is started it must first perform a 'sayHello' action.
Once all agents have done this, the game or tournament starts.

Each turn the agent will observe the following percepts:

- symbol(x) or symbol(o) 
	This indicates which symbol this agent should use to mark the cells. It will be the same in every turn.

- a number of marks:  e.g. mark(0,0,x) , mark(0,1,o) ,  mark(2,2,x)
  this indicates which cells have been marked with a 'x' or an 'o'. 
  Of course, in the first turn no cell will be marked yet, so there will be no such percept.

- round(Z)
	Indicates in which round of the game we are. 
	Since this will be changing each round, it can be used by the agent as a trigger to start the plan to determine
	its next move.

Furthermore, the agent may also observe the following:

- next 
	This means that it is this agent's turn.
  
- winner(x) or winner(o)
	If the game is over and did not end in a draw. Indicates which player won.
	
- end 
	If the game is finished.
	
- After observing 'end' the agent must perform the action 'confirmEnd'.

To mark a cell, use the 'play' action. For example if you perform the action play(1,1). 
Then the cell with coordinates (1,1) will be marked with your symbol. 
This action will fail if that cell is already marked.

*/



/* Initial beliefs and rules */


// First, define a 'cell' to be a pair of numbers, between 0 and 2. i.e. (0,0) , (0,1), (0,2) ... (2,2).

isCoordinate(0).
isCoordinate(1).
isCoordinate(2).
isCorner(0).
isCorner(2).

isCell(X,Y) :- isCoordinate(X) & isCoordinate(Y).
isCorner(X,Y) :- isCorner(X) & isCorner(Y).     /* corner cells are (0,0),(0,2),(2,0),(2,2)

/* A cell is 'available' if it does not contain a mark.*/
available(X,Y) :- isCell(X,Y) & not mark(X,Y,_).
corner(X,Y) :- isCorner(X,Y) & not mark(X,Y,_).

/* Define marked cell */
myplayer(X,Y,symbol) .

// Define beliefs to represent the marks made by each player
myMark(X, Y) :- myplayer(X, Y, symbol).
opponentMark(X, Y) :- not myplayer(X, Y, _) & mark(X, Y, _).

// Define corners marked by either player
myCorner(X, Y) :- myMark(X, Y) & isCorner(X, Y).
oppCorner(X, Y) :- opponentMark(X, Y) & isCorner(X, Y).

started. 

/* Plans */
iStarted(false).
/* When the agent is started, perform the 'sayHello' action. */
+started <- sayHello.




/* Whenever it is my turn, this is the sequence:
- Mark the centre cell
	- if centre cell is taken mark, check how many cells opponent has
		- if opponent has only 1 cell, mark random corner cell
		- if opponent has 2 or more cells, check if there is winning move for myPlayer
			- if there is a winning move for the myPlayer, mark the winning cell
			- if there is no winning move for myPlayer, check if there is winning move for opponent
				- if there is a winning move for the opponent, block the opponent's winning cell
				- if there is no winning move for the opponent, mark a random corner cell

*/
+round(Z) : next <- .findall(available(X,Y),available(X,Y),AvailableCells);  
            		L = .length(AvailableCells);

			/* Update belief base */				
			.findall(myMark(X,Y),myMark(X,Y),MyMarks);                 /* - find all cells marked by myPlayer. */
			.findall(opponentMark(X,Y),opponentMark(X,Y),OppMarks);    /*- find all cells marked by Opponent player */
			.findall(corner(X,Y),corner(X,Y),AvailableCorners);        /* - find all available corners.*/
			LC = .length(AvailableCorners);

            /* If no marks have been made, play a random corner and set iStarted to true */
			if (.length(MyMarks) == 0 & .length(OppMarks) == 0) {
				NC = math.floor(math.random(LC));
				.nth(NC, AvailableCorners, corner(A,B));
				play(A,B);
				/* Set iStarted to true */
				iStarted(true);

			} else {
				if (iStarted ){    				/* If there are 7 or 8 available cells (i.e opponent has only 1 marked cell),*/
					if (L == 7){
						if (myMark(0, 0) & available(2, 2)) {
            				play(2, 2);
        				} else {
							if (myMark(0, 2) & available(2, 0)) {
            					play(2, 0); 
							} else {
								if (myMark(2, 0) & available(0, 2)) {
           	 						play(0, 2);
								} else {
									if (myMark(2, 2) & available(0, 0)) {
            							play(0, 0);
									} else {
										NC = math.floor(math.random(LC));
										.nth(NC, AvailableCorners, corner(A,B));
										play(A,B);
									}
								} 
        					}  
        				} 
        			} else {
                        .nth(N,AvailableCells,available(A,B));
						play(A,B);
                    }
				} else {
					if (L == 8){
						if (opponentMark(0, 0) & available(2, 2)) {
            				play(2, 2);
        				} else {
							if (opponentMark(0, 2) & available(2, 0)) {
            					play(2, 0); 
							} else {
								if (opponentMark(2, 0) & available(0, 2)) {
           	 						play(0, 2);
								} else {
									if (opponentMark(2, 2) & available(0, 0)) {
            							play(0, 0);
									} else {
										NC = math.floor(math.random(LC));
										.nth(NC, AvailableCorners, corner(A,B));
										play(A,B);
									}
								} 
        					}  
        				} 
        			} else {
                        .nth(N,AvailableCells,available(A,B));
						 play(A,B);
                    }
            
        		}
			}.									/*mark a random corner cell */
            				
											 
						 
/* If I am the winner, then print "I won!"  */
+winner(S) : symbol(S) <- .print("I won!").

+end <- confirmEnd.