import controls
from controls import pygame, log
from sprites import base_sprite, player_sprite, npc_sprite, static_sprite
from text import base_text
from load import levels
from sprite_groups import main_physical_group
pc = player_sprite(
        34*2, 
        64*2, 
        i=controls.width/2 - 20,
        j=controls.height/2 - 35,
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
            "default_right": [
                pygame.image.load("assets/images/Iandalara_right00.bmp").convert_alpha()
                ],
            "default_left": [
                pygame.image.load("assets/images/Iandalara_left00.bmp").convert_alpha()
                ],
            "up": [
                pygame.image.load("assets/images/Iandalara_up0{}.bmp".format(i)).convert_alpha() for i in range(4)
                ],
            "down": [
                pygame.image.load("assets/images/Iandalara_down0{}.bmp".format(i)).convert_alpha() for i in range(4)
                ],
            "left": [
                pygame.image.load("assets/images/Iandalara_left0{}.bmp".format(i)).convert_alpha() for i in range(4)
                ],
            "right": [
                pygame.image.load("assets/images/Iandalara_right0{}.bmp".format(i)).convert_alpha() for i in range(4)
                ],
            },

        )
a_text = base_text()
background = base_sprite(**levels['l1'].settings)
level_sprites = [npc_sprite(**child.settings) for child in levels['l1'].children['npc']]
static_sprites = [static_sprite(**child.settings) for child in levels['l1'].children['static']]
level_sprites.append(pc)        
[main_physical_group.add(sprite) for sprite in level_sprites + static_sprites]
controls.main(background_layers=[background], sprites=level_sprites + static_sprites, text=a_text, sprite_groups=[main_physical_group])
exit(1)
