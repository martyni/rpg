import os
import yaml
from pprint import pprint
from controls import log

assets =[{i[0] :[i[1], i[2]]} for i in os.walk('assets')] 
assets ={i[0] :[i[1], i[2]] for i in os.walk('assets')}
levels = {i: {} for i in assets['assets'][0] if 'l' in i}

class Base(object):
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
        except:
           pass

    def get_file(self, item):
        filename = 'assets/{level}/{item}'.format(
                level=self.level,
                item=item
                )
        return filename

    def update_states(self):
        for state in self.settings['states']:
            image_list = self.settings['states'][state]
            for image_file in range(len(image_list)):
                if self.path not in state[image_file]:
                    try:
                      image_name = image_list.pop()
                    
                      self.settings['states'][state].insert(image_file, 
                            self.get_file(image_name)
                            )
                    except:
                      pass
    def parse_files(self):
        for filename in files:
           
            if '.jpg' in filename or 'png' in filename:
                self.images.append(self.get_file(filename))
            if '.yml' in filename or '.yaml' in filename:
                with open(self.get_file(filename), 'r') as cfg:
                    config = yaml.load(cfg.read())
                    self.settings.update(config)
                    self.settings['path'] = self.path


for level in levels:
    level_key = '/'.join(['assets', level] )
    dirs = assets[level_key][0]
    files = assets[level_key][1]
    levels[level] = Base(level, files, dirs)
    for dire in dirs:
       level_key = 'assets/{level}/{dire}'.format(
               level=level,
               dire=dire
               )
       for child in assets[level_key][0]:
          level_key = 'assets/{level}/{dire}/{child}'.format(
               level=level,
               dire=dire,
               child=child
               )
          child_level = '{level}/{dire}/{child}'.format(
               level=level,
               dire=dire,
               child=child
               )
          dirs = assets[level_key][0]
          files = assets[level_key][1]
          try:
             levels[level].children[dire].append(Base(child_level, files, dirs))
          except:
             levels[level].children[dire] = [Base(child_level, files, dirs)]
tile_list = [ image for image in [file for file in os.walk('assets/images/')][0][2] if 'tile' in image]

tiles = {}
for tile in tile_list:
   _, name, index = tile.split('_')
   index = int(index.split('.')[0])
   if tiles.get(name):
      tiles[name].append('assets/images/' + tile)
   else:
      tiles[name] = ['assets/images/' + tile] 
   print name

print tiles
