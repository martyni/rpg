import controls
from controls import pygame, log
pygame.font.init()


class base_text(pygame.sprite.Sprite):
    def __init__(self,
            text='abcdefg',
            **kwargs
            ):
        self.font = pygame.font.SysFont('liberationserif',30)
        self.text = text
        self.i =0
        self.j =10000000000
        self.width = controls.width
        self.height = controls.height
        self.border_width = 3
        self.write = True
        self.resize(self.width, self.height)
        self.cooldown = 0
        self.state = ''

    def resize(self, width, height): 
        self.width, self.height = width, height
        self.text_screen = self.font.render(self.text, True, (0,0,0,0) )
        self.background = pygame.Surface((width, int(height/9) )).convert_alpha()
        self.background.fill((255,255,255, 200))

    def update(self, text_queue):    
        self.resize(self.width, self.height)
        try:
           self.text = text_queue[0]
           self.write = True
        except:
           self.write = False 

        if self.write:
           controls.screen.blit(self.background, [0, self.height - int(self.height /9)])
           pygame.draw.rect(controls.screen, (0,0,0,0),[0, self.height - int(self.height /9), self.width, int(self.height/9)], self.border_width )
           controls.screen.blit(self.text_screen, [ self.border_width, self.height - int(self.height /9)])
        for action in controls.actions:
            if controls.actions[action]:
                self.state = action
            if self.state == 'attack':
                try:
                   if not self.cooldown:
                      text_queue.pop(0)
                      self.cooldown = 30
                except:
                   pass 
        if self.cooldown >0:
           self.cooldown -= 1       
        return text_queue 
        


