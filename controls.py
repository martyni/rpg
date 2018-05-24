"""Main game loop"""
# pylint: disable=global-statement, no-name-in-module, no-member, dangerous-default-value
# need access to global variables
# another pygame error
# and another one
# still live dangerously
# pylint: disable=too-many-function-args,too-many-locals,too-many-nested-blocks,too-many-branches,too-many-statements,too-many-boolean-expressions
# too many shame

from copy import deepcopy
from random import randint
import yaml
import pygame
from pygame import event as ev
from pygame.locals import (
    QUIT,
    VIDEORESIZE,
    DOUBLEBUF,
    RESIZABLE,
    MOUSEBUTTONDOWN,
    KEYDOWN,
    KEYUP,
    )
from introduction import splash_screen

splash_screen()
pygame.init()
WIDTH, HEIGHT = 640, 480
SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))

BLANK_SCREEN = pygame.Surface((WIDTH, HEIGHT))
BLANK_SCREEN.fill((0, 0, 0))
VERBOSE = False
SPEED = 3
SPACING = 32
X = 0
Y = 0
ACTIONS = {i: False for i in ["up", "down", "left", "right", "attack", "back"]}
KEY_MAP = {
    "up": [111, 134, 126],
    "down": [116, 133, 125],
    "left": [113, 131, 123],
    "right": [114, 132, 124],
    "attack": [8, 0],
    "back": [9, 1]
}


def log(self, message):
    """ Criminally underutilised logging function"""
    if VERBOSE:
        print self, message


def check_move(blocking):
    """Mapping of directions with their corresponding functions"""
    funcs = {
        "up": up,
        "down": down,
        "left": left,
        "right": right,
        "attack": attack,
        "back": back
    }
    passback = False
    for i in ACTIONS:
        if ACTIONS[i] and i not in blocking:
            funcs[i]()
            passback = True
    return passback


def move(i, j):
    """Global move function called on PC"""
    global X
    global Y
    X += i
    Y += j


def position_to_grid(i, j):
    """Convert i,j mouse location and snap to grid based on global spacing value"""
    i -= i % SPACING - X % SPACING
    j -= j % SPACING - Y % SPACING
    return [i, j]


# pylint: disable=invalid-name
# up is a fine name
def up():
    """Global up"""
    move(0, SPEED)


def down():
    """Global down"""
    move(0, -SPEED)


def left():
    """Global left"""
    move(SPEED, 0)


def right():
    """Global right"""
    move(-SPEED, 0)


def attack():
    """Global attack"""
    pass


def back():
    """Global back"""
    pass


def load_background(a_file):
    """Load background from a file"""
    with open(a_file, 'r') as background:
        raw_f = background.read()
    return yaml.load(raw_f)


def save_background(a_file, tile_list):
    """
    Saves current placed tiles to yml file.
    no_repeats creates a dictionary where redundant tiles will
    save over each other. The way the tile list is created means
    new tiles will always take president.
    """
    no_repeats = {(tile["i"], tile["j"]): tile for tile in tile_list}
    tile_list = [tile for tile in no_repeats.values()]
    with open(a_file, 'w') as background:
        background.write(yaml.dump(tile_list))


def scroll(key, a_list, direction=1):
    """ a """
    key += direction
    if key >= len(a_list) - 1:
        key = 0
    elif key < 0:
        key = len(a_list) - 1
    return key

