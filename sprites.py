""" Class for dealing with sprites"""

# pylint: disable=too-many-instance-attributes, dangerous-default-value, too-many-arguments, unused-argument, no-name-in-module, c-extension-no-member
# 1) Sprites require lots of attributes
# 2) I need those typed default values
# 3) Same as the attributes sprites need lots of information
# 4) Unused arguments are used by other functions in controls.py
# 5) This seems to keep coming up in pygame
# 6) Something about gfxdraw being a c-extension

import sys
from random import choice
from copy import deepcopy
from ruamel.yaml import YAML
from pygame import gfxdraw, error
import controls
from controls import pygame, log

def draw_points(points_list):
    """Draws points as circles"""
    for point in points_list:
        gfxdraw.filled_circle(controls.SCREEN, point[0], point[1], 5, (128, 0, 128))

class BaseSprite(pygame.sprite.Sprite):
    """ Base sprite class that shares functionality with all other sprites"""
    move = 0
    walk_duration = 0

    def __init__(
            self,
            width=34,
            height=64,
            states={"default": [pygame.image.load(
                "test.png").convert_alpha()]},
            i=0,
            j=0,
            path='assets/images/',
            colide=["Ouch! Don't bang into me!",
                    "Hello, how are you today?", "Inside, I'm dying"],
            message=choice(["I like you"]),
            name="default",
            **kwargs
    ):
        pygame.sprite.Sprite.__init__(self)
        self.state = "default"
        self.width = width
        self.height = height
        self.states = states
        self.colide = colide
        self.step = 0
        self.frame_counter = 0
        self.i = i
        self.j = j
        self.knee = [0, 0]
        self.char_x = int()
        self.char_y = int()
        self.path = path
        self.kwargs = kwargs
        self.state_files = {key: list(states[key]) for key in states}
        self.state_generator()
        self.children = []
        self.rest_state = "default"
        self.frame_wait = 10
        self.message = message
        self.name = name
        self.current_move = self.still
        self.passback = {}
        self.state_map = {
            "up": self.up,
            "down": self.down,
            "left": self.left,
            "right": self.right
        }
        self.image = pygame.transform.scale(
            self.states[self.state][self.step],
            (self.width, self.height)
        ).copy()
        self.rect = pygame.Rect(self.i, self.j, self.width, self.height)

    def movement(self, i, j):
        """ Method takes the global value for x, y of PC and sets the local value of this sprite"""
        self.rect.x = self.i + controls.X
        self.rect.y = self.j + controls.Y

    def collide(self, rect):
        """ What happens when an NPC collides with another sprite in the same group"""
        if rect.x < self.rect.x:
            self.left()
            self.current_move = self.left
        if rect.x > self.rect.x:
            self.right()
            self.current_move = self.right
        if rect.y > self.rect.y:
            self.down()
            self.current_move = self.down
        if rect.y < self.rect.y:
            self.up()
            self.current_move = self.up
        if self.move >= self.walk_duration * 0.8:
            self.current_move = self.still
        return None

    def to_yaml(self):
        """ Prints certain values to the screen in YAML format"""
        yaml = YAML()
        yaml.explicit_start = True
        yaml.indent(sequence=4, offset=2)
        data = {
            "i": self.i,
            "j": self.j,
            "x": self.x,
            "y": self.y}
        data.update({"states": self.state_files})
        print yaml.dump(
            data,
            sys.stdout
        )

    def right(self):
        """ Basic move right function"""
        self.state = "right"
        self.rest_state = "default_right"
        self.movement(-self.speed, 0)

    def left(self):
        """ Basic move left function"""
        self.state = "left"
        self.rest_state = "default_left"
        self.movement(self.speed, 0)

    # pylint: disable=invalid-name
    # I think this is because up is only 2 letters long.
    # It explains what its doing so I'm keeping it.
    def up(self):
        """ Basic move up function"""
        self.state = "up"
        self.rest_state = "default_up"
        self.movement(0, self.speed)

    def down(self):
        """ Basic move down function"""
        self.state = "down"
        self.rest_state = "default"
        self.movement(0, -self.speed)

    def still(self):
        """ Basic don't move function"""
        self.movement(0, 0)

    def state_generator(self):
        """
        Run when the sprite loads.
        This takes the sprite state object/text and loads images to cycle through"""
        for state in self.states:
            for frame_index in range(len(self.states[state])):
                if isinstance(self.states[state][frame_index], str):
                    try:
                        self.states[state][frame_index] = pygame.image.load(
                            self.states[state][frame_index]
                        ).convert_alpha()
                    except error:
                        self.states[state][frame_index] = pygame.image.load(
                            self.path + self.states[state][frame_index]
                        ).convert_alpha()

                self.states[state][frame_index] = pygame.transform.scale(
                    self.states[state][frame_index],
                    (self.width, self.height)
                )

    def position_log(self):
        """ print sprite position"""
        log(__name__, [self.i, self.j])

    def each_frame(self):
        """ method handle to do each frame"""
        pass

    def resize(self, *args):
        """ Method to handle screen resizes"""
        pass

    def update(self):
        """ Run each frame to update the sprite"""
        self.position_log()
        self.each_frame()
        if self.step >= len(self.states[self.state]):
            self.step = 0
        controls.SCREEN.blit(
            self.states[self.state][self.step],
            (self.i + controls.X, self.j + controls.Y),
        )
        self.state = self.rest_state
        self.frame_counter += 1
        if not self.frame_counter % self.frame_wait:
            self.step += 1
        self.movement(0, 0)
        return self.passback


