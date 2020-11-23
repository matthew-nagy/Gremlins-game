import ServerClient as net
import pygame as py

class state:
    dead = 0
    alive = 1
'''
This is a snapshot of the state of a player in time
They will be sent to and from the server and hosts, with the idea that when a client
recieves positional datum from the server, it can see if its own state matches it. If it doesn't,
a UPD package was lost somewhere, and the client corrects itself to match the server, propagating the change up
'''
class Positional_Data:
    def __init__(self, x, y, rotation, state):
        self.x = float(x)
        self.y = float(y)
        self.rotation = int(rotation)
        self.state = int(state)
        self.frameOn = 0

    def __bytes__(self):
        return bytes(self.x, self.y, self.rotation, self.state, self.frameOn)

    def equals(self, otherData):
        if not self.x == otherData.x:
            return False
        elif not self.y == otherData.y:
            return False
        elif not self.rotation == otherData.rotation:
            return False
        elif not self.state == otherData.state:
            return False
        elif not self.frameOn == otherData.frameOn:
            return False
        return True

#Used to store what a players input was on a particular frame
class Player_Input:
    def __init__(self, up, down, left, right, trigger):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.trigger = trigger

class Player:
    def __init__(self, x, y):
        self.predictions = []
        self.inputs = []
        self.currentPosition = Positional_Data(x, y, 0, state.alive)
    
    #sends by UDP because we don't want the entire system to freeze up
    def sendPositionData(self, connection):
        connection.sendto(bytes(self.currentPosition))
