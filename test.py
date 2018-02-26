import pygame
from pygame import event as ev
from copy import deepcopy
from pygame.locals import *
pygame.init()
width, height = 500, 500
screen=pygame.display.set_mode((width, height),DOUBLEBUF|RESIZABLE)
def main(background_layers=[], sprites=[]):        
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
   
          print event
       
if __name__ == "__main__":
    main()
