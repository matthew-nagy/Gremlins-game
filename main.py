import pygame as py
from pygame.locals import *
py.init()
import ServerClient as net
import level as l
import sprite as s
import player

def runGame():
    window = py.display.set_mode((600,600))
    white_screen_col = py.Color(255, 255, 255)
    fps_controller = py.time.Clock()

    lvl = l.Level('map1.png', 20, (50, 50))

    p = player.Base_Player(300, 300, py.Color(255, 0, 150), window)

    play = True
    while play:
        py.draw.rect(window, white_screen_col, (0,0,600,600))
        lvl.draw(window)
        p.draw()

        py.display.update()
        for event in py.event.get():
            if event.type == QUIT:
                py.quit()
                play = False
                return
        
        player_input = player.Player_Input.generate()

        if py.key.get_pressed()[py.K_9]:
            p.applyMovement(p.getLastInput(), lvl)
        else:
            p.applyMovement(player_input, lvl)
        
        fps_controller.tick(30)


runGame()