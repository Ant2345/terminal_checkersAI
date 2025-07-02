# Class to handle the creation of a player object
# (Planning to use to primarily assist in showcasing captured pieces and such)

import piece, board


class Player():

    def __init__(self, name, color, type):
        self.name = name
        self.p_Color = color
        self.type = type

    def setColor(self, color):
        self.p_Color = color

    def getColor(self):
        return self.p_Color
    
    def getName(self):
        return self.name
    
    def getType(self):
        return self.type