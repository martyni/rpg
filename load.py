""" Loads the assets and levels """
import os
import yaml
from controls import log

ASSETS = [{i[0]:[i[1], i[2]]} for i in os.walk('assets')]
ASSETS = {i[0]: [i[1], i[2]] for i in os.walk('assets')}
LEVELS = {i: {} for i in ASSETS['assets'][0] if 'l' in i}

# pylint: disable=too-many-instance-attributes
# Need to these attributes
class Base(object):
    """ Loads the assets and levels """
    def __init__(self, level, files, directories):
        self.level = level
        self.__name__ = self.level
        self.files = files
        self.directories = directories
        self.images = []
        self.settings = {}
        self.children = {}
        self.path = 'assets/{}/'.format(self.level)
        self.parse_files()
        try:
            self.update_states()
        except IndexError:
            pass

    def get_file(self, item):
        """ Sanitizer for file names"""
        filename = 'assets/{level}/{item}'.format(
            level=self.level,
            item=item
        )
        return filename

    def update_states(self):
        """ Iterator to get all of the states for a given sprite"""
        for state in self.settings['states']:
            image_list = self.settings['states'][state]
            for image_file in range(len(image_list)):
                if self.path not in state[image_file]:
                    #try:
                    image_name = image_list.pop()

                    self.settings['states'][state].insert(image_file,
                                                          self.get_file(
                                                              image_name)
                                                         )
                    #except:
                    #    pass

    def parse_files(self):
        """ Main loop to drive loading"""
        for filename in self.files:
            if '.jpg' in filename or 'png' in filename:
                self.images.append(self.get_file(filename))
            if '.yml' in filename or '.yaml' in filename:
                with open(self.get_file(filename), 'r') as cfg:
                    config = yaml.load(cfg.read())
                    self.settings.update(config)
                    self.settings['path'] = self.path


for asset_level in LEVELS:
    level_key = '/'.join(['assets', asset_level])
    dirs = ASSETS[level_key][0]
    asset_files = ASSETS[level_key][1]
    LEVELS[asset_level] = Base(asset_level, asset_files, dirs)
    for dire in dirs:
        level_key = 'assets/{level}/{dire}'.format(
            level=asset_level,
            dire=dire
        )
        for child in ASSETS[level_key][0]:
            level_key = 'assets/{level}/{dire}/{child}'.format(
                level=asset_level,
                dire=dire,
                child=child
            )
            child_level = '{level}/{dire}/{child}'.format(
                level=asset_level,
                dire=dire,
                child=child
            )
            dirs = ASSETS[level_key][0]
            asset_files = ASSETS[level_key][1]
            try:
                LEVELS[asset_level].children[dire].append(
                    Base(child_level, asset_files, dirs))
            except KeyError:
                LEVELS[asset_level].children[dire] = [Base(child_level, asset_files, dirs)]
TILE_LIST = [image for image in [f for f in os.walk(
    'assets/images/')][0][2] if 'tile' in image]

TILES = {}
for tile in TILE_LIST:
    _, name, index = tile.split('_')
    index = int(index.split('.')[0])
    if TILES.get(name):
        TILES[name].append('assets/images/' + tile)
    else:
        TILES[name] = ['assets/images/' + tile]
    log("Loading", name)

log("Loading", TILES)
