from ruamel.yaml import YAML
from random import choice
import sys
import controls
from controls import pygame, log
from time import sleep
from pprint import pprint

class base_sprite(pygame.sprite.Sprite):
    name = "default"
    def __init__(
            self,
            width=34,
            height=64,
            states= {"default": [pygame.image.load("test.png").convert_alpha()]},
            i=0,
            j=0,
            path='assets/images/',
            colide=["Ouch! Don't bang into me!", "Hello, how are you today?", "Inside, I'm dying"],
            message=choice(["I like you"]),
            **kwargs
            ):
        pygame.sprite.Sprite.__init__(self)
        self.state="default"
        self.width = width
        self.height = height
        self.states = states
        self.colide = colide
        self.step = 0
        self.frame_counter = 0
        self.i = i
        self.j = j
        self.path = path
        self.kwargs = kwargs
        self.state_files = { key: list(states[key]) for key in states}
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
        self.rect = pygame.Rect(self.i + 3, self.j + 3, self.width -6, self.height -6)

    def movement(self,i,j):
        self.rect.x = self.i + controls.x
        self.rect.y = self.j + controls.y
    
    def collide(self, rect):
        if rect.x > self.rect.x:
           self.right()
        elif rect.x < self.rect.x:
           self.left()
        if rect.y < self.rect.y:
           self.up()
        elif rect.y > self.rect.y:
           self.down()
        return None
    
    def to_yaml(self):
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent(sequence=4, offset=2)
        data = {
        "i":self.i,
        "j":self.j,
        "x":self.x,
        "y":self.y}
        data.update({"states":self.state_files})
        print yaml.dump(
        data,
        sys.stdout
        )

    def right(self):
        self.state = "right"
        self.rest_state = "default_right"
        self.movement(-self.speed,0)
        

    def left(self):
        self.state = "left"
        self.rest_state = "default_left"
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
                self.states[state][frame_index] = pygame.transform.scale(
                                                         self.states[state][frame_index],
                                                         (self.width, self.height)
                                                      )

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
                #pygame.transform.scale(
                   self.states[self.state][self.step], 
                #  (self.width, self.height)
                #   ),
                   (self.i + controls.x,self.j + controls.y),
        )
        self.state = self.rest_state
        self.frame_counter += 1
        if not self.frame_counter % 10:
           self.step += 1 
        self.passback = {}
        self.movement(0,0)
        return self.passback

class physical_sprite(base_sprite):
    speed = 1
    
class static_sprite(physical_sprite):
    speed = 0
    name = "static"

class npc_sprite(physical_sprite):
    move = 0
    speed = 1
    walk_duration = 20
    name = "npc"

    def movement(self, i, j):
        self.i += i
        self.j += j
        self.rect.x = self.i + controls.x
        self.rect.y = self.j + controls.y

    def choose_random_direction(self):
        self.current_move = choice([self.up, self.down, self.left, self.right] + 10 * [self.still])

    def each_frame(self):
        if not self.move % self.walk_duration:
            self.choose_random_direction()
        self.current_move()    
        self.move += 1

class player_sprite(physical_sprite):
   x = controls.width/2 - 20
   y = controls.height/2 - 35
   sensitivity = 3
   name = "player"
   speed = 30
   passback = {}
   to_say = ''
   to_say_cooldown = 0

   def movement(self,i,j):
        pass

   def collide(self, rect):
        collisions = [False, False]
        if rect.x > self.rect.x and rect.collidepoint(self.rect.midright):
           collisions[0] ="right"
        elif rect.x < self.rect.x and rect.collidepoint(self.rect.midleft):
           collisions[0] ="left"
        if rect.y < self.rect.y and rect.collidepoint(self.rect.midtop):
           collisions[1] = "up"
        elif rect.y > self.rect.y and rect.collidepoint(self.rect.midbottom):
           collisions[1] = "down"
        return collisions
        
   def update(self):
        self.position_log()
        if self.step >= len(self.states[self.state]):
           self.step = 0
        for child in self.children:
           controls.scrren.blit(child.state.get(self.state, "default"), self.x, self.y)
        controls.screen.blit(
                   self.states[self.state][self.step], 
                   (self.x, self.y),
        )
        self.state = self.rest_state
        for action in ["left", "right", "down", "up", "attack", "back"]:
            if controls.actions[action] and action not in ["attack", "back"]:
                if self.states[action]:
                   self.state = action
                   self.state_map[action]()
            elif controls.actions[action] and action in ["attack", "back"]:
                if action == "back":
                   self.to_yaml()
        self.frame_counter += 1
        if not self.frame_counter % 10:
           self.step += 1 
        self.i = self.x 
        self.j = self.y 
        self.passback = {}
        return self.passback