# pylint: disable=too-many-arguments,unused-argument
# yeh probably need to cut down
# I might need to access kwargs in the future
def main(background_layers=[],
         sprites=[],
         text=None,
         sprite_groups=None,
         tiles=None,
         base_sprite=None,
         **kwargs):
    """ a """
    global SCREEN
    global BLANK_SCREEN
    text_queue = ["Hello Game", "How are you today?"]
    game = True
    clock = pygame.time.Clock()
    rect_list = []
    try:
        current_background_dump = load_background('level.yml')
        if current_background_dump is None:
            current_background_dump = []
    except IOError:
        current_background_dump = []
        log(__name__, 'load failed')
    current_tile = 0
    sudo_clock = 0
    while game:
        ev.pump()
        blocking = []
        position = pygame.mouse.get_pos()
        grid_position = position_to_grid(position[0], position[1])
        cursor = pygame.Rect(grid_position[0], grid_position[1], SPACING, SPACING)
        rect_list.append(cursor)
        for event in ev.get():
            if event.type == QUIT:
                game = False
                save_background("level.yml", current_background_dump)
                pygame.display.quit()
                log(__name__, "exiting")
                exit(1)

            elif event.type == VIDEORESIZE:
                width, height = event.dict['size']
                SCREEN = pygame.display.set_mode(
                    (width, height), DOUBLEBUF | RESIZABLE, 12)
                BLANK_SCREEN = pygame.Surface((width, height))
                BLANK_SCREEN.fill((255, 255, 255))

                # pylint: disable=expression-not-assigned
                # Don't want this assigned
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
                    new_tile = base_sprite(**tiles[current_tile])
                    new_tile.i = int(grid_position[0] - X)
                    new_tile.j = int(grid_position[1] - Y)
                    background_layers.append(new_tile)
                    tiles[current_tile]['states'] = states_copy
                    tile_copy = dict(tiles[current_tile])
                    tile_copy["i"] = int(grid_position[0] - X)
                    tile_copy["j"] = int(grid_position[1] - Y)
                    current_background_dump.append(deepcopy(tile_copy))

            elif event.type == KEYDOWN:
                if event.scancode in KEY_MAP["up"]:
                    ev.post(ev.Event(20, {"up": True}))
                elif event.scancode in KEY_MAP["down"]:
                    ev.post(ev.Event(20, {"down": True}))
                elif event.scancode in KEY_MAP["left"]:
                    ev.post(ev.Event(20, {"left": True}))
                elif event.scancode in KEY_MAP["right"]:
                    ev.post(ev.Event(20, {"right": True}))
                if event.scancode in KEY_MAP["attack"]:
                    ev.post(ev.Event(20, {"attack": True}))
                if event.scancode in KEY_MAP["back"]:
                    ev.post(ev.Event(20, {"back": True}))

            elif event.type == KEYUP:
                if event.scancode in KEY_MAP["up"]:
                    ev.post(ev.Event(20, {"up": False}))
                elif event.scancode in KEY_MAP["down"]:
                    ev.post(ev.Event(20, {"down": False}))
                elif event.scancode in KEY_MAP["left"]:
                    ev.post(ev.Event(20, {"left": False}))
                elif event.scancode in KEY_MAP["right"]:
                    ev.post(ev.Event(20, {"right": False}))
                if event.scancode in KEY_MAP["attack"]:
                    ev.post(ev.Event(20, {"attack": False}))
                if event.scancode in KEY_MAP["back"]:
                    ev.post(ev.Event(20, {"back": False}))

            elif event.type == 20:
                log(__name__, event)
                direction = event.dict.keys()[0]
                ACTIONS[direction] = event.dict[direction]

        for layer in background_layers:
            layer.update(sudo_clock/10)
        sprites = sorted(sprites, None, lambda sprite: (
            sprite.rect.y, sprite.rect.x))
        #grid(screen, rect_list, 640, 480)
        for sprite in sprites:
            sprite_pass_back = sprite.update(sudo_clock/10)
            #pygame.draw.rect(screen, (0,0,255), sprite.rect)
            rect_list.append(sprite.rect)

            if sprite_pass_back.get('text'):
                text_queue.append(sprite_pass_back['text'])
            for group in sprite_groups:
                if sprite in group:
                    group.remove(sprite)
                    collision = pygame.sprite.spritecollideany(sprite, group)
                    if collision:
                        if sprite.collide(collision.rect):
                            for collision in pygame.sprite.groupcollide(sprite_groups[1],
                                                                        sprite_groups[0],
                                                                        False,
                                                                        False)[sprite]:
                                #pygame.draw.rect(screen, (255,0,0,40), collision.rect)
                                #pygame.draw.line(
                                #    SCREEN,
                                #    (255, 128, 40),
                                #    sprite.rect.center,
                                #    collision.rect.center,
                                #    5)
                                if collision.children.get("col"):
                                    if collision.rect.collidepoint(sprite.rect.midbottom) or \
                                        collision.rect.collidepoint(sprite.rect.bottomright) or  \
                                        collision.rect.collidepoint(sprite.rect.bottomleft):
                                        col = [WIDTH/2 - X - 16 - 2, HEIGHT/2 - Y + 16]
                                        collision.children["col"].i, collision.children["col"].j \
                                                = col
                                        collision.children["col"].update(sudo_clock/10)
                                        rect_list.append(collision.children["col"].rect)
                                blocking += sprite.collide(collision.rect)
                    group.add(sprite)
        text_queue = text.update(text_queue)
        #grid(screen, rect_list, 640, 480)
        able_to_move = check_move(blocking)
        #crt_tv(screen, rect_list, 640, 480)
        pygame.draw.rect(SCREEN, (255, 128, 56), cursor, 0)
        pygame.display.update(rect_list)
        if able_to_move:
            #screen.fill((randint(1,255), randint(1,255), randint(1,255)))
            pass
        SCREEN.fill((0, 0, 0, 0))
        # pygame.display.update(rect_list)
        clock.tick(40)
        game_info = "mouse: {m_x} , {m_y}, pos: {x}, {y} fps: {fps}, tile: {tile}".format(
            m_x=cursor.x,
            m_y=cursor.y,
            x=X,
            y=Y,
            fps=clock.get_fps(),
            tile=tiles[current_tile].get("name")
        )
        pygame.display.set_caption(game_info)
        sudo_clock += 1


def crt_tv(screen, rect_list, width, height, flicker=40):
    """ a """
    for i in xrange(height/4):
        pygame.draw.aaline(screen, (120 + randint(0, flicker), 120 + randint(
            0, flicker), 120 + randint(0, flicker)), (0, i * 4), (width, i * 4))

        rect_list.append(pygame.Rect(0, i * 4, 640, 1))


def grid(screen, rect_list, width, height):
    """ a """
    for j in xrange(0, height, SPACING):
        pygame.draw.aaline(screen, (0, 0, 0), (0, Y %
                                               SPACING + j), (width, Y % SPACING + j))
        rect_list.append(pygame.Rect(0, j * SPACING, width, 1))
    for i in xrange(0, width, SPACING):
        pygame.draw.aaline(screen, (0, 0, 0), (X %
                                               SPACING + i, 9), (X % SPACING + i, height))
        rect_list.append(pygame.Rect(i * SPACING, 0, height, 1))


if __name__ == "__main__":
    main()
