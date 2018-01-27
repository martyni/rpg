import controls
from controls import pygame, log

class base_sprite(pygame.sprite.Sprite):
    def __init__(
            self,
            width,
            height,
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
        self.image = pygame.transform.scale(
                self.states[self.state][self.step],
                (self.width, self.height)
                ).copy()

    def update(self):
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



background = base_sprite(500, 500)
npc = base_sprite(50, 50, i=250, j=250)
npc1 = base_sprite(50, 50, i=350, j=12)
npc2 = base_sprite(50, 50, i=20, j=2)
pc = player_sprite(
        50, 
        50, 
        i=250, 
        j=250,
        states={
            "default": [
                pygame.image.load("test.png").convert_alpha(),
                ],
            "up": [
                pygame.image.load("test.png").convert_alpha(),
                pygame.transform.flip(pygame.image.load("test.png").convert_alpha(),1,0)
                ],
            "down": [
                pygame.image.load("test.png").convert_alpha(),
                pygame.transform.flip(pygame.image.load("test.png").convert_alpha(),1,0)
                ],
            "left": [
                pygame.image.load("test.png").convert_alpha(),
                pygame.transform.flip(pygame.image.load("test.png").convert_alpha(),1,0)
                ],
            "right": [
                pygame.image.load("test.png").convert_alpha(),
                pygame.transform.flip(pygame.image.load("test.png").convert_alpha(),1,0)
                ]
            },

        )
controls.main(background_layers=[background], sprites=[pc, npc, npc1, npc2])
exit(1)
