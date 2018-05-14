import pygame.midi
import yaml
import os
from pygame import event as ev
from copy import deepcopy
from pygame.locals import *
from pprint import pprint
from random import randint
from math import pi
from time import sleep
from introduction import splash_screen
('X11', 'dga', 'ggi', 'vgl', 'aalib', 'directfb', 'fbcon', 'svgalib')
os.environ["SDL_FBDEV"] = "dave"
splash_screen()
pygame.init()
width, height = 640, 480
screen = pygame.display.set_mode((width, height))

blank_screen = pygame.Surface((width, height))
blank_screen.fill((255, 255, 255))
verbose = True
speed = 3
spacing = 32
x = 0
y = 0
actions = {i: False for i in ["up", "down", "left", "right", "attack", "back"]}
key_map = {
    "up": [111, 134, 126],
    "down": [116, 133, 125],
    "left": [113, 131, 123],
    "right": [114, 132, 124],
    "attack": [8, 0],
    "back": [9, 1]
}


def log(self, message):
    ''' Criminally underutilised logging function'''
    if verbose:
        print self, message


def check_move(blocking):
    '''Mapping of directions with their corresponding functions'''
    funcs = {
        "up": up,
        "down": down,
        "left": left,
        "right": right,
        "attack": attack,
        "back": back
    }
    move = False
    for i in actions:
        if actions[i] and i not in blocking:
            funcs[i]()
            move = True
    return move


def move(i, j):
    global x
    x += i
    global y
    y += j


def position_to_grid(i, j):
    i -= i % spacing - x % spacing
    j -= j % spacing - y % spacing
    return [i, j]


def up():
    move(0, speed)


def down():
    move(0, -speed)


def left():
    move(speed, 0)


def right():
    move(-speed, 0)


def attack():
    pass


def back():
    pass


def load_background(file):
    with open(file, 'r') as background:
        raw_f = background.read()
    return yaml.load(raw_f)


def save_background(file, tile_list):
    with open(file, 'w') as background:
        raw_f = background.write(yaml.dump(tile_list))


def scroll(key, list, direction=1):
    key += direction
    if key >= len(list) - 1:
        key = 0
    elif key < 0:
        key = len(list) - 1
    return key


