import ServerClient as net
import pygame as py
import level as l
import copy
import sprite
import pickle
import datetime
import datetime

class state:
    dead = 0
    alive = 1

#Used to store what a players input was on a particular frame
class Player_Input:
    def __init__(self, up, down, left, right, rotate_clockwise, rotate_anticlockwise, trigger):
        self.up = up
        self.down = down
        self.left = left
        self.right = right
        self.rotate_clockwise = rotate_clockwise
        self.rotate_anticlockwise = rotate_anticlockwise
        self.trigger = trigger

    def __bytes__(self):
        return bytes([self.up, self.down, self.left, self.right, self.rotate_clockwise, self.rotate_anticlockwise, self.trigger])

    def getAsBytes(self):
        msg = pickle.dumps(self)
        return msg

    @staticmethod
    def generate(mapUse = 0):
        inputs = [False, False, False, False, False, False, False] 
        key_maps = []
        if mapUse == 0:
            key_maps = [py.K_w, py.K_s, py.K_a, py.K_d, py.K_l, py.K_k, py.K_RETURN]
        else:
            key_maps = py.K_UP, py.K_DOWN, py.K_LEFT, py.K_RIGHT, py.K_e, py.K_q, py.K_SPACE
        all_key_pressed_info = py.key.get_pressed()

        count = 0
        for key in key_maps:
            if all_key_pressed_info[key]:
                inputs[count] = True
            count += 1

        return Player_Input(inputs[0], inputs[1], inputs[2], inputs[3], inputs[4], inputs[5], inputs[6])

'''
This is a snapshot of the state of a player in time
They will be sent to and from the server and hosts, with the idea that when a client
recieves positional datum from the server, it can see if its own state matches it. If it doesn't,
a UPD package was lost somewhere, and the client corrects itself to match the server, propagating the change up
'''
class Positional_Data:
    x = 0.0
    y = 0.0
    packX = 0
    packY = 0
    rotation = 0
    state = 0
    timestamp = datetime.datetime.now()

    def __init__(self, x, y, rotation, state):
        self.x = float(x)
        self.y = float(y)
        self.packX = int(x)
        self.packY = int(y)
        self.rotation = int(rotation)
        self.state = int(state)
        self.timestamp =  datetime.datetime.now()

    def equals(self, otherData):
        if not self.x == otherData.x:
            return False
        elif not self.y == otherData.y:
            return False
        elif not self.rotation == otherData.rotation:
            return False
        elif not self.state == otherData.state:
            return False
        elif not self.timestamp == otherData.timestamp:
            return False
        return True

    def apply_movement(self, input, level):
        x_movement = 0
        y_movement = 0
        if input.up:
            y_movement = -1
        elif input.down:
            y_movement = 1
        
        if input.left:
            x_movement = -1
        elif input.right:
            x_movement = 1
        
        if not level.is_collision(self.x + x_movement, self.y):
            self.x += x_movement
        if not level.is_collision(self.x, self.y + y_movement):
            self.y += y_movement
        rotation_speed = 2
        if input.rotate_clockwise: 
            self.rotation += rotation_speed
            if self.rotation > 360:
                self.rotation -= 360
        elif input.rotate_anticlockwise:
            self.rotation -= rotation_speed
            if self.rotation < 0:
                self.rotation += 360
        
        self.packX = int(self.x)
        self.packY = int(self.y)
        #Finally reregister when this happened
        self.timestamp = datetime.datetime.now()

class Player_Network_Information:
    def __init__(self, player_input, player_number):
        self.input = player_input
        self.player_number = player_number
    
    def get_as_pickle_obj(self):
        return pickle.dumps(self)

class Base_Player:
    def __init__(self, x, y, colour, window, player_number):
        self.previous_positions = []#The last few positions it has been in
        self.previous_inputs = []#The last few inputs the player recieved

        self.current_input = Player_Input(0,0,0,0,0,0,0) #The current Input it thinks it has
        self.current_position = Positional_Data(x, y, 0, state.alive)    #Current position
        self.sprite = sprite.Sprite((x,y), sprite.drawCircle, (window, 3), colour)

        self.player_number = player_number
    
    
    def send_to_host(self, connection):
        data = self.get_as_data()
        connection.socket.sendto(data, (connection.IP, connection.port))

    def get_as_data(self):
        return pickle.dumps(self.current_input)#Player_Network_Information(self.current_input, self.player_number).get_as_pickle_obj()

    def respond_to_server_ping(self, truePosition, level):
        if max(truePosition.timestamp, self.current_position.timestamp) == truePosition.timestamp:
            self.adjust_to_future_data(truePosition)
        else:
            self.adjust_to_past_data(truePosition, level)

    #This one is real easy, just TP the player there
    def adjust_to_future_data(self, truePosition):
        self.previous_positions = []
        self.previous_inputs = []
        self.current_position = truePosition

    #This one. This is hard. You need to teleport the player back and then
    #play through their inputs since the past event
    #Don't let them be more than 10 frames ahead
    def adjust_to_past_data(self, truePosition, level):
        trueTime = truePosition.timestamp
        for pos_index in range(len(self.previous_positions)):
            myTime = self.previous_positions[pos_index].timestamp
            #If this timestamp is ahead of the true order of events
            if max(myTime, trueTime) == myTime:
                #found what the server thinks, so lets update off of that

                self.current_position = copy.copy(truePosition)
                #Store old thoughts about positions and inputs
                stored_timestamps = self.previous_positions
                past_past_inputs = self.previous_inputs
                #Now set the actual past to 0, and get ready to rebuild it
                self.previous_positions = []
                self.previous_inputs = []

                for i in range(pos_index + 1, len(stored_timestamps)):
                    self.apply_movement(past_past_inputs[i], level)
                    # Re:Timestamp. Building up a list of timestamps from zero
                    self.current_position.timestamp = stored_timestamps[i].timestamp

                return

    
    def draw(self):
        self.sprite.setPosition(self.current_position.x, self.current_position.y)
        self.sprite.draw()
    
    #If they didn't 
    def get_last_input(self):
        return self.current_input
    
    def apply_movement(self, input, level):
        self.previous_positions.append(copy.copy(self.current_position))
        self.previous_inputs.append(copy.copy(self.current_input))

        self.apply_movement_no_save(input, level)

    def apply_movement_no_save(self, input, level):
        self.current_input = input
        self.current_position.apply_movement(input, level)
