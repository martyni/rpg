""" Main loop/entry point for game"""
import yaml
import controls
from sprites import BaseSprite, PlayerSprite, NpcSprite, StaticSprite
from text import BaseText
from load import LEVELS, TILES
from sprite_groups import MAIN_PHYSICAL_GROUP, PC_PHYSICAL_GROUP

#Create base game variables
A_TEXT = BaseText()
BACKGROUND = BaseSprite(**LEVELS['l1'].settings)
GAME_TILES = []

#Load game tiles from level yml file
with open('level.yml', 'r') as bg_tiles:
    TILE_LIST = yaml.load(bg_tiles.read())
try:
    BACKGROUND_LAYERS = [BaseSprite(**t) for t in TILE_LIST]
except TypeError:
    BACKGROUND_LAYERS = []

#Add the solid tiles to the MAIN_PHYSICAL_GROUP for collisions
for layer in BACKGROUND_LAYERS:
    if "solid" in layer.name:
        MAIN_PHYSICAL_GROUP.add(layer)

#Create the list of tiles found in Assets for editing
for tile in TILES:
    GAME_TILES.append({
        "width": 32,
        "height": 32,
        "i": 0,
        "j": 0,
        "name": tile,
        "states": {
            "default": TILES[tile]
        }
    })

#Add level 1 sprites
LEVEL_SPRITES = [NpcSprite(**child.settings)
                 for child in LEVELS['l1'].children['npc']]
STATIC_SPRITES = [StaticSprite(**child.settings)
                  for child in LEVELS['l1'].children['static']]

#Create Player character
PC = PlayerSprite(
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
        ] * 3 + [
            "assets/images/Iandalara_base_up0{}.bmp".format(i) for i in range(3)
        ],
        "default_right":
        [
            "assets/images/Iandalara_right00.bmp"
        ],
        "default_left":
        [
            "assets/images/Iandalara_left00.bmp"
        ],
        "up":
        [
            "assets/images/Iandalara_up0{}.bmp".format(i) for i in range(4)
        ],
        "down":
        [
            "assets/images/Iandalara_down0{}.bmp".format(i) for i in range(4)
        ],
        "left":
        [
            "assets/images/Iandalara_left0{}.bmp".format(i) for i in range(4)
        ],
        "right":
        [
            "assets/images/Iandalara_right0{}.bmp".format(i) for i in range(4)
        ],
    },

)
LEVEL_SPRITES.append(PC)
PC_PHYSICAL_GROUP.add(PC)

# pylint: disable=expression-not-assigned
# I also like to live dangerously
[MAIN_PHYSICAL_GROUP.add(sprite) for sprite in LEVEL_SPRITES + STATIC_SPRITES]

controls.main(background_layers=BACKGROUND_LAYERS,
              sprites=LEVEL_SPRITES + STATIC_SPRITES,
              text=A_TEXT,
              sprite_groups=[MAIN_PHYSICAL_GROUP, PC_PHYSICAL_GROUP],
              tiles=GAME_TILES,
              BaseSprite=BaseSprite,
              StaticSprite=StaticSprite)
exit(1)
