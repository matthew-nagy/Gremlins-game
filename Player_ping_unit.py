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

    fake_position_data = player.Positional_Data(350, 350, 0, player.state.alive)
    fake_position_data.frameOn = 20

    play = True
    frame = 0
    cooloff = 0
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
            p.apply_movement(p.get_last_input(), lvl)
        elif py.key.get_pressed()[py.K_5] and cooloff == 0:
            p.adjust_to_past_data(fake_position_data, lvl)
            fake_position_data = player.copy.copy(fake_position_data)
            fake_position_data.frameOn = frame - 5
            cooloff = 10
        else:
            p.apply_movement(player_input, lvl)
        
        if cooloff > 0:
            cooloff -= 1
        frame+=1
        fps_controller.tick(30)


runGame()