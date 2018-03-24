import pygame
from pygame import event as ev
from copy import deepcopy
from pygame.locals import *
from random import randint
pygame.init()
def main(background_layers=[], sprites=[]):        
   width, height = 500, 500
   global screen
   screen=pygame.display.set_mode((width, height),HWSURFACE|DOUBLEBUF|RESIZABLE)
   game = True
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
          print(event)
       
       screen.fill((randint(1,255),randint(1,255),randint(1,255)))
       pygame.display.flip()
       
if __name__ == "__main__":
    main()
