import pygame
from pygame import event as ev
from copy import deepcopy
from pygame.locals import *
pygame.init()
width, height = 500, 500
screen=pygame.display.set_mode((width, height),HWSURFACE|DOUBLEBUF|RESIZABLE)
verbose = True
speed = 1
x = 0
y = 0
action = {i: False for i in ["up", "down", "left", "right"]}
key_map = {
        "up":[111, 134],
        "down": [116, 133],
        "left": [113, 131],
        "right": [114, 132]
        }
def log(message):
    if verbose:
        print __name__ , message


def check_move():
    funcs = {
            "up": up,
            "down": down,
            "left": left,
            "right": right
            }

    for i in action:
        if action[i]:
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

def main(background_layers=[], sprites=[]):        
   global screen

   game=True
   clock = pygame.time.Clock()
   while game:
       ev.pump()
       for event in ev.get():
          if event.type==QUIT: 
              game = False
              pygame.display.quit()
              log("exiting")
              exit(1)
          elif event.type==VIDEORESIZE:
              width, height = event.dict['size']
              screen=pygame.display.set_mode((width, height),HWSURFACE|DOUBLEBUF|RESIZABLE)
   
          elif event.type==KEYDOWN:
              if event.scancode in key_map["up"]:
                  ev.post(ev.Event(20, {"up": True})) 
              elif event.scancode in key_map["down"]:
                  ev.post(ev.Event(20, {"down": True})) 
              elif event.scancode in key_map["left"]:
                  ev.post(ev.Event(20, {"left": True})) 
              elif event.scancode in key_map["right"]:
                  ev.post(ev.Event(20, {"right": True})) 
   
          elif event.type==KEYUP:
              if event.scancode in key_map["up"]:
                  ev.post(ev.Event(20, {"up": False})) 
              elif event.scancode in key_map["down"]:
                  ev.post(ev.Event(20, {"down": False})) 
              elif event.scancode in key_map["left"]:
                  ev.post(ev.Event(20, {"left": False}))
              elif event.scancode in key_map["right"]:
                  ev.post(ev.Event(20, {"right": False})) 

          elif event.type==20:
              log(event)
              direction = event.dict.keys()[0]
              action[direction] = event.dict[direction] 

       for layer in background_layers:
           layer.update()
       sprites = sorted(sprites,None, lambda sprite: (sprite.j, sprite.i))
       log([(i.i, i.j) for i in sprites])
       for sprite in sprites:
           sprite.update()
       check_move()
       pygame.display.flip()
       screen.fill((255,255,255,0))
       clock.tick(60)
       
if __name__ == "__main__":
    main()
