from PIL import Image
from os import walk

DIR = ["top", "bottom", "left", "right"]:
IMAGES = [i for i in walk('assets/images/')][0][-1]
JPGS = [j for j in images if 'jpg' in j]
MASKS = [ m for m in jpgs if 'mask' in m]
BASE_TILES = []
#for jpg in JPGS:
#    if jpg not in MASKS:
#        for 
