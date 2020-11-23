import pygame as py
from pygame.locals import *


#Arguments has window then width then height
def drawRect(x, y, col, arguments):
    py.draw.rect(arguments[0], col, (x, y, arguments[1], arguments[2]))

#Arguments has window then radius
def drawCircle(x, y, col, arguments):
    py.draw.circle(arguments[0], col, (x, y), arguments[1])

class Sprite:
    def __init__(self, spawnPos, drawFunction, drawArguments, colour):
        self.drawFunction = drawFunction
        self.drawArguments = drawArguments
        
        self.setPosition(spawnPos[0], spawnPos[1])
        self.setColour(colour)
    
    def draw(self):
        self.drawFunction(int(self.x), int(self.y), self.colour, self.drawArguments)
    
    def move(self, x, y):
        self.x += x
        self.y += y
    
    def setColour(self, newColour):
        self.colour = newColour

    def setPosition(self, x, y):
        self.x = float(x)
        self.y = float(y)