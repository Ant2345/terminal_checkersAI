# Program to implement a game of checkers in the terminal
# Logic from this will hopefully self.be applied and used in the 
# original checkers I made

import board, piece, player, evaluateFT, aBpruning, SARSArlPlayer, randomPlayer

from numpy import inf

# get undo working first, evaluation, game over seperately

class Checkers:

    def start(self, t_n):
    # Gather starting information to start the game with
        if not t_n:
            print('A simple game of checkers. Want to start?')
            y_n = input()
            if (y_n == 'yes') or (y_n == 'y') or (y_n == 'YES'):
                self.b = board.Board()
                self.b.populateBoard()
                self.setup(False, None, None, None, None)
            else:
                print("Aw, that's a shame. Goodbye.")
                pass
        else:
            self.b = board.Board()
            self.b.populateBoard()
            print('Training for RL player.')
        


    def setup(self, tRL, p1, p2, rl, rlOp):
        # if not (player_1 and player_2):
        if not tRL:
            vWho = input('HxH, HxCPU or CPUxCPU?\n(Human vs Human, Human vs CPU, or CPU vs CPU): \n')
            if (vWho == 'HxH'):
                if ((input("Do you want to use your names? ") == 'yes')):
                    name1 = input('Player 1, enter a name: ')
                    self.player_1 = player.Player(name1, 'r', 'Human')
                    name2 = input('Player 2, enter a name: ')
                    self.player_2 = player.Player(name2, 'w', 'Human')
                else:
                    self.player_1 = player.Player('Player 1', 'r', 'Human')
                    self.player_2 = player.Player('Player 2', 'w', 'Human')
            elif (vWho == 'HxCPU'):
                if ((input("Do you want to use your names? ") == 'yes')):
                    name1 = input('Player 1, enter a name: ')
                    self.player_1 = player.Player(name1, 'r', 'Human')
                else:
                    self.player_1 = player.Player('Player 1', 'r', 'Human')
                choice = input("aB, RL or random player? ")
                if ((choice == 'aB')):
                    self.player_2 = player.Player('Computer', 'w', 'aBCPU')
                    self.aBP2 = aBpruning.aBpruningMiniMax(self.player_2, self.b)
                elif (choice == 'RL'):
                    self.player_2 = player.Player('Computer', 'w', 'rLCPU')
                    self.rlP2 = SARSArlPlayer.sarsarlPlayer(self.player_2, self.b)
                elif (choice == 'random'):
                    self.player_2 = player.Player('Computer', 'w', 'randCPU')
                    self.randP2 = randomPlayer.randomPlayer(self.player_2, self.b)
            elif (vWho == 'CPUxCPU'):
                choice = input("Choose CPU to play: (RL, aB, random)? \nChoose from: RL v aB, RL v RL, aB v aB, RL v random, aB v random. \n")
                if ((choice == 'RL v aB')):
                    self.player_1 = player.Player('Computer 1', 'r', 'rLCPU')
                    self.rlP1 = SARSArlPlayer.sarsarlPlayer(self.player_1, self.b)
                    self.player_2 = player.Player('Computer 2', 'w', 'aBCPU')
                    self.aBP2 = aBpruning.aBpruningMiniMax(self.player_2, self.b)
                elif ((choice == 'RL v RL')):
                    self.player_1 = player.Player('Computer 1', 'r', 'rLCPU')
                    self.rlP1 = SARSArlPlayer.sarsarlPlayer(self.player_1, self.b)
                    self.player_2 = player.Player('Computer 2', 'w', 'rLCPU')
                    self.rlP2 = SARSArlPlayer.sarsarlPlayer(self.player_2, self.b)
                elif ((choice == 'aB v aB')):
                    self.player_1 = player.Player('Computer 1', 'r', 'aBCPU')
                    self.aBP1 = aBpruning.aBpruningMiniMax(self.player_1, self.b)
                    self.player_2 = player.Player('Computer 2', 'w', 'aBCPU')
                    self.aBP2 = aBpruning.aBpruningMiniMax(self.player_2, self.b)
                elif (choice == 'RL v random'):
                    self.player_1 = player.Player('Computer 1', 'r', 'rLCPU')
                    self.rlP1 = SARSArlPlayer.sarsarlPlayer(self.player_1, self.b)
                    self.player_2 = player.Player('Computer 2', 'w', 'randCPU')
                    self.randP2 = randomPlayer.randomPlayer(self.player_2, self.b)
                elif (choice == 'aB v random'):
                    self.player_1 = player.Player('Computer 1', 'r', 'aBCPU')
                    self.aBP1 = aBpruning.aBpruningMiniMax(self.player_1, self.b)
                    self.player_2 = player.Player('Computer 2', 'w', 'randCPU')
                    self.randP2 = randomPlayer.randomPlayer(self.player_2, self.b)
                else:
                    print("Invalid inputs! Restarting.")
                    self.setup() 
            else:
                print("Invalid inputs! Restarting.")
                self.setup()
        else:
            self.player_1 = p1
            self.rlP1 = rl
            self.player_2 = p2
            self.aBP2 = rlOp

        print("Game Start: \n")
        self.game()

    def game(self):
        # turns 
        self.pieces = self.b.howManyPieces()
        self.p1_pieces = self.pieces[0]
        # print(f"{self.player_1.getName()} has {self.p1_pieces} pieces left.")
        self.p2_pieces = self.pieces[1]
        # print(f"{self.player_2.getName()} has {self.p2_pieces} pieces left.")

        while ((self.p1_pieces > 0 and self.p2_pieces > 0)): # if they aren't both > 0 (i.e., one of them is out, all pieces checked)                

            # print(f'Value of current board state for P1: {evaluateFT.evaluate(self.player_1, self.b)}')

            # og_board1 = self.copyArray(self.b.board)

            # re-calculate pieces left
            self.pieces = self.b.howManyPieces()

            self.p1_pieces = self.pieces[0]

            # print(self.p1_pieces)

            if (self.p1_pieces == 1):
                print(f"{self.player_1.getName()} has {self.p1_pieces} piece left.")
            else:
                print(f"{self.player_1.getName()} has {self.p1_pieces} pieces left.")

            # check how many pieces in side of the self.board are None (i.e., which are captured)
            p1_collected = 12 - self.p2_pieces
            if (p1_collected == 0):
                print(f'{self.player_1.getName()} has captured {p1_collected} white piece.')
            elif (p1_collected > 0):
                print(f'{self.player_1.getName()} has captured {p1_collected} white pieces.')
            else:
                pass

            # player 1 turn
            print(f"\n{self.player_1.getName()}, your turn.\n")
            if (self.player_1.getType() == 'Human'):
                self.b.HumanMove(self.player_1, None)
            else: # assuming it's CPU
                if (self.player_1.getType() == 'aBCPU'):
                    res = self.aBP1.returnMove()
                    p_mov = res[0]
                    val, act_mov = p_mov
                    # print(f'possible move, {act_mov}')
                    rand_m = res[1]
                    if not act_mov:
                        print(f"Chose move: {rand_m}")
                        self.b.CPUMove(self.player_1, rand_m)
                    else:
                        print(f"Chose move: {act_mov}")
                        self.b.CPUMove(self.player_1, act_mov)   
                    # if (not p_mov or not act_mov):
                    #     print('No possible plays, passing.')
                    #     pass
                    print(f'Value returned after aBprune: {val}\n')
                elif (self.player_1.getType() == 'rLCPU'):
                    # move = self.rlP1.choose_action()
                    # self.b.CPUMove(self.player_1, move)          
                    Q = self.rlP1.SARSA()
                    print('Learned Q-values: ')
                    print(Q)
                # self.b.CPUMove(self.player_2, move)
                

            # # see if they want to undo (to test undo)
            # print('Board after your move displayed below: \n')
            # self.b.displayBoard()
            # undorN = input(f'{self.player_1.getName()}, Do you want to undo that prior move? \n')
            # if (undorN == 'Yes') or (undorN == 'Y') or (undorN == 'yes'):
            #     self.b.undo(og_board1)
            # else:
            #     pass

            # print(f'Value of current board state for P2: {evaluateFT.evaluate(self.player_2, self.b)}')

            # og_board2 = self.copyArray(self.b.board)

            # calculate pieces left (2nd index is 2nd player pieces)
            self.pieces = self.b.howManyPieces()

            self.p2_pieces = self.pieces[1]

            if (self.p2_pieces == 1):
                print(f"{self.player_2.getName()} has {self.p2_pieces} piece left.")
            else:
                print(f"{self.player_2.getName()} has {self.p2_pieces} pieces left.")

            # check how many pieces in side of the self.board are None (i.e., which are captured)
            p2_collected = 12 - self.p1_pieces
            if (p2_collected == 0):
                print(f'{self.player_2.getName()} has captured {p2_collected} red piece.')
            elif (p2_collected > 0):
                print(f'{self.player_2.getName()} has captured {p2_collected} red pieces.')
            else:
                pass

            # player 2 turn
            print(f"\n{self.player_2.getName()}, your turn.\n")
            if (self.player_2.getType() == 'Human'):
                self.b.HumanMove(self.player_2, None)
            else: # assuming this is a cpu turn
                if (self.player_2.getType() == 'aBCPU'):
                    res = self.aBP2.returnMove()
                    p_mov = res[0]
                    val, act_mov = p_mov
                    # print(f'possible move, {act_mov}')
                    rand_m = res[1]
                    # print(f'random move {rand_m}')
                    if not act_mov:
                        print(f"Chose move: {rand_m}")
                        self.b.CPUMove(self.player_2, rand_m)
                    else:
                        print(f"Chose move: {act_mov}")
                        self.b.CPUMove(self.player_2, act_mov)   
                    # if (not p_mov or not act_mov):
                    #     print('No possible plays, passing.')
                    #     pass
                    print(f'Value returned after aBprune: {val}\n')
                elif (self.player_2.getType() == 'rLCPU'): # RL player
                    # move = self.rlP2.choose_action()
                    # self.b.CPUMove(self.player_2, move)
                    Q = self.rlP2.SARSA()
                    print('Learned Q-values: ')
                    print(Q)
                elif (self.player_2.getType() == 'randCPU'):
                    move = self.randP2.choose_action()
                    self.b.CPUMove(self.player_2, move)
                # self.b.CPUMove(self.player_2, move)

            # # # see if they want to undo (to test undo)
            # print('Board after your move displayed below: \n')
            # self.b.displayBoard
            # undorN = input(f'{self.player_2.getName()}, Do you want to undo that prior move? \n')
            # if (undorN == 'Yes') or (undorN == 'Y') or (undorN == 'yes'):
            #     self.b.undo(og_board2)
            # else:
            #     pass
                # need to check win state stuff, game still going even when player has 0 pieces left

                # win state

        if (self.b.isGOver(self.player_1)):
            print(f'{self.player_2.getName()}, you win! ') 
            if (input('Reset?\n') == 'y'):
                self.reset() 
            else:
                return
        elif (self.b.isGOver(self.player_2)):
            print(f'{self.player_1.getName()}, you win! ')
            if (input('Reset?\n') == 'y'):
                self.reset()
            else:
                return
        # if (self.p2_pieces == 0): 
        #     print(f'{self.player_1.getName()}, you win! ')
        #     if (input('Reset?\n') == 'y'):
        #         self.reset()
        #     else:
        #         return
        # elif (self.p1_pieces == 0):
        #     print(f'{self.player_2.getName()}, you win! ') 
        #     if (input('Reset?\n') == 'y'):
        #         self.reset() 
        #     else:
        #         return
        
    # def reset(self):
    #     if self.b.isGOver(self.player_1) or self.b.isGOver(self.player_2):
    #         return 0
    #     else:
    #         self.b.populateBoard()
    #         self.game()


    # # Method to utilize in evaluation function (and general purposes)
    # # Returns a yes or no depending on if game is over, or ongoing
    # def isGameOver(self):
    #     if (self.p2_pieces == 0 or self.p1_pieces == 0): 
    #         return True
    #     else:
    #         return False



if __name__ == '__main__':
    game = Checkers()
    game.start(None)


        