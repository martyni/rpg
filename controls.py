import pygame
from pygame import event as ev
from copy import deepcopy
from pygame.locals import *
pygame.init()
width, height = 900,900 
screen=pygame.display.set_mode((width, height),DOUBLEBUF)

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


def check_move():
    funcs = {
            "up": up,
            "down": down,
            "left": left,
            "right": right,
            "attack": attack,
            "back": back
            }

    for i in actions:
        if actions[i]:
            funcs[i]()

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

def main(background_layers=[], sprites=[], text=None):        
   global screen
   global blank_screen
   text_queue = ["Hello Game", "How are you today?"]
   game=True
   clock = pygame.time.Clock()
   while game:
       ev.pump()
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
       sprites = sorted(sprites,None, lambda sprite: (sprite.j, sprite.i))
       for sprite in sprites:
           a = sprite.update()
           if a.get('text'):
               text_queue.append(a['text'])
       text_queue = text.update(text_queue)
       check_move()
       #pygame.display.flip()
       pygame.display.update(background_layers[0].image.get_rect())
       screen.fill((255,255,255))
       clock.tick(25)
       #print clock.get_fps()
       
if __name__ == "__main__":
    main()
