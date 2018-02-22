import controls
from controls import pygame, log
pygame.font.init()


class base_text(pygame.sprite.Sprite):
    def __init__(self,
            text='a',
            **kwargs
            ):
        self.font = pygame.font.SysFont('notosanslisu',50)
        self.text = text
        self.surface = self.font.render(self.text, True, (0,0,0,0) )
        controls.screen.blit(self.surface, [0, int(controls.height /9)])



