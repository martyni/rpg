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
def log(message):
    if verbose:
        print __name__, message


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

   clock = pygame.time.Clock()
   while True:
       ev.pump()
       for event in ev.get():
   
          if event.type==QUIT: pygame.display.quit()
   
          elif event.type==VIDEORESIZE:
              width, height = event.dict['size']
              screen=pygame.display.set_mode((width, height),HWSURFACE|DOUBLEBUF|RESIZABLE)
   
          elif event.type==KEYDOWN:
              if event.scancode == 111:
                  ev.post(ev.Event(20, {"up": True})) 
              elif event.scancode == 116:
                  ev.post(ev.Event(20, {"down": True})) 
              elif event.scancode == 113:
                  ev.post(ev.Event(20, {"left": True})) 
              elif event.scancode == 114:
                  ev.post(ev.Event(20, {"right": True})) 
   
          elif event.type==KEYUP:
              if event.scancode == 111:
                  ev.post(ev.Event(20, {"up": False})) 
              elif event.scancode == 116:
                  ev.post(ev.Event(20, {"down": False})) 
              elif event.scancode == 113:
                  ev.post(ev.Event(20, {"left": False}))
              elif event.scancode == 114:
                  ev.post(ev.Event(20, {"right": False})) 

          elif event.type==20:
              log(event)
              direction = event.dict.keys()[0]
              action[direction] = event.dict[direction] 
       for layer in background_layers:
           layer.update()
       sprites = sorted(sprites,None, lambda sprite: (sprite.j, sprite.i))
       print [(i.i, i.j) for i in sprites]
       for sprite in sprites:
           sprite.update()
       check_move()
       pygame.display.flip()
       screen.fill((255,255,255,0))
       clock.tick(60)
       
if __name__ == "__main__":
    main()
