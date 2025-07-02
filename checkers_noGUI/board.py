# Class to represent a board in a game of checkers
# Tends to be an 8 x 8 board
# Can represent empty white/black spaces with 0, 1

import piece

class Board:

    def __init__(self):
        pass

    # Method to populate the board with pieces and None in places of 
    # empty space

    def populateBoard(self):
        self.board = []
        for row in range(8): 
            list = []
            for col in range(8):
                if (row >= 0 and row < 3):
                    if row % 2 == 0:
                        if col % 2 != 0:
                            list.append(piece.Piece('w', "pawn"))
                        else: 
                            list.append(None)
                    elif row % 2 != 0:
                        if col % 2 == 0: 
                            list.append(piece.Piece('w', "pawn"))
                        else:
                            list.append(None)
                elif (row >= 3 and row < 5):
                    list.append(None)
                elif (row >= 5 and row < 8):
                    if row % 2 == 0:
                        if col % 2 != 0:
                            list.append(piece.Piece('r', "pawn"))
                        else:
                            list.append(None)
                    elif row % 2 != 0:
                        if col % 2 == 0:
                            list.append(piece.Piece('r', "pawn"))
                        else:
                            list.append(None)
            self.board.append(list)

    # Method to display the board in a cleaner format          
    
    def displayBoard(self):

        val = 0
        v = 0
        for i in range(9):
            if i == 0:
                print('   ', end='')
            else:    
                print(f' {v} ', end='')
                v += 1
                
        print()      
        for row in self.board:
            board = ''
            r = ''
            r = r + f' {val} '
            val += 1
            for node in row:
                if node != None:
                    # print(node)
                    board = board + f' {node.getColor()} '
                else:
                    # print(node)
                    board = board + f' _ '
            print(r, end='')
            print(board)
        print()

    # Idea about dealing with movement of pawns vs king (being able to move backwards/forwards, or horizontal and tell where
    # you end up at that point (also helps with calculating 2 moves in a row))
    # as in, for the row/col if you take the subtraction of the two points given, if the result is positive, then it's moving
    # 'upwards', if negative, then downward

    # for dealing with only going horizontal, we can check that the inputted move
    # is within a certain range
    # for the initial going forward from red's perspective, if the upper left and right exist, they would be the upper row 
    # (so current row - 1) and then the current col -1 is the upper left, and +1 is the upper right
    # 
    
    # for the white pieces, if the lower right and lower left exist, they would be the 'lower row' (since here it would actually be current row += 1)
    # then the current col - 1 is the lower right, and +1 the lower left

    # for both, exception is corner pieces, which can only go to the right in the beginning (can add a specific rule for that

    def HumanMove(self, player, move):
        self.choice_1 = []
        self.choice_2 = []
        self.displayBoard()
        if (len(self.choice_1) == 0):
            print("To move pieces do (ex.): row then col, row then col to move piece at row, col to row, col.")
            for num in range(2):
                if move:
                    i = int(move[0][num]) # if given move, we only want the first grouping here
                    if (i <= 7 and i >= 0):
                        self.choice_1.append(i)
                    else:
                        print("Invalid coordinates.")
                        return
                else:   
                    i = int(input("Which piece? "))
                    if (i <= 7 and i >= 0):
                        self.choice_1.append(i)
                    else:
                        print("Invalid coordinates.")
                        self.HumanMove(player, None)
              
        self.c1_x = self.choice_1[0]
        self.c1_y = self.choice_1[1]

        # If the entered combination is not a piece, return and ask again
        if self.board[self.c1_x][self.c1_y] == None:
            print(f"No piece at {self.c1_x, self.c1_y}.")
            self.HumanMove(player, None)   

        if (len(self.choice_2) == 0):
            for num in range(2):
                if move:
                    n = int(move[1][num]) # should be the second grouping of coordinates here
                    if (n <= 7 and n >= 0):
                        self.choice_2.append(n)
                    else:
                        print("Invalid coordinates.")
                        return
                else:
                    n = int(input("To where? "))
                    if (n <= 7 and n >= 0):
                        self.choice_2.append(n)
                    else:
                        print("Invalid coordinates.")
                        self.HumanMove(player, None)
   
        self.c2_x = self.choice_2[0]
        self.c2_y = self.choice_2[1]
        self.check = True

        # If the destination contains a piece, not allowed to move
        if self.board[self.c2_x][self.c2_y] != None:
            print(f"Can't move to occupied space at {self.c2_x, self.c2_y}.")
            self.HumanMove(player, None)
        self.move(player)
    
    def CPUMove(self, player, move):
        if not move:
            print('No current possible moves. Skipping turn.\n')
            return
        else:
            pass
        # print(move[0][0])
        self.choice_1 = []
        self.choice_2 = []
        self.displayBoard()
        if (len(self.choice_1) == 0):
            for num in range(2):
                i = int(move[0][num]) # if given move, we only want the first grouping here
                if (i <= 7 and i >= 0):
                    self.choice_1.append(i)
                else:
                    print("Invalid coordinates.")
                    return
              
        self.c1_x = self.choice_1[0]
        self.c1_y = self.choice_1[1]

        # If the entered combination is not a piece, return and ask again
        if isinstance(self.board[self.c1_x][self.c1_y], piece.Piece) == False:
            print(f"No piece at {self.c1_x, self.c1_y}.")
            self.CPUMove(player)  
        
        if (len(self.choice_2) == 0):
            for num in range(2):
                n = int(move[1][num]) # should be the second grouping of coordinates here
                if (n <= 7 and n >= 0):
                    self.choice_2.append(n)
                else:
                    print("Invalid coordinates.")
                    return
   
        self.c2_x = self.choice_2[0]
        self.c2_y = self.choice_2[1]
        self.check = True
        # If the destination contains a piece, not allowed to move
        if isinstance(self.board[self.c2_x][self.c2_y], piece.Piece) == True:
            print(f"Can't move to occupied space at {self.c2_x, self.c2_y}.")
            return
        self.move(player)

    def move(self, player):

        self.diff_x = self.c1_x - self.c2_x
        self.diff_y = self.c1_y - self.c2_y
        # ensuring that the players are only accessing pieces of their own Color
        if self.board[self.c1_x][self.c1_y] != None:
            node = self.board[self.c1_x][self.c1_y]
            if player.getColor() == 'r' and (node.getColor() == 'r' or node.getColor() == 'R'):
                pass
            elif player.getColor() == 'w' and  (node.getColor() == 'w' or node.getColor() == 'W'):            
                pass
            else:
                print(f"Incorrect piece choice. Color, {node.getColor()}, does not match {player.getName()}'s set Color, {player.getColor()}.")
                # self.move(player)
                return

        # dealing with the first choice values (r and w pieces seperately)
        # king functionality to be added (should be allowed to go backwards unlike pawn)

        # decide to be king, if their destination equals the first c1_x (0) or the last c1_x (7), and the move is valid
        # change their type to be king (which will have altered movement)

        for row in range(8):
            for col in range(8):
                if (self.board[self.c1_x][self.c1_y] != None):
                    self.s = self.board[self.c1_x][self.c1_y]
                    if (self.s != None):
                        if (self.s.getType() == "pawn"):
                            # different rules for each Color (not being able to go anywhere but horizontal)
                            if (self.s.getColor() == 'r'):
                                # dealing with left corner specific case with red pieces
                                # red pieces going upwards should only have a diff of x being: 1, and y being negative 1 or 1
                                if ((self.c1_x == 7 and self.c1_y == 0)):
                                    # dealing with not allowing weird 'moves' in the first step
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1)):
                                        print("Invalid move for red piece.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for red piece.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # dealing with left corner specific case with red pieces
                                if (self.c1_x == 5 and self.c1_y == 0):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) or
                                        (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y + 1)):
                                        print(f"Invalid move for red piece trying to go anywhere but {self.c1_x + 1, self.c1_y + 1}, (diagonally).")
                                        return
                                    if (((self.diff_x == -1) and (self.diff_y == -1 or self.diff_y == 1)) or 
                                    ((self.diff_x == 1 or self.diff_x == 1) and (self.diff_y == -1 or self.diff_y == -1)) or ((self.diff_x != 1 or
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print(f"Invalid move for red piece. Something to do with {self.diff_x, self.diff_y}.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # dealing with right corner specific case with red pieces
                                if (self.c1_x == 6 and self.c1_y == 7):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) or
                                        (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y - 1)):
                                        print("Invalid move for red piece.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for red piece.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # all other cases for red pieces
                                if (self.c1_x == row and self.c1_y == col):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) or
                                        (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y - 1) or
                                        (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y + 1) or (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y - 1)
                                        or (self.c2_x == self.c1_x - 2 and self.c2_y == self.c1_y + 1) or (self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y + 2)):
                                        print("Invalid move for red piece.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for red piece.")
                                                return
                                    if (self.c2_x == 0):
                                        self.s.isKing()
                                        # print(f'someone became a king {self.s.getType()}')
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]

                            if (self.s.getColor() == 'w'):
                                # dealing with right corner specific case with white pieces
                                if (((self.c1_x == 0 and self.c1_y == 7))):
                                    if ((self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y - 1)):
                                        print("Invalid move for white piece. trying to move to the direct right or directly down.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print(f"Invalid move for white piece. Something to do with, diff x: {self.diff_x}, diff y: {self.diff_y}.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # dealing with right corner specific case with white pieces
                                if ((self.c1_x == 2 and self.c1_y == 7)):
                                    if (self.c2_x != self.c1_x + 1 and self.c2_y != self.c1_y - 1):
                                        print(f"Invalid move for white piece. Something to do with, ({self.c2_x}, {self.c2_y}).")
                                        return
                                    else:
                                        pass
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0) and (self.diff_y % 2 != 0) or (self.diff_x % 2 == 0) and (self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0) and (self.diff_y % 2 == 0)):
                                                print(f"Invalid move for white piece. Something to do with, diff x: {self.diff_x}, diff y: {self.diff_y}.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # dealing with left corner specific case with white pieces
                                if ((self.c1_x == 1) and (self.c1_y == 0)):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) or
                                        (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y + 1)):
                                        print(f"Invalid move for white piece. Something to do with, ({self.c2_x}, {self.c2_y}).")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or
                                    self.diff_x == 1) and (self.diff_y == 1 or  self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print(f"Invalid move for white piece. Something to do with, diff x: {self.diff_x}, diff y: {self.diff_y}.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # handle all other cases with white pieces
                                if (self.c1_x == row and self.c1_y == col):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) or
                                        (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y - 1) or
                                        (self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y - 1) or (self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y + 1)
                                        or (self.c2_x == self.c1_x - 2 and self.c2_y == self.c1_y + 1) or (self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y + 2)):
                                        print(f"Invalid move for white piece. Something to do with, ({self.c2_x}, {self.c2_y}).")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print(f"Invalid move for white piece. Something to do with, diff x: {self.diff_x}, diff y: {self.diff_y}.")
                                                return
                                    if (self.c2_x == 7):
                                        self.s.isKing()
                                        # print(f'someone became a king {self.s.getType()}')
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                        if (self.s.getType() == "king"):
                            if (self.s.getColor() == 'R'):
                                # dealing with left corner specific case with red king piece
                                if (((self.c1_x == 7 and self.c1_y == 0))):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1)):
                                        print("Invalid move for red king.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for red king.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # dealing with left corner specific case with red king piece
                                if ((self.c1_x == 5 and self.c1_y == 0)):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) 
                                        or (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y)):
                                        print("Invalid move for red king.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for red king.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # dealing with right corner specific case with red king piece
                                if ((self.c1_x == 6 and self.c1_y == 7)):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) 
                                        or (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y)):
                                        print("Invalid move for red king.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for red king.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # deal with all other cases with red king piece
                                if (self.c1_x == row and self.c1_y == col):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) or
                                        (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y - 1)
                                        or (self.c2_x == self.c1_x - 2 and self.c2_y == self.c1_y + 1) or (self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y + 2)):
                                        print("Invalid move for red king.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for red king.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]

                            if (self.s.getColor() == 'W'):
                                # dealing with right corner specific case with white king piece
                                if (((self.c1_x == 0 and self.c1_y == 7))):
                                    if ((self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y - 1)):
                                        print('Invalid move for white king.')
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for white king.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # dealing with right corner specific case with white king piece
                                if ((self.c1_x == 2 and self.c1_y == 7)):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) 
                                        or (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y)):
                                        print("Invalid move for white king.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for white king.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # dealing with left corner specific case with white king piece
                                if ((self.c1_x == 1 and self.c1_y == 0)):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) 
                                        or (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y)):
                                        print("Invalid move for white king.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for white king.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
                                # deal with all other cases with white king piece
                                if (self.c1_x == row and self.c1_y == col):
                                    if ((self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y + 1) or
                                        (self.c2_x == self.c1_x + 1 and self.c2_y == self.c1_y) or (self.c2_x == self.c1_x and self.c2_y == self.c1_y - 1)
                                        or (self.c2_x == self.c1_x - 2 and self.c2_y == self.c1_y + 1) or (self.c2_x == self.c1_x - 1 and self.c2_y == self.c1_y + 2)):
                                        print("Invalid move for white king.")
                                        return
                                    if (((self.diff_x != 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y != -1)) or 
                                    ((self.diff_x == 1 or self.diff_x != -1) and (self.diff_y != 1 or self.diff_y == -1)) or ((self.diff_x != 1 or 
                                    self.diff_x == 1) and (self.diff_y == 1 or self.diff_y != -1))):
                                        if ((self.diff_x < -1 or self.diff_x > 1) and (self.diff_y < -1 or self.diff_y > 1)):
                                            if ((self.diff_x % 2 != 0 and self.diff_y % 2 != 0) or (self.diff_x % 2 == 0 and self.diff_y % 2 != 0) or
                                            (self.diff_x % 2 != 0 and self.diff_y % 2 == 0)):
                                                print("Invalid move for white king.")
                                                return
                                    else:
                                        pass
                                else:
                                    self.temp = self.board[self.c1_x][self.c1_y]
        # dealing with the second choice values (r and w pieces seperately)

        # eepy so im gonna write ideas

        # i think the idea is sound, of checking if an instance exists between a point and the end
        # (i'll have to adjust it slightly for a double move)
        # should check for one if the Color is not the same (meaning a king or a pawn)
        # if the Color is the same, then don't do anything, pass onto the swap as usual
        # then if its the other case, we can check (from statement in 270)

        # could make this part a seperate method that gets called at the end of move
        # takes in, the piece, diff_x, y, and player

        for row in range(8):
            for col in range(8):
                # currently processing only one move (i.e. a piece existing between a move of '2' spaces)
                # i think i need to do cases for each possible pairing of differences
                # (i.e., (2, 2), (-2, 2), (2, -2), (-2, -2))

                # for kings
                # checking down to the right is (-2, 2)
                # checking down to the left is (-2, -2)
                # checking up to the left is (2, 2)
                # checking up to the right is (2, -2)

                # for red piece
                # checking up to the left is (2, 2)
                # checking up to the right is (2, -2)

                # for white piece
                # checking down to the left is (-2, -2)
                # checking down to the right is ((-2, 2))

                # Single move Implementation
                if (self.s != None):
                    # (2, 2) difference in coordinates case 
                    if ((self.diff_x == 2 and self.diff_y == 2)):
                        # print(f"2, 2 case")
                        # print(f"x is: {self.diff_x}, y is {self.diff_y}. ")
                        # red piece case for (2, 2)
                        if ((self.s.getType() == "pawn")):
                            if ((self.s.getColor() == 'r')):
                                # checking if piece exists in left upper
                                if self.c2_x + 1 <= 7 and self.c2_y + 1 <= 7:
                                    if self.board[self.c2_x + 1][self.c2_y + 1] != None:
                                        self.p = self.board[self.c2_x + 1][self.c2_y + 1]
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                print("move! Captured white piece.")
                                                self.check = False
                                # if a piece does not exist on the spot before the move, not allowed
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return

                        # can go backwards and forwards
                        if ((self.s.getType() == "king")):
                            if ((self.s.getColor() == 'R')):
                                # checking if piece exists in left upper
                                if self.c2_x + 1 <= 7 and self.c2_y + 1 <= 7:
                                    if self.board[self.c2_x + 1][self.c2_y + 1] != None:
                                        self.p = self.board[self.c2_x + 1][self.c2_y + 1]  
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                if (self.p.getColor() == 'w' or self.p.getColor() == 'W'):
                                                    print("move! Captured white piece.")
                                                    self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                            if ((self.s.getColor() == 'W')):
                                # checking if piece exists in left upper
                                if self.c2_x + 1 <= 7 and self.c2_y + 1 <= 7:
                                    if self.board[self.c2_x + 1][self.c2_y + 1] != None:
                                        self.p = self.board[self.c2_x + 1][self.c2_y + 1]  
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                if (self.p.getColor() == 'r' or self.p.getColor() == 'r'):
                                                    print("move! Captured red piece.")
                                                    self.check = False
                                    else:
                                        print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                        # self.move(player)
                                        return
                            
                    # (-2, -2) difference in coordinates case
                    if ((self.diff_x == -2 and self.diff_y == -2)):
                        # print(f"-2, -2 case")
                        # print(f"x is: {self.diff_x}, y is {self.diff_y}. ")
                        # white piece case for (-2, -2)
                        if (self.s.getType() == "pawn"):
                            if ((self.s.getColor() == 'w')):
                                # checking if piece exists in left upper
                                if self.c2_x - 1 >= 0 and self.c2_y - 1 >= 0:
                                    if self.board[self.c2_x - 1][self.c2_y - 1] != None:
                                        self.p = self.board[self.c2_x - 1][self.c2_y - 1] 
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                print("move! Captured red piece.")
                                                self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                        # can go backwards and forwards
                        if ((self.s.getType() == "king")):
                            if ((self.s.getColor() == 'R')):
                                # checking if piece exists in left upper
                                if self.c2_x - 1 >= 0 and self.c2_y - 1 >= 0:
                                    if self.board[self.c2_x - 1][self.c2_y - 1] != None:
                                        self.p = self.board[self.c2_x - 1][self.c2_y - 1]  
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                if (self.p.getColor() == 'w' or self.p.getColor() == 'W'):
                                                    print("move! Captured white piece.")
                                                    self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                            if ((self.s.getColor() == 'W')):
                                # checking if piece exists in left upper
                                if self.c2_x - 1 >= 0 and self.c2_y - 1 >= 0:
                                    if self.board[self.c2_x - 1][self.c2_y - 1] != None:
                                        self.p = self.board[self.c2_x - 1][self.c2_y - 1]  
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                if (self.p.getColor() == 'r' or self.p.getColor() == 'r'):
                                                    print("move! Captured red piece.")
                                                    self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return

                    # (2, -2) difference in coordinates case
                    if ((self.diff_x == 2 and self.diff_y == -2)):
                        # print(f"2, -2 case")
                        # checking if piece exists in right upper
                        if ((self.s.getType() == "pawn")):
                            if ((self.s.getColor() == 'r')):
                                if self.c2_x + 1 <= 7 and self.c2_y - 1 >= 0:
                                    if self.board[self.c2_x + 1][self.c2_y - 1] != None:
                                        self.p = self.board[self.c2_x + 1][self.c2_y - 1]
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                print("move! Captured white piece.")
                                                self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                        if ((self.s.getType() == "king")):
                            if ((self.s.getColor() == 'R')):
                                # checking if piece exists in left upper
                                if self.c2_x + 1 <= 7 and self.c2_y - 1 >= 0:
                                    if self.board[self.c2_x + 1][self.c2_y - 1] != None:
                                        self.p = self.board[self.c2_x + 1][self.c2_y - 1]  
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                if (self.p.getColor() == 'w' or self.p.getColor() == 'W'):
                                                    print("move! Captured white piece.")
                                                    self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                            if ((self.s.getColor() == 'W')):
                                # checking if piece exists in left upper
                                if self.c2_x + 1 <= 7 and self.c2_y - 1 >= 0:
                                    if self.board[self.c2_x + 1][self.c2_y - 1] != None:
                                        self.p = self.board[self.c2_x + 1][self.c2_y - 1]  
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                if (self.p.getColor() == 'r' or self.p.getColor() == 'r'):
                                                    print("move! Captured red piece.")
                                                    self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                    # (2, 2) difference in coordinates case
                    if ((self.diff_x == -2 and self.diff_y == 2)):
                        # print(f"-2, 2 case")
                        # print(f"x is: {self.diff_x}, y is {self.diff_y}. ")
                        # checking if piece exists in right lower
                        if ((self.s.getType() == "pawn")):
                            if ((self.s.getColor() == 'w')):
                                if self.c2_x - 1 >= 0 and self.c2_y + 1 <= 7:
                                    if self.board[self.c2_x - 1][self.c2_y + 1] != None:
                                        self.p = self.board[self.c2_x - 1][self.c2_y + 1]
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                print("move! Captured red piece.")
                                                self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                        if ((self.s.getType() == "king")):
                            if ((self.s.getColor() == 'R')):
                                # checking if piece exists in right lower
                                if self.c2_x - 1 >= 0 and self.c2_y + 1 <= 7:
                                    if self.board[self.c2_x - 1][self.c2_y + 1] != None:
                                        self.p = self.board[self.c2_x - 1][self.c2_y + 1]  
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                if (self.p.getColor() == 'w' or self.p.getColor() == 'W'):
                                                    print("move! Captured white piece.")
                                                    self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                            if ((self.s.getColor() == 'W')):
                                # checking if piece exists in right lower
                                if self.c2_x - 1 >= 0 and self.c2_y + 1 <= 7:
                                    if self.board[self.c2_x - 1][self.c2_y + 1] != None:
                                        self.p = self.board[self.c2_x - 1][self.c2_y + 1]  
                                        if (self.p.getColor() == self.s.getColor()):
                                            print("Invalid move. Can't move over own pieces.")
                                            return
                                        else:
                                            self.p.setChecked()
                                            if (self.check):
                                                if (self.p.getColor() == 'r' or self.p.getColor() == 'r'):
                                                    print("move! Captured red piece.")
                                                    self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                    # performing swap for a single space
                    if (self.c2_x == row and self.c2_y == col):
                        # print("Performing swap for move.")
                        self.board[self.c2_x][self.c2_y] = self.temp
                        # print(f"End piece is now {self.board[self.c2_x][self.c2_y]}.")
                        self.board[self.c1_x][self.c1_y] = None
                        # print(f"(Expecting None) Start piece is now {self.board[self.c1_x][self.c1_y]}.")

                    # Double move Implementation

                    # i think this will process if its a double move (so copy most of the code but also having to keep track
                    # of both pieces in between the start point and end point) (can do another if statement with the instance of check)
                    # i think i need to do cases for each possible pairing of differences
                    # (i.e., (4, 4), (-4, 4), (4, -4), (-4, -4))

                    # i was wrong, because of the possibility of the end being the same col/row i have to account for that too
                    # example, if there is a red piece at 3, 4 and 5, 4, a white piece could double move to get both
                    # if it was at say, 2, 5, it would move first to 4, 3, then to 6, 5 (technically, if reality the player would just put the end
                    # coordinate and i need to do the calculations to also count both pieces in the path)
                    # the difference in those the x and y would be 2 - 6, 5 - 5 = -4, 0 (for pieces going down to the right)
                    # after more testing, i think it's always going to be a difference of -4, 0 for double moves going down (white pieces initially)
                    # for red pieces going up,
                    # piece at 5, 2, moves to 1, 2 with 2 white pieces at 4,1 and 2,1
                    # results: 5 - 1, 2, 2 = 4, 0

                    # (4, 0) difference in coordinates case 

                    # red piece
                    if ((self.diff_x == 4 and self.diff_y == 0)): # sideway double jump up (left or right)
                        if ((self.s.getType() == "pawn")):
                            if ((self.s.getColor() == 'r')):
                                if self.c2_x + 3 <= 7 and self.c2_y - 2 >= 0:
                                    if self.board[self.c2_x + 1][self.c2_y - 1] != None:
                                        self.p2 = self.board[self.c2_x + 1][self.c2_y - 1]
                                        if self.board[self.c2_x + 2][self.c2_y - 2] == None:
                                            if self.board[self.c2_x + 3][self.c2_y - 1] != None:
                                                self.p = self.board[self.c2_x + 3][self.c2_y - 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else: 
                                                    self.p.setChecked()                                          
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        print("Double move! Captured 2 white pieces.")
                                                        self.check = False
                                if self.c2_x + 3 <= 7 and self.c2_y + 2 <= 7:
                                    if self.board[self.c2_x + 1][self.c2_y + 1] != None:
                                        self.p2 = self.board[self.c2_x + 1][self.c2_y + 1]
                                        if self.board[self.c2_x + 2][self.c2_y + 2] == None:
                                            if self.board[self.c2_x + 3][self.c2_y + 1] != None:
                                                self.p = self.board[self.c2_x + 3][self.c2_y + 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else: 
                                                    self.p.setChecked()                                          
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        print("Double move! Captured 2 white pieces.")
                                                        self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return

                        # kings
                        if ((self.s.getType() == "king")):
                            if ((self.s.getColor() == 'R')):
                                # Double jump up to the left
                                if self.c2_x + 3 <= 7 and self.c2_y - 2 <= 7:
                                    if self.board[self.c2_x + 1][self.c2_y - 1] != None: # sideway double jump up (left or right)
                                        self.p2 = self.board[self.c2_x + 1][self.c2_y - 1] 
                                        if self.board[self.c2_x + 2][self.c2_y - 2] == None:
                                            if self.board[self.c2_x + 3][self.c2_y - 1] != None:
                                                self.p = self.board[self.c2_x + 3][self.c2_y - 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else:
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        if ((self.p2.getColor() == 'W' or self.p.getColor() == 'w') 
                                                            and (self.p2.getColor() == 'w' or self.p.getColor() == 'W')):
                                                            print("Double move! Captured 2 white pieces.")
                                                            self.check = False
                                # Double jump up to the right
                                if self.c2_x + 3 <= 7 and self.c2_y + 2 <= 7:
                                    if self.board[self.c2_x + 1][self.c2_y + 1] != None:
                                        self.p2 = self.board[self.c2_x + 1][self.c2_y + 1]
                                        if self.board[self.c2_x + 2][self.c2_y + 2] == None:
                                            if self.board[self.c2_x + 3][self.c2_y + 1] != None:
                                                self.p = self.board[self.c2_x + 3][self.c2_y + 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else: 
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        if ((self.p2.getColor() == 'W' or self.p.getColor() == 'w') 
                                                            and (self.p2.getColor() == 'w' or self.p.getColor() == 'W')):
                                                            print("Double move! Captured 2 white pieces.")
                                                            self.check = False
                            else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                            if ((self.s.getColor() == 'W')):
                                if self.c2_x + 3 <= 7 and self.c2_y - 2 <= 7:
                                    if self.board[self.c2_x + 1][self.c2_y - 1] != None: # sideway double jump up (left or right)
                                        self.p2 = self.board[self.c2_x + 1][self.c2_y - 1] 
                                        if self.board[self.c2_x + 2][self.c2_y - 2] == None:
                                            if self.board[self.c2_x + 3][self.c2_y - 1] != None:
                                                self.p = self.board[self.c2_x + 3][self.c2_y - 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else:
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        if ((self.p2.getColor() == 'r' or self.p.getColor() == 'R') 
                                                            and (self.p2.getColor() == 'R' or self.p.getColor() == 'r')):
                                                            print("Double move! Captured 2 red pieces.")
                                                            self.check = False
                                if self.c2_x + 3 <= 7 and self.c2_y + 2 <= 7:
                                    if self.board[self.c2_x + 1][self.c2_y + 1] != None:
                                        self.p2 = self.board[self.c2_x + 1][self.c2_y + 1]
                                        if self.board[self.c2_x + 2][self.c2_y + 2] == None:
                                            if self.board[self.c2_x + 3][self.c2_y + 1] != None:
                                                self.p = self.board[self.c2_x + 3][self.c2_y + 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else: 
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        if ((self.p2.getColor() == 'W' or self.p.getColor() == 'w') 
                                                            and (self.p2.getColor() == 'w' or self.p.getColor() == 'W')):
                                                            print("Double move! Captured 2 white pieces.")
                                                            self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                    # (-4, 0) difference in coordinates case

                    # white pieces
                    
                    if ((self.diff_x == 4 and self.diff_y == 0)):
                        if ((self.s.getType() == "pawn")):
                            if ((self.s.getColor() == 'w')):
                                # Double jump down to the right
                                if self.c2_x - 3 >= 0 and self.c2_y - 2 >= 0:
                                    if self.board[self.c2_x - 1][self.c2_y - 1] != None:
                                        self.p2 = self.board[self.c2_x - 1][self.c2_y - 1]
                                        if self.board[self.c2_x - 2][self.c2_y - 2] == None:
                                            if self.board[self.c2_x - 3][self.c2_y - 1] != None:
                                                self.p = self.board[self.c2_x - 3][self.c2_y - 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else: 
                                                    self.p.setChecked()                                          
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        print("Double move! Captured 2 red pieces.")
                                                        self.check = False
                                # Double jump down to the left
                                if self.c2_x - 3 >= 0 and self.c2_y + 2 <= 7:
                                    if self.board[self.c2_x - 1][self.c2_y + 1] != None:
                                        self.p2 = self.board[self.c2_x - 1][self.c2_y + 1]
                                        if self.board[self.c2_x - 2][self.c2_y + 2] == None:
                                            if self.board[self.c2_x - 3][self.c2_y + 1] != None:
                                                self.p = self.board[self.c2_x - 3][self.c2_y + 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else: 
                                                    self.p.setChecked()                                          
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        print("Double move! Captured 2 red pieces.")
                                                        self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return

                        # kings

                        if ((self.s.getType() == "king")):
                            if ((self.s.getColor() == 'R')):
                                # Double jump down to the right
                                if self.c2_x - 3 >= 0 and self.c2_y - 2 >= 0:
                                    if self.board[self.c2_x - 1][self.c2_y - 1] != None:
                                        self.p2 = self.board[self.c2_x - 1][self.c2_y - 1]
                                        if self.board[self.c2_x - 2][self.c2_y - 2] == None:
                                            if self.board[self.c2_x - 3][self.c2_y - 1] != None:
                                                self.p = self.board[self.c2_x - 3][self.c2_y - 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else:
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        if ((self.p2.getColor() == 'W' or self.p.getColor() == 'w') 
                                                            and (self.p2.getColor() == 'w' or self.p.getColor() == 'W')):
                                                            print("Double move! Captured 2 white pieces.")
                                                            self.check = False
                                # Double jump down to the left
                                if self.c2_x - 3 >= 0 and self.c2_y + 2 <= 7:
                                    if self.board[self.c2_x - 1][self.c2_y + 1] != None:
                                        self.p2 = self.board[self.c2_x - 1][self.c2_y + 1]
                                        if self.board[self.c2_x - 2][self.c2_y + 2] == None:
                                            if self.board[self.c2_x - 3][self.c2_y + 1] != None:
                                                self.p = self.board[self.c2_x - 3][self.c2_y + 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else: 
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        if ((self.p2.getColor() == 'W' or self.p.getColor() == 'w') 
                                                            and (self.p2.getColor() == 'w' or self.p.getColor() == 'W')):
                                                            print("Double move! Captured 2 white pieces.")
                                                            self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                            if ((self.s.getColor() == 'W')):
                                 # Double jump down to the right
                                if self.c2_x - 3 >= 0 and self.c2_y - 2 >= 0:
                                    if self.board[self.c2_x - 1][self.c2_y - 1] != None:
                                        self.p2 = self.board[self.c2_x - 1][self.c2_y - 1]
                                        if self.board[self.c2_x - 2][self.c2_y - 2] == None:
                                            if self.board[self.c2_x - 3][self.c2_y - 1] != None:
                                                self.p = self.board[self.c2_x - 3][self.c2_y - 1]
                                            if ((self.p != None and self.p2 != None and self.s != None)):
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else:
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        if ((self.p2.getColor() == 'r' or self.p.getColor() == 'R') 
                                                            and (self.p2.getColor() == 'R' or self.p.getColor() == 'r')):
                                                            print("Double move! Captured 2 red pieces.")
                                                            self.check = False
                                # Double jump down to the left
                                if self.c2_x - 3 >= 0 and self.c2_y + 2 <= 7:
                                    if self.board[self.c2_x - 1][self.c2_y + 1] != None:
                                        self.p2 = self.board[self.c2_x - 1][self.c2_y + 1]
                                        if self.board[self.c2_x - 2][self.c2_y + 2] == None:
                                            if self.board[self.c2_x - 3][self.c2_y + 1] != None:
                                                self.p = self.board[self.c2_x - 3][self.c2_y + 1]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else: 
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        if ((self.p2.getColor() == 'r' or self.p.getColor() == 'R') 
                                                            and (self.p2.getColor() == 'R' or self.p.getColor() == 'r')):
                                                            print("Double move! Captured 2 red pieces.")
                                                            self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                    # didn't think of other positions (which would be 0, _)

                    # so probably (0, 4)

                    # (0, -4)
                    
                    # (4, 4) difference in coordinates case
                    if ((self.diff_x == 4 and self.diff_y == 4)):
                        # print(f"4, 4 case")
                        # red piece case for (4, 4)
                        if ((self.s.getType() == "pawn")):
                            if ((self.s.getColor() == 'r')):
                                # checking if piece exists in left upper (ensuring its only a white piece to perform a move)
                                if (self.c2_x + 3 <= 7 and self.c2_y + 3 <= 7):
                                    if self.board[self.c2_x + 1][self.c2_y + 1] != None:
                                        self.p2 = self.board[self.c2_x + 1][self.c2_y + 1]
                                        if self.board[self.c2_x + 2][self.c2_y + 2] == None:
                                            if self.board[self.c2_x + 3][self.c2_y + 3] != None:
                                                self.p = self.board[self.c2_x + 3][self.c2_y + 3]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else: 
                                                    self.p.setChecked()                                          
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        print("Double move! Captured 2 white pieces.")
                                                        self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                        # can go backwards and forwards
                        if ((self.s.getType() == "king")):
                            if ((self.s.getColor() == 'R' or self.s.getColor() == 'W')):
                                # checking if piece exists in left upper
                                if (self.c2_x + 3 <= 7 and self.c2_y + 3 <= 7):
                                    if self.board[self.c2_x + 1][self.c2_y + 1] != None:
                                        self.p2 = self.board[self.c2_x + 1][self.c2_y + 1]
                                        if self.board[self.c2_x + 2][self.c2_y + 2] == None:
                                            if self.board[self.c2_x + 3][self.c2_y + 3] != None:
                                                self.p = self.board[self.c2_x + 3][self.c2_y + 3]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else:
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        if (self.s.getColor() == 'R'):
                                                            print("Double move! Captured 2 white pieces.")
                                                            self.check = False
                                                        if (self.s.getColor() == 'W'):
                                                            print("Double move! Captured 2 red pieces.")
                                                            self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                    # (-4, -4) difference in coordinates case
                    if ((self.diff_x == -4 and self.diff_y == -4)):
                        # print(f"-4, -4 case")
                        if ((self.s.getType() == "pawn")):
                            if ((self.s.getColor() == 'w')):
                                # checking if piece exists in left lower
                                if (self.c2_x - 3 >= 0 and self.c2_y - 3 >= 0):
                                    if self.board[self.c2_x - 1][self.c2_y - 1] != None:
                                        self.p2 = self.board[self.c2_x - 1][self.c2_y - 1]
                                        if self.board[self.c2_x - 2][self.c2_y - 2] == None:
                                            if self.board[self.c2_x - 3][self.c2_y - 3] != None:
                                                self.p = self.board[self.c2_x - 3][self.c2_y - 3]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else:
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        print("Double move! Captured 2 white pieces.")
                                                        self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                        # can go backwards and forwards
                        if ((self.s.getType() == "king")):
                            if ((self.s.getColor() == 'R' or self.s.getColor() == 'W')):
                                # checking if piece exists in left lower
                                if (self.c2_x - 3 >= 0 and self.c2_y - 3 >= 0):
                                    if self.board[self.c2_x - 1][self.c2_y - 1] != None:
                                        self.p2 = self.board[self.c2_x - 1][self.c2_y - 1]
                                        if self.board[self.c2_x - 2][self.c2_y - 2] == None:
                                            if self.board[self.c2_x - 3][self.c2_y - 3] != None:
                                                self.p = self.board[self.c2_x - 3][self.c2_y - 3]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                            else: 
                                                self.p.setChecked()
                                                self.p2.setChecked()
                                                if (self.check):
                                                    if (self.s.getColor() == 'R'):
                                                        print("Double move! Captured 2 white pieces.")
                                                        self.check = False
                                                    if (self.s.getColor() == 'W'):
                                                        print("Double move! Captured 2 red pieces.")
                                                        self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                    # (4, -4) difference in coordinates case
                    if ((self.diff_x == 4 and self.diff_y == -4)):
                        # print(f"4, -4 case")
                        if ((self.s.getType() == "pawn")):
                            if ((self.s.getColor() == 'r')):
                            # checking if piece exists in right upper
                                if (self.c2_x + 3 <= 7 and self.c2_y - 3 >= 0):
                                    if self.board[self.c2_x + 1][self.c2_y - 1] != None:
                                        self.p2 = self.board[self.c2_x + 1][self.c2_y - 1]
                                        if self.board[self.c2_x + 2][self.c2_y - 2] == None:
                                            if self.board[self.c2_x + 3][self.c2_y - 1] != None:
                                                self.p = self.board[self.c2_x + 3][self.c2_y - 3]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else:
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        print("Double move! Captured 2 white pieces.")
                                                        self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                        # can go backwards and forwards
                        if ((self.s.getType() == "king")):
                            if ((self.s.getColor() == 'R' or self.s.getColor() == 'W')):
                                # checking if piece exists in right upper
                                if (self.c2_x + 3 <= 7 and self.c2_y - 3 >= 0):
                                    if self.board[self.c2_x + 1][self.c2_y - 1] != None:
                                        self.p2 = self.board[self.c2_x + 1][self.c2_y - 1]
                                        if self.board[self.c2_x + 2][self.c2_y - 2] == None:
                                            if self.board[self.c2_x + 3][self.c2_y - 1] != None:
                                                self.p = self.board[self.c2_x + 3][self.c2_y - 3]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                            else:
                                                self.p2.setChecked()
                                                self.p.setChecked()
                                                if (self.check):
                                                    if (self.s.getColor() == 'R'):
                                                        print("Double move! Captured 2 white pieces.")
                                                        self.check = False
                                                    if (self.s.getColor() == 'W'):
                                                        print("Double move! Captured 2 red pieces.")
                                                        self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                    # (-4, 4) difference in coordinates case
                    if((self.diff_x == -4 and self.diff_y == 4)):
                        # print(f"-4, 4 case")
                        if ((self.s.getType() == "pawn")):
                            if ((self.s.getColor() == 'w')):
                            # checking if piece exists in right lower
                                if (self.c2_x - 3 >= 0 and self.c2_y + 3 <= 7):
                                    if self.board[self.c2_x - 1][self.c2_y + 1] != None:
                                        self.p2 = self.board[self.c2_x - 1][self.c2_y + 1]
                                        if self.board[self.c2_x - 2][self.c2_y + 2] == None:
                                            if self.board[self.c2_x - 3][self.c2_y + 3] != None:
                                                self.p = self.board[self.c2_x - 3][self.c2_y + 3]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                                else:   
                                                    self.p.setChecked()
                                                    self.p2.setChecked()
                                                    if (self.check):
                                                        print("Double move! Captured 2 white pieces.")
                                                        self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                        # can go backwards and forwards
                        if ((self.s.getType() == "king")):
                            if ((self.s.getColor() == 'R' or self.s.getColor() == 'W')):
                                # checking if piece exists in right lower
                                if (self.c2_x - 3 >= 0 and self.c2_y + 3 <= 7):
                                    if self.board[self.c2_x - 1][self.c2_y + 1] != None:
                                        self.p2 = self.board[self.c2_x - 1][self.c2_y + 1]
                                        if self.board[self.c2_x - 2][self.c2_y + 2] == None:
                                            if self.board[self.c2_x - 3][self.c2_y + 3] != None:
                                                self.p = self.board[self.c2_x - 3][self.c2_y + 3]
                                                if (self.p.getColor() == self.s.getColor() and self.p2.getColor() == self.s.getColor()):
                                                    print("Invalid move. Can't move over own pieces.")
                                                    return
                                            else:
                                                self.p.setChecked()
                                                self.p2.setChecked()
                                                if (self.check):
                                                    if (self.s.getColor() == 'R'):
                                                        print("Double move! Captured 2 white pieces.")
                                                        self.check = False
                                                    if (self.s.getColor() == 'W'):
                                                        print("Double move! Captured 2 red pieces.")
                                                        self.check = False
                                else:
                                    print("Invalid move. Can't move when there are no present pieces. Skipping round.")
                                    # self.move(player)
                                    return
                    # the swap occurs for a double move
                    if (self.c2_x == row and self.c2_y == col):
                        # print("Performing swap for double move.")
                        self.board[self.c2_x][self.c2_y] = self.temp
                        # print(f"End piece is now {self.board[self.c2_x][self.c2_y]}.")
                        self.board[self.c1_x][self.c1_y] = None
                        # print(f"(Expecting None) Start piece is now {self.board[self.c1_x][self.c1_y]}.")
        self.removePiece()

    def undo(self, old_board):
        # how to do undo
        # should not do a shallow copy because that is probably not alterting the values correctly
        self.copyOldBoard(old_board)

    def howManyPieces(self):
        self.r_count = 0
        self.w_count = 0

        for row in self.board:
            for node in row:
                if (node != None):
                    if (node.getColor() == 'R'):
                            self.r_count += 1
                    elif (node.getColor() == 'r'):
                            self.r_count += 1
                    if (node.getColor() == 'W'):
                            self.w_count += 1 
                    elif (node.getColor() == 'w'):
                            self.w_count += 1
        return self.r_count, self.w_count
        
    def removePiece(self):
        for row in range(8):
            for col in range(8):
                node = self.board[row][col]
                if (node != None):
                    # print("is node checked?:", node.isChecked())
                    if (node.isChecked()):
                        # print(f"{node.getType()} got checked.")
                        del node
                        self.board[row][col] = None
                    else:
                        pass
                else:
                    # print('bro got to live.')
                    pass

    # def isEmpty(self, board):
    #     if not board:
    #         return 1
    #     else:
    #         return 0

    # method to copy the data in a given array to another (in our case changing the board)
    # to be used in undo move
    def copyOldBoard(self, old_board):
        # print('i am being copied!!')
        for row in range(8):
            for col in range(8):
                self.board[row][col] = old_board[row][col]
        # self.displayBoard()

    # method to copy arrays
    def copyArray(self, array):
        new_arr = []
        for row in array:
            line = []
            for item in row:
                line.append(item)
            new_arr.append(line)
        return new_arr

    # method to possibly return if game is over since
    # in the aBpruning methods id need to have each board
    # have a seperate method to be able to determine if the board move
    # results in a end game state (which could be good or bad)
    def isGOver(self, player):
        pieces = self.howManyPieces()
        g_overR = pieces[0]
        g_overW = pieces[1]
        if (player.getColor() == 'r'):
            if g_overR == 0:
                return True
        elif (player.getColor() == 'w'):
            if g_overW == 0:
                return True
        else:
            return False
        
    def hFKing(self, player):
        # first = True
        dK = 0
        for row in range(8):
            for col in range(8):
                node = self.board[row][col]
                if node != None:
                    if player.getColor() == 'r':
                        if node.getColor() == 'r':
                            # for red, goal row for kings is 0
                            dK = (0 - row)
                        elif node.getColor() == 'R':
                            dK = (row - 0)
                        else:
                            pass
                    elif player.getColor() == 'w': # assuming its white
                        if node.getColor() == 'w':
                            # for white, goal row for kings is 7
                            dK = (7 - row)
                        elif node.getColor() == 'W':
                             dK = (0 - row)
                        else:
                            pass

        return dK

        
    