class PhysicalSprite(BaseSprite):
    """ Physical sprite class. For sprites that need to touch each other"""
    speed = 1
    gradient = 1

    def shadow(self):
        """ Draw a shadow under the character"""
        gfxdraw.filled_ellipse(
            controls.SCREEN,
            self.rect.midbottom[0],
            self.rect.midbottom[1],
            self.width/3,
            self.height/8,
            (10, 10, 10, 220)
        )


class StaticSprite(PhysicalSprite):
    """ Static sprite class. For sprites that need to stay where they are"""
    speed = 0
    name = "static"


class NpcSprite(PhysicalSprite):
    """ NPC sprites. For those non playable sprites"""
    move = 0
    speed = 1
    walk_duration = 20
    name = "npc"

    def movement(self, i, j):
        """ Method takes the global value for x, y of PC and sets the local value of this sprite"""
        self.i += i
        self.j += j
        self.rect.x = self.i + controls.X
        self.rect.y = self.j + controls.Y

    def choose_random_direction(self):
        """ Picks a random movement function, weighted to stay still most of the time"""
        self.current_move = choice(
            [self.up, self.down, self.left, self.right] + 10 * [self.still])

    def each_frame(self):
        """
        Npc checks if its finished walking
        in a random direction or picks a
        new one to walk in
        """
        # self.shadow()
        if not self.move % self.walk_duration:
            self.choose_random_direction()
        self.current_move()
        self.move += 1


class PlayerSprite(PhysicalSprite):
    """ Player sprites. For those playable sprites"""
    x = controls.WIDTH/2 - 20
    y = controls.HEIGHT/2 - 35
    sensitivity = 3
    name = "player"
    speed = 30
    passback = {}
    to_say = ''
    to_say_cooldown = 0
    collisions = [False, False, False, False]

    def movement(self, i, j):
        """ Generally stay where they are"""
        pass

    def collide(self, rect):
        """ Runs whenever a sprite in the same group as the playable character collides"""
        self.char_x, self.char_y = deepcopy(self.rect.center)
        col_x, col_y = rect.center
        shoulders = list(self.rect.midtop)
        shoulders[1] -= 31
        self.knee = [self.rect.midbottom[0],
                     self.rect.center[1] + (self.rect.midbottom[1] -  self.rect.center[1])/2]
        if col_x < self.char_x and (rect.collidepoint(self.rect.midleft)
                                    or rect.collidepoint(self.knee)):
            self.collisions[0] = "left"
        if col_x > self.char_x and (rect.collidepoint(self.rect.midright)
                                    or rect.collidepoint(self.knee)):
            self.collisions[1] = "right"
        if col_y > self.char_y and (rect.collidepoint(self.rect.midbottom)):
            self.collisions[2] = "down"
        if col_y < self.char_y and (rect.collidepoint(self.rect.midtop)):
            self.collisions[3] = "up"
        return self.collisions



    def update(self):
        """
        Run each frame to update the sprite,
        had to alter for the PC as its
        behaviour was too different
        """
        self.collisions = [False, False, False, False]
        # self.shadow()
        self.position_log()
        if self.step >= len(self.states[self.state]):
            self.step = 0
        for child in self.children:
            controls.SCREEN.blit(child.state.get(
                self.state, "default"), self.x, self.y)
        controls.SCREEN.blit(
            self.states[self.state][self.step],
            (self.x, self.y),
        )
        self.state = self.rest_state
        for action in ["left", "right", "down", "up", "attack", "back"]:
            if controls.ACTIONS[action] and action not in ["attack", "back"]:
                if self.states[action]:
                    self.state = action
                    self.state_map[action]()
            elif controls.ACTIONS[action] and action in ["attack", "back"]:
                if action == "back":
                    self.to_yaml()
        self.frame_counter += 1
        if not self.frame_counter % self.frame_wait:
            self.step += 1
        self.i = self.x
        self.j = self.y
        self.passback = {}
        #draw_points([self.rect.center,
        #                   self.rect.midleft,
        #                   self.rect.midbottom,
        #                   self.rect.midtop,
        #                   self.rect.midright,
        #                   self.knee])

        return self.passback
