import controls
import yaml
from controls import pygame, log
from sprites import BaseSprite, PlayerSprite, NpcSprite, StaticSprite
from text import BaseText
from load import LEVELS, TILES
from sprite_groups import MAIN_PHYSICAL_GROUP, PC_PHYSICAL_GROUP
pc = PlayerSprite(
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
a_text = BaseText()
background = BaseSprite(**LEVELS['l1'].settings)
with open('level.yml', 'r') as bg_tiles:
    tile_list = yaml.load(bg_tiles.read())
try:
    background_layers = [BaseSprite(**t) for t in tile_list]
except TypeError:
    background_layers = []
for layer in background_layers:
    if "solid" in layer.name:
        MAIN_PHYSICAL_GROUP.add(layer)
    else:
        print layer.name
        print layer.states["default"][0]

game_tiles = []
for tile in TILES:
    game_tiles.append({
        "width": 32,
        "height": 32,
        "i": 0,
        "j": 0,
        "name": tile,
        "states": {
            "default": TILES[tile]
        }
    })
level_sprites = [NpcSprite(**child.settings)
                 for child in LEVELS['l1'].children['npc']]
StaticSprites = [StaticSprite(**child.settings)
                  for child in LEVELS['l1'].children['static']]
level_sprites.append(pc)

[MAIN_PHYSICAL_GROUP.add(sprite) for sprite in level_sprites + StaticSprites]
PC_PHYSICAL_GROUP.add(pc)
controls.main(background_layers=background_layers,
              sprites=level_sprites + StaticSprites,
              text=a_text,
              sprite_groups=[MAIN_PHYSICAL_GROUP, PC_PHYSICAL_GROUP],
              tiles=game_tiles,
              BaseSprite=BaseSprite,
              StaticSprite=StaticSprite)
exit(1)
