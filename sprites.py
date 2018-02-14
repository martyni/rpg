import controls
from controls import pygame, log

class base_sprite(pygame.sprite.Sprite):
    def __init__(
            self,
            width=50,
            height=50,
            states= {"default": [pygame.image.load("test.png").convert_alpha()]},
            i=0,
            j=0,
            ):
        self.state="default"
        self.width = width
        self.height = height
        self.states = states
        self.step = 0
        self.i = i
        self.j = j
        self.state_generator()
        self.image = pygame.transform.scale(
                self.states[self.state][self.step],
                (self.width, self.height)
                ).copy()

    def log(self, message):
        log(__name__, message)

    def state_generator(self):
        for state in self.states:
            for frame_index in range(len(self.states[state])):
                if type(self.states[state][frame_index]) == str:
                    print self.states[state][frame_index]
                    print frame_index
                    self.states[state][frame_index] = pygame.image.load(
                               self.states[state][frame_index]
                            ).convert_alpha()

    def position_log(self):
        self.log([self.i, self.j])

    def update(self):
        self.position_log()
        controls.screen.blit(
                pygame.transform.scale(
                   self.states[self.state][self.step], 
                   (self.width, self.height)
                   ),
                   (self.i + controls.x,self.j + controls.y),
        )

class player_sprite(base_sprite):
   x = 250
   y = 250
   def update(self):
        self.position_log()
        if self.step >= len(self.states[self.state]):
           self.step = 0
        controls.screen.blit(
                pygame.transform.scale(
                   self.states[self.state][self.step], 
                   (self.width, self.height)
                   ),
                   (self.x, self.y),
        )
        self.state = "default"
        for action in controls.action:
            if controls.action[action]:
                self.state = action
                
        self.step += 1
        self.i = self.x - controls.x  
        self.j = self.y - controls.y 
