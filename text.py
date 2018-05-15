"""This is for handling Text to display in the game"""
import controls
from controls import pygame, log
pygame.font.init()


class BaseText(pygame.sprite.Sprite):
    """This Class is to handle the text sprites"""

    # pylint: disable=too-many-instance-attributes
    # need those bits
    def __init__(self,
                 text='abcdefg',
                 **kwargs
                ):
        self.font = pygame.font.SysFont('liberationserif', 30)
        self.text = text
        self.__name__ = "text"
        self.i = 0
        self.j = 10000000000
        self.width = controls.WIDTH
        self.height = controls.HEIGHT
        self.border_width = 3
        self.write = True
        self.resize(self.width, self.height)
        self.cooldown = 0
        self.state = ''
        self.kwargs = kwargs

    def resize(self, width, height):
        """Resize text so that it fits on the screen"""
        self.width, self.height = width, height
        self.text_screen = self.font.render(self.text, True, (0, 0, 0, 0))
        # pylint: disable=too-many-function-args
        # this is fined
        self.background = pygame.Surface(
            (width, int(height/9))).convert_alpha()
        self.background.fill((255, 255, 255, 200))

    def update(self, text_queue):
        """
        Runs once a frame, checks if theres anything in the
        text_queue and sets the self.write flag
        """
        try:
            self.text = text_queue[0]
            self.write = True
        except IndexError:
            self.write = False

        if self.write:
            self.resize(self.width, self.height)
            controls.SCREEN.blit(
                self.background, [0, self.height - int(self.height / 9)])
            pygame.draw.rect(
                controls.SCREEN,
                (0, 0, 0, 0),
                [
                    0,
                    self.height - int(self.height / 9),
                    self.width,
                    int(self.height/9)
                ],
                self.border_width
            )
            controls.SCREEN.blit(self.text_screen, [
                self.border_width,
                self.height - int(self.height / 9)
            ])
        for action in controls.ACTIONS:
            if controls.ACTIONS[action]:
                self.state = action
            if self.state == 'attack':
                try:
                    if not self.cooldown:
                        text_queue.pop(0)
                        self.cooldown = 30
                except IndexError:
                    log(self.__name__, 'out of text')
        if self.cooldown > 0:
            self.cooldown -= 1
        return text_queue
