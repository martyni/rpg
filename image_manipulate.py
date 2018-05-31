"""Module for manipulating images"""
from os import walk
#from PIL import Image

DIR = ["top", "bottom", "left", "right"]
IMAGES = [_ for _ in walk('assets/IMAGES/')][0][-1]
JPGS = [_ for _ in IMAGES if 'jpg' in _]
MASKS = [_ for _ in JPGS if 'mask' in _]
BASE_TILES = []
#for jpg in JPGS:
#    if jpg not in MASKS:
#        for
