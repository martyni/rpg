""" Class for dealing with sprites """

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


class BaseSprite(pygame.sprite.Sprite):
    """ Base sprite class that shares functionality with all other sprites """
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
        """ a """
        self.rect.x = self.i + controls.x
        self.rect.y = self.j + controls.y

    def collide(self, rect):
        """ a """
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
        """ a """
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
        """ a """
        self.state = "right"
        self.rest_state = "default_right"
        self.movement(-self.speed, 0)

    def left(self):
        """ a """
        self.state = "left"
        self.rest_state = "default_left"
        self.movement(self.speed, 0)

    # pylint: disable=invalid-name
    # I think this is because up is only 2 letters long.
    # It explains what its doing so I'm keeping it.
    def up(self):
        """ a """
        self.state = "up"
        self.rest_state = "default_up"
        self.movement(0, self.speed)

    def down(self):
        """ a """
        self.state = "down"
        self.rest_state = "default"
        self.movement(0, -self.speed)

    def still(self):
        """ a """
        self.movement(0, 0)

    def state_generator(self):
        """ a """
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
        """ a """
        log(__name__, [self.i, self.j])

    def each_frame(self):
        """ a """
        pass

    def resize(self, *args):
        """ a """
        pass

    def update(self):
        """ a """
        self.position_log()
        self.each_frame()
        if self.step >= len(self.states[self.state]):
            self.step = 0
        controls.screen.blit(
            # pygame.transform.scale(
            self.states[self.state][self.step],
            #  (self.width, self.height)
            #   ),
            (self.i + controls.x, self.j + controls.y),
        )
        self.state = self.rest_state
        self.frame_counter += 1
        if not self.frame_counter % self.frame_wait:
            self.step += 1
        self.movement(0, 0)
        # pygame.display.flip()
        # sleep(0.5)
        return self.passback


class PhysicalSprite(BaseSprite):
    """ a """
    speed = 1
    gradient = 1

    def shadow(self):
        """ a """
        gfxdraw.filled_ellipse(
            controls.screen,
            self.rect.midbottom[0],
            self.rect.midbottom[1],
            self.width/3,
            self.height/8,
            (10, 10, 10, 220)
        )


class StaticSprite(PhysicalSprite):
    """ a """
    speed = 0
    name = "static"


class NpcSprite(PhysicalSprite):
    """ a """
    move = 0
    speed = 1
    walk_duration = 20
    name = "npc"

    def movement(self, i, j):
        """ a """
        self.i += i
        self.j += j
        self.rect.x = self.i + controls.x
        self.rect.y = self.j + controls.y

    def choose_random_direction(self):
        """ a """
        self.current_move = choice(
            [self.up, self.down, self.left, self.right] + 10 * [self.still])

    def each_frame(self):
        """ a """
        # self.shadow()
        if not self.move % self.walk_duration:
            self.choose_random_direction()
        self.current_move()
        self.move += 1


class PlayerSprite(PhysicalSprite):
    """ a """
    x = controls.width/2 - 20
    y = controls.height/2 - 35
    sensitivity = 3
    name = "player"
    speed = 30
    passback = {}
    to_say = ''
    to_say_cooldown = 0
    collisions = [False, False, False, False]

    def movement(self, i, j):
        """ a """
        pass

    def collide(self, rect):
        """ a """
        self.char_x, self.char_y = deepcopy(self.rect.center)
        col_x, col_y = rect.center
        shoulders = list(self.rect.midtop)
        shoulders[1] -= 31
        if col_x < self.char_x and (rect.collidepoint(self.rect.midleft) \
                                    or rect.collidepoint(self.rect.bottomleft)):
            self.collisions[0] = "left"
        if col_x > self.char_x and (rect.collidepoint(self.rect.midright) \
                                    or rect.collidepoint(self.rect.bottomright)):
            self.collisions[1] = "right"
        if col_y > self.char_y and (rect.collidepoint(self.rect.midbottom)):
            self.collisions[2] = "down"
        if col_y < self.char_y and (rect.collidepoint(self.rect.midtop)):
            print self.rect.midtop
            print self.rect.center
            print self.rect.midbottom
            print col_x, col_y
            self.collisions[3] = "up"
        return self.collisions

    def update(self):
        """ a """
        self.collisions = [False, False, False, False]
        # self.shadow()
        self.position_log()
        if self.step >= len(self.states[self.state]):
            self.step = 0
        for child in self.children:
            controls.screen.blit(child.state.get(
                self.state, "default"), self.x, self.y)
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
        if not self.frame_counter % self.frame_wait:
            self.step += 1
        self.i = self.x
        self.j = self.y
        self.passback = {}
        return self.passback
