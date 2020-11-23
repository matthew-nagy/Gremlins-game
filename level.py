from PIL import Image
import pygame as py
import sprite as s

class Level:
    def __init__(self, levelName, blockSize, startPoint):
        self.image = Image.open(levelName)
        self.size = self.image.size
        self.blockSize = blockSize
        self.startPoint = startPoint

        self.BlackCol = py.Color(0, 0, 0)
        self.BlueCol = py.Color(0, 255, 255)
        self.GreenCol = py.Color(0, 255, 0)


    #returns true if the two colours colours given are the same
    def isColor(self, col, r, g, b):
        return col[0] == r and col[1] == g and col[2] == b
    
    #Draws a rect based off of level data
    def drawRect(self, window, colour, x, y):
        py.draw.rect(window, colour, ((x * self.blockSize) + self.startPoint[0], (y * self.blockSize) + self.startPoint[1], self.blockSize, self.blockSize))

    #Draws the map
    def draw(self, window):
        for y in range(self.size[1]):
            for x in range(self.size[0]):
                pixel = self.image.getpixel((x, y))
                if self.isColor(pixel, 0, 0, 0):
                    self.drawRect(window, self.BlackCol, x, y)
                elif self.isColor(pixel, 0, 255, 255):
                    self.drawRect(window, self.BlueCol, x, y)
                elif self.isColor(pixel, 0, 255, 0):
                    self.drawRect(window, self.GreenCol, x, y)
    
    def isCollision(self, x, y):
        return self.isColor(self.image.getpixel((x / self.blockSize, y / self.blockSize)), 0, 0, 0)
    
    def isGoal(self, x, y):
        return self.isColor(self.image.getpixel((x / self.blockSize, y / self.blockSize)), 0, 255, 0)

  #  def towerSpawnPositions(self):


