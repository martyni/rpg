"""Custom image filters """
from PIL import ImageChops
from PIL.ImageFilter import BLUR


def ghost(image, ghostyness=10, show=True):
    """ Returns ghostly looking shining image"""
    blurred_image = image.filter(BLUR)
    for _ in range(ghostyness):
        blurred_image = blurred_image.filter(BLUR)
    final = ImageChops.lighter(blurred_image, image)
    if show:
        final.show()
    return final
