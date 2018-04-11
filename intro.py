import sys, pygame
from pygame.locals import *
from random import choice
pygame.init()


def draw_connected_lines(position_list, event):
   if event.type == MOUSEBUTTONDOWN:
      position_list.append( event.pos)
   if len(position_list) > 1:
      for position in range(len(position_list ) - 1):
         pygame.draw.line(screen, (255,255,255), position_list[position], position_list[position + 1])
   return position_list
   

def intro():
   size = width, height = 640, 480
   screen=pygame.display.set_mode((width, height))
   
   blank_screen = pygame.Surface((width, height))
   blank_screen.fill((255,255,255))
   
   speed = [2, 2]
   black = 0, 0, 0
   intro1 = pygame.transform.scale(pygame.image.load("assets/images/Title01.bmp").convert_alpha(), size)
   intro2 = pygame.transform.scale(pygame.image.load("assets/images/Title02.bmp").convert_alpha(), size)
   loading = pygame.transform.scale(pygame.image.load("assets/images/Loading01.bmp").convert_alpha(), size)
   intro = True
   position_list = []       
   counter = 0
   while intro:
       if not counter % 10:  
          screen.fill(black)
          screen.blit(choice([intro1, intro2]),(0,0) )
       for event in pygame.event.get():
           if event.type == pygame.QUIT: 
              sys.exit()
           elif event.type==KEYDOWN:
              intro = False 
              screen.fill(black)
       pygame.display.flip()
       counter += 1
   screen.fill(black)
   screen.blit(loading,(0,0) )
   pygame.display.flip()
   
   
if __name__ == '__main__':
   intro()
