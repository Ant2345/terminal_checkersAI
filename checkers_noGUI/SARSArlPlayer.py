# Class to define and implement an RL player (using on-policy SARSA, to later be replaced with Q-Learning) for the game, Checkers

from numpy import inf
import random as rand
import numpy as np

import checkers_nogui, player, evaluateFT, piece, aBpruning, randomPlayer

class sarsaRLPlayer:

    def __init__(self, player, game, episodes, alpha, gamma, epsilon):
        self.ep = episodes
        self.a = alpha
        self.g = gamma
        self.e =  epsilon
        self.game = game
        self.player = player
        self.start = self.game.b.copyArray(self.game.b.board)
        self.state = self.start
        self.st_idx = 0
        self.move_idx = 0
        self.reward = 0

    def SARSA(self):
        # Initialize Q-table
        Q = np.zeros((8, 8))

        # print(Q)

        for ep in range(self.ep):
            self.st_idx = 0
            self.move_idx = 0
            self.resetState()
            self.move = self.epsilon_greedy_policy(Q, self.state, self.e, self.st_idx) 
            self.st_idx += 1
            self.st_nidx = self.st_idx + 1
            self.move_idx += 1   
            self.nmove_idx = self.move_idx + 1
            # print(self.state, self.move)
            # print(f'SARSA move {self.move}')
            self.done = False

            while not self.done:
                self.st_idx = 0
                self.move_idx = 0
                self.next_state, self.reward, self.done = self.makeMove()
                self.next_move = self.epsilon_greedy_policy(Q, self.next_state, self.e, self.st_idx)

                self.st_idx += 1
                self.move_idx += 1 

                Q[self.st_idx, self.move_idx] += self.a * (self.reward + self.g * Q[self.st_nidx, self.nmove_idx] - Q[self.st_idx, self.move_idx])

                # self.st_nidx = self.st_idx + 1
                # self.nmove_idx = self.move_idx + 1

                self.state = self.next_state
                self.move = self.next_move

                
                
        return Q
    
    def resetState(self):
        # self.state = self.start
        self.game.b.undo(self.start)
        # return self.state

    def makeMove(self):
        self.game.b.CPUMove(self.player, self.move)
        if (self.game.b.isGOver(self.player)):
            self.reward = -5
            self.done = True
        elif (not self.game.b.isGOver(self.player)):
            self.reward = 5
            self.done = True
        else:
            self.state = self.game.b.board
        return self.game.b.board, self.reward, self.done
    
    def epsilon_greedy_policy(self, table, b_state, e, idx):
        if rand.uniform(0, 1) < e:
            return self.randMove(self.generateMove(b_state, self.player))
        else:
            return np.argmax(table[idx])
        
    def generateMove(self, board, player):
        if player.getColor() == 'w':
            moves = self.generateWBasicMoves(board)
        if player.getColor() == 'r':
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
        
    def make2DArray(self, val):
        b_arr = []
        for _ in range(val):
            arr = []
            for _ in range(val):
                arr.append(0)
            b_arr.append(arr)
        return b_arr


if __name__ == '__main__':

    game = checkers_nogui.Checkers()

    game.start(True)

    player_1 = player.Player('Computer 1', 'r', 'rLCPU')
    player_2 = player.Player('Computer 2', 'w', 'aBCPU')

    sarRLP = sarsaRLPlayer(player_1, game, 100, 0.1, 0.99, 0.9)

    aBopp = aBpruning.aBpruningMiniMax(player_2, game.b)

    game.setup(True, player_1, player_2, sarRLP, aBopp)

    # Q = sarRLP.SARSA()
    # print('Learned Q-values: ')
    # print(Q)

    # SARSA parameters defined
