"""Custom image filters """
from PIL import ImageChops, Image
from PIL.ImageFilter import BLUR


DIRECTIONS = {
    0: "bottom",
    90: "right",
    180: "top",
    270: "left"
}

def ghost(image, ghostyness=10, show=True):
    """ Returns ghostly looking shining image"""
    blurred_image = image.filter(BLUR)
    for _ in range(ghostyness):
        blurred_image = blurred_image.filter(BLUR)
    final = ImageChops.lighter(blurred_image, image)
    if show:
        final.show()
    return final


def image_combine(background, foreground, rotation=0):
    """Function to blit one image ontop of another"""
    foreground = foreground.rotate(rotation)
    background.paste(foreground, (0, 0), foreground)
    background.show()
    return background


def tile_masker(base, mask, frame_number=None):
    """
    Loops through different rotations
    given a mask and background tile
    """
    base_name = base.split(".png")[0]
    fore_name = mask.split(".png")[0]
    for i in range(0, 360, 90):
        background = Image.open(base)
        foreground = Image.open(mask)
        export = image_combine(background, foreground, rotation=i)
        if frame_number is None:
            export.save("{}_{}_{}.png".format(base_name, fore_name, DIRECTIONS[i]))
        elif isinstance(frame_number, int):
            export.save("{}_{}_{}_{}.png".format(base_name,
                                                 fore_name,
                                                 DIRECTIONS[i],
                                                 str(frame_number).zfill(2)))
        background.close()
        foreground.close()
        export.close()

if __name__ == "__main__":
    tile_masker("grass.png", "beach.png")
    tile_masker("grass.png", "beach.png", 0)
