import controls
from controls import pygame, log
from sprites import base_sprite, player_sprite, npc_sprite
from load import levels
npc = base_sprite(50, 50, i=250, j=250)
npc1 = base_sprite(50, 50, i=350, j=12)
npc2 = base_sprite(50, 50, i=20, j=2)
pc = player_sprite(
        50, 
        50, 
        i=250, 
        j=250,
        states={
            "default": [
                pygame.image.load("test.png").convert_alpha(),
                ],
            "up": [
                pygame.image.load("test.png").convert_alpha(),
                pygame.transform.flip(pygame.image.load("test.png").convert_alpha(),1,0)
                ],
            "down": [
                pygame.image.load("test.png").convert_alpha(),
                pygame.transform.flip(pygame.image.load("test.png").convert_alpha(),1,0)
                ],
            "left": [
                pygame.image.load("test.png").convert_alpha(),
                pygame.transform.flip(pygame.image.load("test.png").convert_alpha(),1,0)
                ],
            "right": [
                pygame.image.load("test.png").convert_alpha(),
                pygame.transform.flip(pygame.image.load("test.png").convert_alpha(),1,0)
                ]
            },

        )
background = base_sprite(**levels['l1'].settings)
level_sprites = [npc_sprite(**child.settings) for child in levels['l1'].children['npc']]
level_sprites.append(pc)        
#controls.main(background_layers=[background], sprites=[pc, npc, npc1, npc2])
controls.main(background_layers=[background], sprites=level_sprites)
exit(1)
