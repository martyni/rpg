import pygame
from pygame import event as ev
from copy import deepcopy
from pygame.locals import *
pygame.init()
width, height = 500, 500
screen=pygame.display.set_mode((width, height),DOUBLEBUF|RESIZABLE)
verbose = True
speed = 3
x = 0
y = 0
actions = {i: False for i in ["up", "down", "left", "right", "attack", "back"]}
key_map = {
        "up":[111, 134],
        "down": [116, 133],
        "left": [113, 131],
        "right": [114, 132],
        "attack": [8],
        "back": [9]
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
              screen=pygame.display.set_mode((width, height),HWSURFACE|DOUBLEBUF|RESIZABLE)
              [sprite.resize(width, height) for sprite in sprites]
   
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
       pygame.display.flip()
       screen.fill((255,255,255,0))
       clock.tick(25)
       
if __name__ == "__main__":
    main()
