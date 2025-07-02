# Class to handle pieces in a game of checkers
# Pieces are usually white and red
# Pieces can only move diagonally (on black squares so 1's)
# if a piece is in that path, it's a 'jump', and if another piece lays in that following square
# it is a 'double jump'
# If one piece reads the last row of the opposing side, they become kings
# King's can jump backwards
# Each player has 12 pieces in the beginning

class Piece(object):

    def __init__(self, color, type):
        self.color = color
        self.type = type
        self.checked = False

    def getColor(self):
        return self.color
    
    def getType(self):
        return self.type

    def isKing(self):
        self.type = "king"
        # will change logic in main game
        if self.color == 'r':
            self.color = 'R'
        if self.color == 'w':
            self.color = 'W'
        # print(f'color is now {self.color}')
        # print(f'type is now {self.type}')

    def setChecked(self):
        # print('piece was checked?')
        self.checked = True

    def isChecked(self):
        return self.checked