def main(background_layers=[], sprites=[], text=None, sprite_groups=None, tiles=None, BaseSprite=None, StaticSprite=None):
    global screen
    global blank_screen
    text_queue = ["Hello Game", "How are you today?"]
    game = True
    clock = pygame.time.Clock()
    rect_list = []
    try:
        current_background_dump = load_background('level.yml')
        if current_background_dump is None:
            current_background_dump = []
    except:
        current_background_dump = []
        print 'load failed'
    current_tile = 0
    while game:
        ev.pump()
        blocking = []
        position = pygame.mouse.get_pos()
        grid_position = position_to_grid(position[0], position[1])
        r = pygame.Rect(grid_position[0], grid_position[1], spacing, spacing)
        rect_list.append(r)
        for event in ev.get():
            if event.type == QUIT:
                game = False
                save_background("level.yml", current_background_dump)
                pygame.display.quit()
                log(__name__, "exiting")
                exit(1)

            elif event.type == VIDEORESIZE:
                width, height = event.dict['size']
                screen = pygame.display.set_mode(
                    (width, height), DOUBLEBUF | RESIZABLE, 12)
                blank_screen = pygame.Surface((width, height))
                blank_screen.fill((255, 255, 255))
                [sprite.resize(width, height) for sprite in sprites]
                text.resize(width, height)

            elif event.type == MOUSEBUTTONDOWN:
                if event.button == 4:
                    current_tile = scroll(current_tile, tiles)
                elif event.button == 5:
                    current_tile = scroll(current_tile, tiles, -1)
                else:
                    states_copy = {}
                    for state in tiles[current_tile]['states']:
                        states_copy[state] = list(
                            tiles[current_tile]['states'][state])
                    new_tile = BaseSprite(**tiles[current_tile])
                    new_tile.i = int(grid_position[0] - x)
                    new_tile.j = int(grid_position[1] - y)
                    background_layers.append(new_tile)
                    tiles[current_tile]['states'] = states_copy
                    tile_copy = dict(tiles[current_tile])
                    tile_copy["i"] = int(grid_position[0] - x)
                    tile_copy["j"] = int(grid_position[1] - y)
                    print tile_copy
                    current_background_dump.append(deepcopy(tile_copy))

            elif event.type == KEYDOWN:
                if event.scancode in key_map["up"]:
                    ev.post(ev.Event(20, {"up": True}))
                elif event.scancode in key_map["down"]:
                    ev.post(ev.Event(20, {"down": True}))
                elif event.scancode in key_map["left"]:
                    ev.post(ev.Event(20, {"left": True}))
                elif event.scancode in key_map["right"]:
                    ev.post(ev.Event(20, {"right": True}))
                if event.scancode in key_map["attack"]:
                    ev.post(ev.Event(20, {"attack": True}))
                if event.scancode in key_map["back"]:
                    ev.post(ev.Event(20, {"back": True}))

            elif event.type == KEYUP:
                if event.scancode in key_map["up"]:
                    ev.post(ev.Event(20, {"up": False}))
                elif event.scancode in key_map["down"]:
                    ev.post(ev.Event(20, {"down": False}))
                elif event.scancode in key_map["left"]:
                    ev.post(ev.Event(20, {"left": False}))
                elif event.scancode in key_map["right"]:
                    ev.post(ev.Event(20, {"right": False}))
                if event.scancode in key_map["attack"]:
                    ev.post(ev.Event(20, {"attack": False}))
                if event.scancode in key_map["back"]:
                    ev.post(ev.Event(20, {"back": False}))

            elif event.type == 20:
                log(__name__, event)
                direction = event.dict.keys()[0]
                actions[direction] = event.dict[direction]

        for layer in background_layers:
            layer.update()
        sprites = sorted(sprites, None, lambda sprite: (
            sprite.rect.y, sprite.rect.x))
        #grid(screen, rect_list, 640, 480)
        for sprite in sprites:
            a = sprite.update()
            #pygame.draw.rect(screen, (0,0,255), sprite.rect)
            rect_list.append(sprite.rect)

            if a.get('text'):
                print len(text_queue)
                text_queue.append(a['text'])
            for group in sprite_groups:
                if sprite in group:
                    group.remove(sprite)
                    collision = pygame.sprite.spritecollideany(sprite, group)
                    if collision:
                        if sprite.collide(collision.rect):
                            for collision in pygame.sprite.groupcollide(sprite_groups[1], sprite_groups[0], False, False)[sprite]:
                                #pygame.draw.rect(screen, (255,0,0,40), collision.rect)
                                pygame.draw.line(
                                    screen, (255, 128, 40), sprite.rect.center, collision.rect.center, 5)
                                blocking += sprite.collide(collision.rect)
                                print blocking
                    group.add(sprite)
        text_queue = text.update(text_queue)
        #grid(screen, rect_list, 640, 480)
        move = check_move(blocking)
        #crt_tv(screen, rect_list, 640, 480)
        pygame.draw.rect(screen, (255, 128, 56), r, 0)
        pygame.display.update(rect_list)
        if move:
            #screen.fill((randint(1,255), randint(1,255), randint(1,255)))
            pass
        screen.fill((250, 250, 250, 0))
        # pygame.display.update(rect_list)
        clock.tick(40)
        game_info = "mouse: {m_x} , {m_y}, pos: {x}, {y} fps: {fps}, tile: {tile}".format(
            m_x=r.x,
            m_y=r.y,
            x=x,
            y=y,
            fps=clock.get_fps(),
            tile=tiles[current_tile].get("name")
        )
        pygame.display.set_caption(game_info)


def crt_tv(screen, rect_list, width, height, flicker=40):
    for i in xrange(height/4):
        pygame.draw.aaline(screen, (120 + randint(0, flicker), 120 + randint(
            0, flicker), 120 + randint(0, flicker)), (0, i * 4), (width, i * 4))

        rect_list.append(pygame.Rect(0, i * 4, 640, 1))


def grid(screen, rect_list, width, height):
    for j in xrange(0, height, spacing):
        pygame.draw.aaline(screen, (0, 0, 0), (0, y %
                                               spacing + j), (width, y % spacing + j))
        rect_list.append(pygame.Rect(0, j * spacing, width, 1))
    for i in xrange(0, width, spacing):
        pygame.draw.aaline(screen, (0, 0, 0), (x %
                                               spacing + i, 9), (x % spacing + i, height))
        rect_list.append(pygame.Rect(i * spacing, 0, height, 1))


if __name__ == "__main__":
    main()
