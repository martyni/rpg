import pygame
from pygame import event as ev
from copy import deepcopy
from pygame.locals import *
from pprint import pprint
from random import randint
pygame.init()
width, height = 800,800 
screen=pygame.display.set_mode((width, height),DOUBLEBUF|HWSURFACE)

blank_screen = pygame.Surface((width, height))
blank_screen.fill((255,255,255))
verbose = True
speed = 3
x = 0
y = 0
actions = {i: False for i in ["up", "down", "left", "right", "attack", "back"]}
key_map = {
        "up":[111, 134, 126],
        "down": [116, 133, 125],
        "left": [113, 131, 123],
        "right": [114, 132, 124],
        "attack": [8, 0],
        "back": [9, 1]
        }


def log(self, message):
    if verbose:
        #print self , message
        pass


def check_move(blocking):
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

def move(i,j):
  global x
  x += i
  global y
  y += j


def up():
    move(0, speed)

def down():
    move(0, -speed)

def left():
    move(speed, 0)

def right():
    move(-speed,0)

def attack():
    pass

def back():
    pass

def main(background_layers=[], sprites=[], text=None, sprite_groups=None):        
   global screen
   global blank_screen
   text_queue = ["Hello Game", "How are you today?"]
   game=True
   clock = pygame.time.Clock()
   frames = 0
   while game:
       ev.pump()
       blocking = []
       for event in ev.get():
          if event.type==QUIT: 
              game = False
              pygame.display.quit()
              log(__name__, "exiting")
              exit(1)
          elif event.type==VIDEORESIZE:
              width, height = event.dict['size']
              screen=pygame.display.set_mode((width, height),DOUBLEBUF|RESIZABLE,12)
              blank_screen = pygame.Surface((width, height))
              blank_screen.fill((255,255,255))
              [sprite.resize(width, height) for sprite in sprites]
              text.resize(width,height)
   
          elif event.type==KEYDOWN:
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
   
          elif event.type==KEYUP:
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

          elif event.type==20:
              log(__name__, event)
              direction = event.dict.keys()[0]
              actions[direction] = event.dict[direction] 

       for layer in background_layers:
           layer.update()
       sprites = sorted(sprites, None, lambda sprite: (sprite.rect.y, sprite.rect.x))
       rect_list = []
       for sprite in sprites:
           a = sprite.update()
           #pygame.draw.rect(screen, (0,0,255), sprite.rect) 
           rect_list.append(sprite.rect)
           
           if a.get('text'):
               text_queue.append(a['text'])
           for group in sprite_groups:
              if sprite in group:
                 group.remove(sprite) 
                 collision = pygame.sprite.spritecollideany(sprite, group)
                 if collision:
                    #pygame.draw.rect(screen, (255,0,0,40), collision.rect) 
                    blocking = sprite.collide(collision.rect) if sprite.collide(collision.rect) else blocking
                 group.add(sprite)
       text_queue = text.update(text_queue)
       move = check_move(blocking)
       #pygame.display.flip()
       #for group in sprite_groups:
       #   print pygame.sprite.groupcollide(sprite_groups[0], group, False, False)
       #pygame.display.update(background_layers[0].image.get_rect())
       pygame.display.update(rect_list)
       if move:
          #screen.fill((randint(1,255), randint(1,255), randint(1,255)))
          pass
       screen.fill((250,250,250,0))
       #pygame.display.update(rect_list)
       clock.tick()
       pygame.display.set_caption(str(clock.get_fps())) 
       frames += 1 
if __name__ == "__main__":
    main()
