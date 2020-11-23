import pygame as py
from pygame.locals import *
py.init()
import ServerClient as server
import level as l
import sprite as s

window = py.display.set_mode((600,600))
white_screen_col = py.Color(255, 255, 255)
fps_controller = py.time.Clock()

l = l.Level('map1.png', 20, (50, 50))

spr = s.Sprite((200,200),s.drawRect,(window,5,5), py.Color(255,0,0))

play = True
while play:
    py.draw.rect(window, white_screen_col, (0,0,600,600))
    l.draw(window)
    spr.move(1,1)
    spr.draw()

    py.display.update()
    for event in py.event.get():
        if event.type == QUIT:
            py.quit()
            play = False
    
    fps_controller.tick(30)
