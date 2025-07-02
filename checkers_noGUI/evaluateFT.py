import board, piece, player, checkers_nogui

# Method to implement our evaluation function and process possible game states,
# movements, etc, to use in our abPruning/miniMax algorithm to build our aB pruning player

# Essentially returns a value based on who is winning

# only has win/lose condition realistically
# either is able to make one last jump which will result in a win (all the pieces of the opponent being captured)
# or, it will result in a jump being performed on it, and resulting in a lose (as all of it's pieces are captured)

# heuristic be (based on current position), how close it is to capturing a piece? (which is techincally the goal, but with all pieces to win)
# so maybe, checking if a piece exists in a given space (i.e., one that is a valid move/jump) and if a path has a capturable piece
# weight that path higher than the rest


def evaluate(player, b):
    # Evaluate potential instances of which the red player (or white player) can win 
    # (I'd assume any state where the other player only has one or two pieces remaining)
    # and the red player (or white player) could perform a jump and or several movements to capture both pieces
    # or one at a time, and win the game

    # check every row, col and diagonal placement to see what potential moves could occur
    # ex. if there's a corner with a red piece in 1,6 and white has a piece that moved to 2,5
    # if it is white's turn, it could jump to 0,7 and capture the last red piece, winning the game
    # if it is red's turn, it could jump from 1,6 to 3,4 (assuming its a king) and win the game

    # if the player has a piece that does not have further space to the direct right or left, it would be safe
    # from being checked (as there is no space to get past it)

    # from owen, realistically just checks the current board state (from the actual game)
    # and returns a value that is good/bad for either player
    # ex. if player 1 is red, and has 8 pieces while white has 4, the heuristic is -4 (4 - 8) which means red would want this board

    h = 0 # represents heuristic value that will change depending on how close piece is to a 'goal' (does this path have a capturable piece, etc)

    pieces = b.howManyPieces()

    

    p1_p = pieces[0]
    p2_p = pieces[1]

    # check if red or white piece
    if (player.getColor() == 'r'):
        dk = b.hFKing(player)
        # if h is positive, bad for red, if negative, good for red
        h = (p2_p - p1_p) + dk
        return h
        # difference between the amount of player 2's pieces left on the board
    elif (player.getColor() == 'w'):
        # if h is positive, bad for white, if negative, good for white
        dk = b.hFKing(player)
        h = (p1_p - p2_p) + dk
        # difference between the amount of player 1's pieces left on the board
        return h