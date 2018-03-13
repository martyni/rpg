import controls
from controls import pygame, log
from sprites import base_sprite, player_sprite, npc_sprite
from text import base_text
from load import levels
npc = base_sprite(50, 50, i=250, j=250)
npc1 = base_sprite(50, 50, i=350, j=12)
npc2 = base_sprite(50, 50, i=20, j=2)
pc = player_sprite(
        40, 
        70, 
        i=250, 
        j=250,
        states={
            "default":
                [ 
                pygame.image.load("assets/images/Iandalara_base0{}.bmp".format(4)).convert_alpha()
                ] * 3 +
                [
                pygame.image.load("assets/images/Iandalara_base0{}.bmp".format(i)).convert_alpha() for i in range(3)
                ],
            "default_up":
                [ 
                pygame.image.load("assets/images/Iandalara_base_up0{}.bmp".format(4)).convert_alpha()
                ] * 3 +
                [
                pygame.image.load("assets/images/Iandalara_base_up0{}.bmp".format(i)).convert_alpha() for i in range(3)
                ],
            "up": [
                pygame.image.load("assets/images/Iandalara_up0{}.bmp".format(i)).convert_alpha() for i in range(4)
                ],
            "down": [
                pygame.image.load("assets/images/Iandalara_down0{}.bmp".format(i)).convert_alpha() for i in range(4)
                ],
            "left": [
                pygame.image.load("assets/images/Iandalara_down0{}.bmp".format(i)).convert_alpha() for i in range(4)
                ],
            "right": [
                pygame.image.load("assets/images/Iandalara_down0{}.bmp".format(i)).convert_alpha() for i in range(4)
                ],
            },

        )
a_text = base_text()
background = base_sprite(**levels['l1'].settings)
level_sprites = [npc_sprite(**child.settings) for child in levels['l1'].children['npc']]
level_sprites.append(pc)        
controls.main(background_layers=[background], sprites=level_sprites, text=a_text)
exit(1)
