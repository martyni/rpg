from PIL import Image, ImageChops
from PIL.ImageFilter import *


def ghost(image, ghostyness=10, show=True):
    a = image.filter(BLUR)
    for i in range(ghostyness):
        a = a.filter(BLUR)
    final = ImageChops.lighter(a, image)
    if show:
        final.show()
    return final
