import pygame as py
from pygame.locals import *
py.init()
import ServerClient as net
import level as l
import sprite as s
import player
import pickle


def runGameHost():

    window = py.display.set_mode((600,600))
    white_screen_col = py.Color(255, 255, 255)
    fps_controller = py.time.Clock()

    lvl = l.Level('map1.png', 20, (50, 50))

    clientPlayer = player.Base_Player(300, 300, py.Color(255, 0, 150), window)
    
    hostPlayer = player.Base_Player(350,350, py.Color(0, 255, 0), window)

    connections, names = net.get_connections()
    for i in connections:
        i.send(bytes("START", 'utf-8'))

    play = True

    frame = 0
    
    while play:
        py.draw.rect(window, white_screen_col, (0,0,600,600))
        lvl.draw(window)
        hostPlayer.draw()
        clientPlayer.draw()

        py.display.update()
        for event in py.event.get():
            if event.type == QUIT:
                py.quit()
                play = False
                return
        
        player_input = player.Player_Input.generate(1)

        hostPlayer.apply_movement(player_input, lvl)
        data, addr = connections[0].socket.recvfrom(1024) # buffer size is 1024 bytes
        
        clientMovement = player.Player_Input(data[0], data[1], data[2], data[3], data[4], data[5], data[6])
        clientPlayer.apply_movement(clientMovement, lvl)
        
        frame += 1
        if frame % 30 == 0:
            print(frame)

        fps_controller.tick(30)



def runGameClient():
    window = py.display.set_mode((600,600))
    white_screen_col = py.Color(255, 255, 255)
    fps_controller = py.time.Clock()

    lvl = l.Level('map1.png', 20, (50, 50))

    clientPlayer = player.Base_Player(300, 300, py.Color(255, 0, 150), window)
    hostPlayer = player.Base_Player(350,350, py.Color(0, 255, 0), window)

    host = net.get_host()
    print("Waiting for the host to start the game")
    host.recv(100)

    play = True

    frame = 0
    
    while play:
        py.draw.rect(window, white_screen_col, (0,0,600,600))
        lvl.draw(window)
        hostPlayer.draw()
        clientPlayer.draw()

        py.display.update()
        for event in py.event.get():
            if event.type == QUIT:
                py.quit()
                play = False
                return
        
        player_input = player.Player_Input.generate()

        clientPlayer.apply_movement(player_input, lvl)
        clientPlayer.send_input_to_host(host)
        
        frame += 1
        if frame % 30 == 0:
            print(frame)

        fps_controller.tick(30)


val = input("Host(h) or Client(c):\n\t")
if val == "h":
    runGameHost()
else:
    runGameClient()