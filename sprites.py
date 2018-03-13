from random import choice
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
            path='',
            colide=choice(["Ouch! Don't bang into me!", "Hello, how are you today?", "Inside, I'm dying"]),
            message=choice(["I like you"]),
            **kwargs
            ):
        self.state="default"
        self.width = width
        self.height = height
        self.states = states
        self.step = 0
        self.frame_counter = 0
        self.i = i
        self.j = j
        self.path = path
        self.kwargs = kwargs
        self.state_generator()
        self.children = []
        self.rest_state = "default"
        self.state_map ={
           "up": self.up,
           "down": self.down,
           "left": self.left,
           "right": self.right
        }
        self.image = pygame.transform.scale(
                self.states[self.state][self.step],
                (self.width, self.height)
                ).copy()

    def movement(self,i,j):
        pass
    
    def right(self):
        self.state = "right"
        self.rest_state = "default_up"
        self.movement(-self.speed,0)

    def left(self):
        self.state = "left"
        self.movement(self.speed,0)

    def up(self):
        self.state = "up"
        self.rest_state = "default_up"
        self.movement(0,self.speed)

    def down(self):
        self.state = "down"
        self.rest_state = "default"
        self.movement(0, -self.speed)

    def still(self):
        self.movement(0, 0)
    def log(self, message):
        log(__name__, message)

    def state_generator(self):
        for state in self.states:
            for frame_index in range(len(self.states[state])):
                if type(self.states[state][frame_index]) == str:
                    try:
                       self.states[state][frame_index] = pygame.image.load(
                                  self.states[state][frame_index]
                               ).convert_alpha()
                    except:
                       self.states[state][frame_index] = pygame.image.load(
                                  self.path + self.states[state][frame_index]
                               ).convert_alpha()


    def position_log(self):
        self.log([self.i, self.j])

    def each_frame(self):
        pass

    def resize(self, *args):
        pass

    def update(self):
        self.position_log()
        self.each_frame()
        if self.step >= len(self.states[self.state]):
           self.step = 0
        controls.screen.blit(
                pygame.transform.scale(
                   self.states[self.state][self.step], 
                   (self.width, self.height)
                   ),
                   (self.i + controls.x,self.j + controls.y),
        )
        self.state = self.rest_state
        self.frame_counter += 1
        if not self.frame_counter % 3:
           self.step += 1 
        self.passback = {}
        return self.passback

class npc_sprite(base_sprite):
    move = 0
    speed = 1
    walk_duration = 20
    name = "npc"

    def movement(self, i, j):
        self.i += i
        self.j += j

    def choose_random_direction(self):
        self.current_move = choice([self.up, self.down, self.left, self.right] + 10 * [self.still])

    def each_frame(self):
        if not self.move % self.walk_duration:
            self.choose_random_direction()
        self.current_move()    
        self.move += 1

class player_sprite(npc_sprite):
   x = controls.width/2 - 20
   y = controls.width/2 - 35
   name = "player"


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
        self.state = self.rest_state
        print controls.actions.keys()
        for action in ["left", "right", "down", "up"]:
            if controls.actions[action] and action not in ["attack", "back"]:
                if self.states[action]:
                   self.state = action
                   self.state_map[action]()
            elif controls.actions[action] and action in ["attack", "back"]:
                print(action)
        self.frame_counter += 1
        if not self.frame_counter % 5:
           self.step += 1 
        self.i = self.x - controls.x  
        self.j = self.y - controls.y 
        self.passback = {}
        return self.passback
