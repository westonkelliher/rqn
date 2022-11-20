import pygame
import math, time
import subprocess as sp
import socket


GUI_SCALE = 2

  

def draw(screen, failure=False):
  screen.fill((60, 160, 110))
  
  w, h = screen.get_size()

  font = pygame.font.Font('freesansbold.ttf', int(32*GUI_SCALE))
  text = font.render('Loading', True, (0, 0, 0), None)
  rect = text.get_rect()
  x = (w - rect.width)/2
  y = 50
  screen.blit(text, (x, y))
  
  if failure:
    font2 = pygame.font.Font('freesansbold.ttf', int(24*GUI_SCALE))
    text2 = font2.render('Failed to connect to WiFi', True, (0, 0, 0), None)
    rect2 = text2.get_rect()
    x2 = (w - rect2.width)/2
    y2 = y + rect.height + 20
    screen.blit(text2, (x2, y2))
    
  pygame.display.flip()



def main():
  pygame.init()
  screen = None
  while True:
    try:
      screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
      break
    except:
      time.sleep(.3)
      print('Re-Attempting to set display', flush=True)
      pass
  draw(screen)
  time.sleep(1.5)

  num_tries = 0
  s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  while True:
    if num_tries == 6:
      draw(screen, failure=True)
    try:
      s.connect(("8.8.8.8", 80))
      break
    except:
      time.sleep(0.5)
    num_tries += 1
  pygame.quit()
  

if __name__ == '__main__':
  main()
