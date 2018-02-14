import os
import yaml
from pprint import pprint
from controls import log

assets =[{i[0] :[i[1], i[2]]} for i in os.walk('assets')] 
assets ={i[0] :[i[1], i[2]] for i in os.walk('assets')}
levels = {i: {} for i in assets['assets'][0]}

class Base(object):
    def __init__(self, level, files, directories):
        self.level = level
        self.__name__ = self.level
        self.files = files
        self.directories = directories
        self.images = []
        self.settings = {}
        self.parse_files()

    def get_file(self, item):
        return 'assets/{level}/{item}'.format(
                level=self.level,
                item=item
                )

    def parse_files(self):
        for filename in files:
            if '.jpg' in filename or 'png' in filename:
                self.images.append(self.get_file(filename))
            if '.yml' in filename or '.yaml' in filename:
                with open(self.get_file(filename), 'r') as cfg:
                    config = yaml.load(cfg.read())
                    self.settings.update(config)
                pprint(config)

for level in levels:
    level_key = '/'.join(['assets', level] )
    dirs = assets[level_key][0]
    files = assets[level_key][1]
    levels[level] = Base(level, files, dirs)
