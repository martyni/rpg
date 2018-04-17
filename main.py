import controls
from controls import pygame, log
from sprites import base_sprite, player_sprite, npc_sprite, static_sprite
from text import base_text
from load import levels, tiles
from sprite_groups import main_physical_group
pc = player_sprite(
        34, 
        64, 
        i=controls.width/2 - 20,
        j=controls.height/2 - 35,
        states={
            "default":
                [ 
                "assets/images/Iandalara_base0{}.bmp".format(4)
                ] * 3 +
                [
                "assets/images/Iandalara_base0{}.bmp".format(i) for i in range(3)
                ],
            "default_up":
                [ 
                "assets/images/Iandalara_base_up0{}.bmp".format(4)
                ] * 3 +
                [
                "assets/images/Iandalara_base_up0{}.bmp".format(i) for i in range(3)
                ],
            "default_right": [
                "assets/images/Iandalara_right00.bmp"
                ],
            "default_left": [
                "assets/images/Iandalara_left00.bmp"
                ],
            "up": [
                "assets/images/Iandalara_up0{}.bmp".format(i) for i in range(4)
                ],
            "down": [
                "assets/images/Iandalara_down0{}.bmp".format(i) for i in range(4)
                ],
            "left": [
                "assets/images/Iandalara_left0{}.bmp".format(i) for i in range(4)
                ],
            "right": [
                "assets/images/Iandalara_right0{}.bmp".format(i) for i in range(4)
                ],
            },

        )
a_text = base_text()
background = base_sprite(**levels['l1'].settings)
game_tiles = []
for tile in tiles:
   game_tiles.append({
      "width": 32,
      "height": 32,
      "i": 0,
      "j": 0,
      "states":{
         "default": tiles[tile]
      }
   })
level_sprites = [npc_sprite(**child.settings) for child in levels['l1'].children['npc']]
static_sprites = [static_sprite(**child.settings) for child in levels['l1'].children['static']]
level_sprites.append(pc)        
[main_physical_group.add(sprite) for sprite in level_sprites + static_sprites]
controls.main(background_layers=[background], 
   sprites=level_sprites + static_sprites, 
   text=a_text, 
   sprite_groups=[main_physical_group], 
   tiles=game_tiles,
   base_sprite=base_sprite)
exit(1)
