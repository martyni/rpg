""" Test script, mainly used to translate keys to events """
from random import randint
import pygame
# pylint: disable=wildcard-import, undefined-variable, unused-wildcard-import, no-member
# Standard pygame tricks
from pygame.locals import *
from pygame import event as ev
pygame.init()
# pylint: disable=invalid-name
# Disagree with ALL_CAPS variables atleast in test function
width, height = 500, 500
screen = pygame.display.set_mode(
    (width, height),
    HWSURFACE | DOUBLEBUF | RESIZABLE)


# pylint: disable=dangerous-default-value
# I also like to live dangerously
def main(sprites=[]):
    """ Test function """
    # pylint: disable= global-statement
    # Why is there a global statement that I'm not allowed to use?
    global screen
    global width
    global height
    game = True
    while game:
        ev.pump()
        for event in ev.get():
            if event.type == QUIT:
                game = False
                pygame.display.quit()
                log(__name__, "exiting")
                exit(1)
            elif event.type == VIDEORESIZE:
                width, height = event.dict['size']
                screen = pygame.display.set_mode(
                    (width, height), HWSURFACE | DOUBLEBUF | RESIZABLE)
                # pylint: disable=expression-not-assigned
                # Don't want this to be assigned.
                [sprite.resize(width, height) for sprite in sprites]
            print event

        screen.fill((randint(1, 255), randint(1, 255), randint(1, 255)))
        pygame.display.flip()


if __name__ == "__main__":
    main()
