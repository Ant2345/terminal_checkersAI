# Methods to implement aBpruning functionality in the instance of a checkers game
# Goal is to process possible moves, and pick what should be the most beneficial
# utilizes miniMax to achieve this goal

# alpha is the value that changes with max
# beta is the value that changes with min

from numpy import inf
import random as rand

import checkers_nogui, player, evaluateFT, piece


# this function would take in and process the player data to determine if it returns the maxValue function
# or the minValue function depending on minPlayer/maxPlayer

class aBpruningMiniMax:

    def __init__(self, player, board):
        self.player = player
        self.b = board

    def returnMove(self):
        return self.maxValue(self.player, -inf, inf, self.b, 1), self.randMove(self.generateMove(self.b.board, self.player))
        # elif (self.player.getColor() == 'w'): # assuming r is always player 1, which i have it set up to be
        #     # if self.randMove(self.generateMove(self.b.board, self.player)):
        #     return self.minValue(self.player, -inf, inf, self.b, 1), self.randMove(self.generateMove(self.b.board, self.player))
        

    # alpha is positive infinity
    # beta is negative infinity

    # make new 'board' list instead of modifying in place when making potential moves

    # looping for each possible move is something we'd have to code situations for

    # ok, so the makeMove will return coordinates based on the current board state it was given
    # then it be played into effect on the board, then evaluated, based on that will determine
    # if we undo the state or let it go through, so the list of states is just gonna be a list of lists of coordinates
    # (since the coordinates would be like [x1, y1] to [x2, y2])

    # need to make sure the coordinates for moves are actually returned depending on their evaluation score, i.e., 
    # i think for my code, it would have to be returned with alpha/evaluation at some point (possibly just the index)

    # Method to implement calculating maxValue (of potential moves) to use in miniMax algorithm
    def maxValue(self, player, alpha, beta, b, depth):
        # pseudo code
        if b.isGOver(player) == True or depth == 0: # game is over/ depth is reached
            # return the values (should be payoff at end of or eval function)
            return evaluateFT.evaluate(player, b), None
        else:
            old_board = b.copyArray(b.board)
            moves = self.generateMove(b.board, player)
            print(moves)
            p_move = []
            for move in moves: # assuming each move is in the format [[x1, y1], [x2, y2]]
                print(f'{move}\n')
                print(f'current board eval before move: {evaluateFT.evaluate(player, b)}')
                b.CPUMove(player, move)
                print(f'current board eval after move: {evaluateFT.evaluate(player, b)}\n')
                b.undo(old_board)
                values, m2 = self.minValue(player, alpha, beta, b, depth - 1)
                p_move = move
                alpha = max(alpha, values)
                # print(f'alpha for max move is : {alpha}')
                if alpha >= beta:
                    return alpha, p_move   
            return alpha, p_move

    # Method to implement calculating minValue (of potential moves) to use in miniMax algorithm
    def minValue(self, player, alpha, beta, b, depth):
        # pseudo code
        if b.isGOver(player) == True or depth == 0: # means game is over / depth is reached
            # return the values (should be payoff at end of or eval function)
            return evaluateFT.evaluate(player, b), None
        else:
            old_board = b.copyArray(b.board)
            moves = self.generateMove(b.board, player)
            print(moves)
            p_move = []
            for move in moves: # assuming each move is in the format [[x1, y1], [x2, y2]]
                print(f'{move}\n')
                print(f'current board eval before move: {evaluateFT.evaluate(player, b)}')
                b.CPUMove(player, move)
                print(f'current board eval after move: {evaluateFT.evaluate(player, b)}')
                b.undo(old_board)
                values, m2 = self.maxValue(player, alpha, beta, b, depth - 1)
                # print(f'min vals {values}')
                p_move = move
                beta = min(beta, values)
                # print(f'alpha for min move is : {alpha}')
                if alpha >= beta:
                    return beta, p_move
            return beta, p_move
    # Method to generate possible moves based on the current board state
    # Will return a new board to be evaluated instead of modifying the actual board

    # seperate function to generate +1, -1 movements
    # seperate functions to generate 1/double jumps separately

    # currently, seemingly when king moves are generated, getting copies of the same move which i think causes recursion error if they are not valid as well
    def generateMove(self, board, player):
        if player.getColor() == 'w':
            moves = self.generateWBasicMoves(board)
        elif player.getColor() == 'r':
            moves = self.generateRBasicMoves(board)
        return moves
    
    def generateRBasicMoves(self, board):
        # generate moves going +1/-1 direction
        move = []
        for row in range(8):
            for col in range(8):
                if board[row][col] != None:
                    n = board[row][col]
                    if n.getColor() == 'r': 
                        # move up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] == None:
                                move.append(([row, col], [row - 1, col + 1]))
                        # move up to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] == None:
                                move.append(([row, col], [row - 1, col - 1]))
                    # Handling moves for red king (all 4 directions)
                    if n.getColor() == 'R':
                        # move down to the right
                        if (row + 1 <= 7 and col - 1 >= 0):
                            if board[row + 1][col - 1] == None:
                                move.append(([row, col], [row + 1, col - 1]))
                        # move down to the left
                        if (row + 1 <= 7 and col + 1 <= 7):
                            if board[row + 1][col + 1] == None:
                                move.append(([row, col], [row + 1, col + 1]))
                        # move up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] == None:
                                move.append(([row, col], [row - 1, col + 1]))
                        # move up to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] == None:
                                move.append(([row, col], [row - 1, col - 1]))
        return self.generateRJumpMoves(board, move)

    def generateWBasicMoves(self, board):
        # generate moves going +1/-1 direction
        move = []
        for row in range(8):
            for col in range(8):
                if board[row][col] != None:
                    n = board[row][col]
                    if n.getColor() == 'w': 
                        # move down to the right
                        if (row + 1 <= 7 and col - 1 >= 0):
                            if board[row + 1][col - 1] == None:
                                move.append(([row, col], [row + 1, col - 1]))
                            else:
                                pass
                        # move down to the left
                        if (row + 1 <= 7 and col + 1 <= 7):
                            if board[row + 1][col + 1] == None:
                                move.append(([row, col], [row + 1, col + 1]))
                    if n.getColor() == 'W':
                        # move up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] == None:
                                move.append(([row, col], [row - 1, col + 1]))
                            else:
                                pass
                        # move up to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] == None:
                                move.append(([row, col], [row - 1, col - 1]))
                        # move down to the right
                        if (row + 1 <= 7 and col - 1 >= 0):
                            if board[row + 1][col - 1] == None:
                                move.append(([row, col], [row + 1, col - 1]))
                            else:
                                pass
                        # move down to the left
                        if (row + 1 <= 7 and col + 1 <= 7):
                            if board[row + 1][col + 1] == None:
                                move.append(([row, col], [row + 1, col + 1]))
        return self.generateWJumpMoves(board, move)

    def generateRJumpMoves(self, board, moves):
        for row in range(8):
            for col in range(8):
                if board[row][col] != None:
                    n = board[row][col]
                    # Handling pawn jump
                    if n.getColor() == 'r':
                        if (row - 1 >= 0 and col + 1 <= 7):
                        # jump going up to the right
                            n_moveR = board[row - 1][col + 1]
                            if n_moveR != None:
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W': 
                                    if row - 2 >= 0 and col + 2 <= 7:
                                        if board[row - 2][col + 2] == None:
                                            moves.append(([row, col], [row - 2, col + 2]))
                        # jump going up to the left
                        if (row - 1 >= 0) and (col - 1 >= 0):
                            n_moveL = board[row - 1][col - 1]
                            if n_moveL != None:
                                if n_moveL.getColor() == 'w' or n_moveL.getColor() == 'W':
                                    if row - 2 >= 0 and col - 2 >= 0:
                                        if board[row - 2][col - 2] == None:
                                            moves.append(([row, col], [row - 2, col - 2]))
                    # Handling red king jump
                    if n.getColor() == 'R': 
                        # jump going down to the right
                        if (row + 1 <= 7 and col - 1 >= 0):
                            n_moveR = board[row + 1][col - 1]
                            if n_moveR != None:
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W': 
                                    if row + 2 <= 7 and col - 2 >= 0:
                                        if board[row + 2][col - 2] == None:
                                            moves.append(([row, col], [row + 2, col - 2]))
                        # jump going down to the left
                        if (row + 1 <= 7) and (col + 1 <= 7):
                            n_moveL = board[row + 1][col + 1]
                            if n_moveL != None:
                                if n_moveL.getColor() == 'w' or n_moveL.getColor() == 'W':
                                    if row + 2 <= 7 and col + 2 <= 7:
                                        if board[row + 2][col + 2] == None:
                                            moves.append(([row, col], [row + 2, col + 2]))
                        # jump going up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            n_moveR = board[row - 1][col + 1]
                            if n_moveR != None:
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W': 
                                    if row - 2 >= 0 and col + 2 <= 7:
                                        if board[row - 2][col + 2] == None:
                                            moves.append(([row, col], [row - 2, col + 2]))
                        # jump going up to the left
                        if (row - 1 >= 0) and (col - 1 >= 0):
                            n_moveL = board[row - 1][col - 1]
                            if n_moveL != None:
                                if n_moveL.getColor() == 'w' or n_moveL.getColor() == 'W':
                                    if row - 2 >= 0 and col - 2 >= 0:
                                        if board[row - 2][col - 2] == None:
                                            moves.append(([row, col], [row - 2, col - 2]))
        return self.generateRDoubleJumpMoves(board, moves)

    def generateWJumpMoves(self, board, moves):
        for row in range(8):
            for col in range(8):
                if board[row][col] != None:
                    n = board[row][col]
                    # Handling pawn jump
                    if n.getColor() == 'w':
                        if (row + 1 <= 7 and col - 1 >= 0):
                        # jump going up to the right
                            n_moveR = board[row + 1][col - 1]
                            if n_moveR != None:
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R': 
                                    if row + 2 <= 7 and col - 2 >= 0:
                                        if board[row + 2][col - 2] == None:
                                            moves.append(([row, col], [row + 2, col - 2]))
                        # jump going up to the left
                        if (row + 1 <= 7) and (col + 1 <= 7):
                            n_moveL = board[row + 1][col + 1]
                            if n_moveL != None:
                                if n_moveL.getColor() == 'r' or n_moveL.getColor() == 'R':
                                    if row + 2 <= 7 and col + 2 <= 7:
                                        if board[row + 2][col + 2] == None:
                                            moves.append(([row, col], [row + 2, col + 2]))
                    # Handling red king jump
                    if n.getColor() == 'W': 
                        # jump going up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            n_moveR = board[row - 1][col + 1]
                            if n_moveR != None:
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R': 
                                    if row - 2 >= 0 and col + 2 <= 7:
                                        if board[row - 2][col + 2] == None:
                                            moves.append(([row, col], [row - 2, col + 2]))
                        # jump going up to the left
                        if (row - 1 >= 0) and (col - 1 >= 0):
                            n_moveL = board[row - 1][col - 1]
                            if n_moveL != None:
                                if n_moveL.getColor() == 'r' or n_moveL.getColor() == 'R':
                                    if row - 2 >= 0 and col - 2 >= 0:
                                        if board[row - 2][col - 2] == None:
                                            moves.append(([row, col], [row - 2, col - 2]))
                        # jump going down to the right
                        if (row + 1 <= 7 and col - 1 >= 0):
                            n_moveR = board[row + 1][col - 1]
                            if n_moveR != None:
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R': 
                                    if row + 2 <= 7 and col - 2 >= 0:
                                        if board[row + 2][col - 2] == None:
                                            moves.append(([row, col], [row + 2, col - 2]))
                        # jump going down to the left
                        if (row + 1 <= 7) and (col + 1 <= 7):
                            n_moveL = board[row + 1][col + 1]
                            if n_moveL != None:
                                if n_moveL.getColor() == 'r' or n_moveL.getColor() == 'R':
                                    if row + 2 <= 7 and col + 2 <= 7:
                                        if board[row + 2][col + 2] == None:
                                            moves.append(([row, col], [row + 2, col + 2]))

        return self.generateRDoubleJumpMoves(board, moves)
            
    def generateRDoubleJumpMoves(self, board, moves):
        for row in range(8):
            for col in range(8):
                if board[row][col] != None:
                    n = board[row][col]
                    # Handling pawn jump
                    if n.getColor() == 'r':
                        # double jump going up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] != None:
                                n_moveR = board[row - 1][col + 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col + 2 <= 7):
                                        if (board[row - 2][col + 2] == None):
                                            if (row - 3 >= 0 and col + 3 <= 7):
                                                n_moveR2 = board[row - 3][col + 3]
                                                if n_moveR2 != None:
                                                    if n_moveR2.getColor() == 'w' or n_moveR2.getColor() == 'W': 
                                                        if row - 4 >= 0 and col + 4 <= 7:
                                                            if board[row - 4][col + 4] == None:
                                                                moves.append(([row, col], [row - 4, col + 4]))
                        # double (sideways) jump up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1 ] != None:    
                                n_moveR = board[row - 1][col + 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col + 2 <= 7):
                                        if (board[row - 2][col + 2] == None):
                                            if (row - 3 >= 0 and col + 1 <= 7):
                                                n_moveR = board[row - 3][col + 1]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W': 
                                                        if row - 4 >= 0 and col <= 7:
                                                            if board[row - 4][col] == None:
                                                                moves.append(([row, col], [row - 4, col]))
                        # double jump going up to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] != None:
                                n_moveR = board[row - 1][col - 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col - 2 >= 0): # checks that the first jump dest isnt a piece
                                        if (board[row - 2][col - 2] == None):
                                            if (row - 3 >= 0) and (col - 3 >= 0):
                                                n_moveL = board[row - 3][col - 3]
                                                if n_moveL != None:
                                                    if n_moveL.getColor() == 'w' or n_moveL.getColor() == 'W':
                                                        if row - 4 >= 0 and col - 4 >= 0:
                                                            if board[row - 4][col - 4] == None:
                                                                moves.append(([row, col], [row - 4, col - 4]))
                        # double (sideways) jump going up to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] != None:
                                n_moveR = board[row - 1][col - 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col - 2 >= 0): # checks that the first jump dest isnt a piece
                                        if (board[row - 2][col - 2] == None):
                                            if (row - 3 >= 0) and (col - 1 <= 7):
                                                n_moveL = board[row - 3][col - 1]
                                                if n_moveL != None:
                                                    if n_moveL.getColor() == 'w' or n_moveL.getColor() == 'W':
                                                        if row - 4 >= 0 and col <= 7:
                                                            if board[row - 4][col] == None:
                                                                moves.append(([row, col], [row - 4, col]))
                    # Handling red king jump (dont forget kings can do a jump that goes up and down unlike pawns)
                    if n.getColor() == 'R': 
                        # double jump up
                        if (row + 1 <= 7 and col + 1 <= 7):
                            if board[row + 1][col + 1] != None:
                                n_moveR = board[row + 1][col + 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row + 2 <= 7 and col + 2 <= 7):
                                        if (board[row + 2][col + 2] == None):
                                            if (row + 1 <= 7 and col + 3 <= 7):
                                                n_moveR = board[row + 1][col + 3]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W': 
                                                        if row <= 7 and col + 4 <= 7:
                                                            if board[row][col + 4] == None:
                                                                moves.append(([row, col], [row, col + 4]))
                        # double jump down
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] != None: 
                                n_moveR = board[row - 1][col + 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col + 2 <= 7):
                                        if (board[row - 2][col + 2] == None):
                                            if (row - 1 >= 0 and col + 3 <= 7):
                                                n_moveR = board[row - 1][col + 3]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W': 
                                                        if row <= 7 and col + 4 <= 7:
                                                            if board[row][col + 4] == None:
                                                                moves.append(([row, col], [row, col + 4]))
                        # double jump going down to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] != None:    
                                n_moveR = board[row - 1][col + 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col + 2 <= 7):
                                        if (board[row - 2][col + 2] == None):
                                            if (row - 3 >= 0 and col + 3 <= 7):
                                                n_moveR = board[row - 3][col + 3]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W': 
                                                        if row - 4 >= 0 and col + 4 <= 7:
                                                            if board[row - 4][col + 4] == None:
                                                                moves.append(([row, col], [row - 4, col + 4]))
                        # double jump going down to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] != None:
                                n_moveR = board[row - 1][col - 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col - 2 >= 0): # checks that the first jump dest isnt a piece
                                        if (board[row - 2][col - 2] == None):
                                            if (row - 3 >= 0) and (col - 3 >= 0):
                                                n_moveL = board[row - 3][col - 3]
                                                if n_moveL != None:
                                                    if n_moveL.getColor() == 'w' or n_moveL.getColor() == 'W':
                                                        if row - 4 >= 0 and col - 4 >= 0:
                                                            if board[row - 4][col - 4] == None:
                                                                moves.append(([row, col], [row - 4, col - 4]))
                        # double jump going up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] != None:
                                n_moveR = board[row - 1][col + 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col + 2 <= 7):
                                        if (board[row - 2][col + 2] == None):
                                            if (row - 3 >= 0 and col + 3 <= 7):
                                                n_moveR = board[row - 3][col + 3]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W': 
                                                        if row - 4 >= 0 and col + 4 <= 7:
                                                            if board[row - 4][col + 4] == None:
                                                                moves.append(([row, col], [row - 4, col + 4]))
                        # double (sideways) jump up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] != None:
                                n_moveR = board[row - 1][col + 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col + 2 <= 7):
                                        if (board[row - 2][col + 2] == None):
                                            if (row - 3 >= 0 and col + 1 <= 7):
                                                n_moveR = board[row - 3][col + 1]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W': 
                                                        if row - 4 >= 0 and col <= 7:
                                                            if board[row - 4][col] == None:
                                                                moves.append(([row, col], [row - 4, col]))
                        # double jump going up to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] != None:
                                n_moveR = board[row - 1][col - 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col - 2 >= 0): # checks that the first jump dest isnt a piece
                                        if (board[row - 2][col - 2] == None):
                                            if (row - 3 >= 0) and (col - 3 >= 0):
                                                n_moveL = board[row - 3][col - 3]
                                                if n_moveL != None:
                                                    if n_moveL.getColor() == 'w' or n_moveL.getColor() == 'W':
                                                        if row - 4 >= 0 and col - 4 >= 0:
                                                            if board[row - 4][col - 4] == None:
                                                                moves.append(([row, col], [row - 4, col - 4]))
                        # double (sideways) jump going up to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] != None:
                                n_moveR = board[row - 1][col - 1]
                                if n_moveR.getColor() == 'w' or n_moveR.getColor() == 'W':
                                    if (row - 2 >= 0 and col - 2 >= 0): # checks that the first jump dest isnt a piece
                                        if (board[row - 2][col - 2] == None):
                                            if (row - 3 >= 0) and (col - 1 >= 0):
                                                n_moveL = board[row - 3][col - 1]
                                                if n_moveL != None:
                                                    if n_moveL.getColor() == 'w' or n_moveL.getColor() == 'W':
                                                        if row - 4 >= 0 and col <= 7:
                                                            if board[row - 4][col] == None:
                                                                moves.append(([row, col], [row - 4, col]))
        return moves

    def generateWDoubleJumpMoves(self, board, moves):
        for row in range(8):
            for col in range(8):
                if board[row][col] != None:
                    n = board[row][col]
                    # Handling pawn jump
                    if n.getColor() == 'w':
                        # double jump going down to the right
                        if (row + 1 <= 7 and col - 1 >= 0):
                            if board[row + 1][col - 1] != None:    
                                n_moveR = board[row + 1][col - 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row + 2 <= 7 and col - 2 >= 0):
                                        if (board[row + 2][col - 2] == None):
                                            if (row + 3 <= 7 and col - 3 >= 0):
                                                n_moveR = board[row + 3][col - 3]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R': 
                                                        if row + 4 <= 7 and col - 4 >= 0:
                                                            if board[row + 4][col - 4] == None:
                                                                moves.append(([row, col], [row + 4, col - 4]))
                        # double (sideways) jump down to the right
                        if (row + 1 <= 7 and col - 1 >= 0):
                            if board[row + 1][col - 1] != None:
                                n_moveR = board[row + 1][col - 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row + 2 <= 7 and col - 2 >= 0):
                                        if (board[row + 2][col - 2] == None):
                                            if (row + 3 <= 7 and col - 1 >= 0):
                                                n_moveR = board[row + 3][col - 1]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R': 
                                                        if row + 4 <= 7 and col <= 7:
                                                            if board[row + 4][col] == None:
                                                                moves.append(([row, col], [row + 4, col]))
                        # double jump going down to the left
                        if (row + 1 <= 7 and col + 1 <= 7):
                            if board[row + 1][col + 1] != None:
                                n_moveR = board[row + 1][col + 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row + 2 <= 7 and col + 2 <= 7): # checks that the first jump dest isnt a piece
                                        if (board[row + 2][col + 2] == None):
                                            if (row + 3 <= 7) and (col + 3 <= 7):
                                                n_moveL = board[row + 3][col + 3]
                                                if n_moveL != None:
                                                    if n_moveL.getColor() == 'r' or n_moveL.getColor() == 'R':
                                                        if row + 4 <= 7 and col + 4 <= 7:
                                                            if board[row + 4][col + 4] == None:
                                                                moves.append(([row, col], [row + 4, col + 4]))
                        # double (sideways) jump going down to the left
                        if (row + 1 <= 7 and col + 1 <= 7):
                            if board[row + 1][col + 1] != None:
                                n_moveR = board[row + 1][col + 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row + 2 <= 7 and col + 2 <= 7): # checks that the first jump dest isnt a piece
                                        if (board[row + 2][col + 2] == None):
                                            if (row + 3 <= 7) and (col + 1 <= 7):
                                                n_moveL = board[row + 3][col + 1]
                                                if n_moveL != None:
                                                    if n_moveL.getColor() == 'r' or n_moveL.getColor() == 'R':
                                                        if row + 4 <= 7 and col <= 7:
                                                            if board[row + 4][col] == None:
                                                                moves.append(([row, col], [row + 4, col]))
                    # Handling white king jump (dont forget kings can do a jump that goes up and down unlike pawns)
                    if n.getColor() == 'W': 
                        # double jump up
                        if (row + 1 <= 7 and col + 1 <= 7):
                            if board[row + 1][col + 1] != None:
                                n_moveR = board[row + 1][col + 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row + 2 <= 7 and col + 2 <= 7):
                                        if (board[row + 2][col + 2] == None):
                                            if (row + 1 <= 7 and col + 3 <= 7):
                                                n_moveR = board[row + 1][col + 3]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R': 
                                                        if row <= 7 and col + 4 <= 7:
                                                            if board[row][col + 4] == None:
                                                                moves.append(([row, col], [row, col + 4]))
                        # double jump down
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] != None:
                                n_moveR = board[row - 1][col + 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row - 2 >= 0 and col + 2 <= 7):
                                        if (board[row - 2][col + 2] == None):
                                            if (row - 1 >= 0 and col + 3 <= 7):
                                                n_moveR = board[row - 1][col + 3]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R': 
                                                        if row <= 7 and col + 4 <= 7:
                                                            if board[row][col + 4] == None:
                                                                moves.append(([row, col], [row, col + 4]))
                        # double jump going up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] != None:
                                n_moveR = board[row - 1][col + 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row - 2 >= 0 and col + 2 <= 7):
                                        if (board[row - 2][col + 2] == None):
                                            if (row - 3 >= 0 and col + 3 <= 7):
                                                n_moveR = board[row - 3][col + 3]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R': 
                                                        if row - 4 >= 0 and col + 4 <= 7:
                                                            if board[row - 4][col + 4] == None:
                                                                moves.append(([row, col], [row - 4, col + 4]))
                        # double (sideways) jump up to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] != None:
                                n_moveR = board[row - 1][col + 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row - 2 >= 0 and col + 2 <= 7):
                                        if (board[row - 2][col + 2] == None):
                                            if (row - 3 >= 0 and col + 1 <= 7):
                                                n_moveR = board[row - 3][col + 1]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R': 
                                                        if row - 4 >= 0 and col <= 7:
                                                            if board[row - 4][col] == None:
                                                                moves.append(([row, col], [row - 4, col]))
                        # double jump going up to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] != None:
                                n_moveR = board[row - 1][col - 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row - 2 >= 0 and col - 2 >= 0): # checks that the first jump dest isnt a piece
                                        if (board[row - 2][col - 2] == None):
                                            if (row - 3 >= 0) and (col - 3 >= 0):
                                                n_moveL = board[row - 3][col - 3]
                                                if n_moveL != None:
                                                    if n_moveL.getColor() == 'r' or n_moveL.getColor() == 'R':
                                                        if row - 4 >= 0 and col - 4 >= 0:
                                                            if board[row - 4][col - 4] == None:
                                                                moves.append(([row, col], [row - 4, col - 4]))
                        # double (sideways) jump going up to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] != None:
                                n_moveR = board[row - 1][col - 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row - 2 >= 0 and col - 2 >= 0): # checks that the first jump dest isnt a piece
                                        if (board[row - 2][col - 2] == None):
                                            if (row - 3 >= 0) and (col + 1 <= 7):
                                                n_moveL = board[row - 3][col + 1]
                                                if n_moveL != None:
                                                    if n_moveL.getColor() == 'r' or n_moveL.getColor() == 'R':
                                                        if row - 4 >= 0 and col <= 7:
                                                            if board[row - 4][col] == None:
                                                                moves.append(([row, col], [row - 4, col]))
                        # double jump going down to the right
                        if (row - 1 >= 0 and col + 1 <= 7):
                            if board[row - 1][col + 1] != None:
                                n_moveR = board[row - 1][col + 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row - 2 >= 0 and col + 2 <= 7):
                                        if (board[row - 2][col + 2] == None):
                                            if (row - 3 >= 0 and col + 3 <= 7):
                                                n_moveR = board[row - 3][col + 3]
                                                if n_moveR != None:
                                                    if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R': 
                                                        if row - 4 >= 0 and col + 4 <= 7:
                                                            if board[row - 4][col + 4] == None:
                                                                moves.append(([row, col], [row - 4, col + 4]))
                        # double jump going down to the left
                        if (row - 1 >= 0 and col - 1 >= 0):
                            if board[row - 1][col - 1] != None:
                                n_moveR = board[row - 1][col - 1]
                                if n_moveR.getColor() == 'r' or n_moveR.getColor() == 'R':
                                    if (row - 2 >= 0 and col - 2 >= 0): # checks that the first jump dest isnt a piece
                                        if (board[row - 2][col - 2] == None):
                                            if (row - 3 >= 0) and (col - 3 >= 0):
                                                n_moveL = board[row - 3][col - 3]
                                                if n_moveL != None:
                                                    if n_moveL.getColor() == 'r' or n_moveL.getColor() == 'R':
                                                        if row - 4 >= 0 and col - 4 >= 0:
                                                            if board[row - 4][col - 4] == None:
                                                                moves.append(([row, col], [row - 4, col - 4]))
        return moves

    def randMove(self, move_list):
        if move_list:
            end = len(move_list) - 1
            ran = rand.randint(0, end)
            print(f'rand move {move_list[ran]}')
            return move_list[ran]
        else:
            # print('No moves in list.')
            return

# if __name__ == '__main__':
#     aBprune_miniMax()
