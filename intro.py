import controls
from controls import pygame, log

def intro():
   intro = True
   pygame.display.set_caption('Intro') 
   while intro:
      print 'looping'
      controls.screen.fill((255,255,0))
      pygame.display.flip() 

print 'hi'
if __name__ == '__main__':
   print 'starting'
   intro()
