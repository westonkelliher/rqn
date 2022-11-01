import os
import pygame
import math, time
import subprocess as sp
import socket

import control_pad_target as cpt

VERSION_CUTOFF = 13

GUI_SCALE = 2

class Client:
  def __init__(self, s):
    parts = s.split(':')
    dims = parts[1].split(',')
    self.client_id = int(parts[0])
    self.w = int(dims[0])
    self.h = int(dims[1])

    
  def to_string(self):
    return "{}:{},{}".format(self.client_id, self.w, self.h)

  # TODO: def get_spec_str

  

class LaunchEntry:
  def __init__(self, name, executable_strs, func=None):
    self.name = name
    self.executable_strs = executable_strs
    self.func = func

    
  def launch(self):
    if self.func:
      self.func()
    else:
      sp.call(self.executable_strs)

    
    


    
class Launcher:
  def __init__(self, launch_entries):
    pygame.init()
    all_entries = [LaunchEntry("Quit", None, self.quit)]
    all_entries += launch_entries
    while True:
      try:
        self.screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
        break
      except:
        pass
    self.launch_entries = all_entries
    self.selection_index = 0
    self.running = False
    w, h = self.screen.get_size()
    font_size = int(h*GUI_SCALE/27)
    self.font = pygame.font.Font('freesansbold.ttf', font_size)
    self.clients = [ Client(q) for q in cpt.get_client_info().split(';')[:-1] ]
    for c in self.clients:
      cpt.assign_spec(c.to_string(), "]1,100,50,200,140;2,100,200,200,150;3,500,100,200,200;]]")
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
      try:
        s.connect(("8.8.8.8", 80))
        break
      except:
        time.sleep(0.5)
    self.ip = s.getsockname()[0]
    s.close()
    # TODO: def get_clients
    sub_font = pygame.font.Font('freesansbold.ttf', int(24*GUI_SCALE))
    f = open('/home/requin/rqn/version')
    minor_v = f.read().strip()
    f.close()
    v_str = 'v0.2.' + str(int(minor_v) - VERSION_CUTOFF)
    self.version_text = sub_font.render(v_str, True, (40, 40, 40))
    ip_str = ' . '.join(self.ip.split('.'))
    self.ip_text = sub_font.render(ip_str, True, (40, 40, 40), (180, 180, 200))




  def quit(self):
    self.running = False
    
    
  def mainloop(self):
    self.running = True

    while self.running:
      # pygame events
      for event in pygame.event.get():
        if event.type == pygame.QUIT:
          self.running = False
          
      # new or dropped control pad
      if cpt.clients_changed():
        self.clients = [ Client(q) for q in cpt.get_client_info().split(';')[:-1] ]
        for c in self.clients:
          cpt.assign_spec(c.to_string(), "]1,100,50,200,140;2,100,200,200,150;3,500,100,200,200;]]")

      # control pad events
      for c in self.clients:
        for event_str in cpt.get_events(c.to_string()).split(']')[:-1]:
          self.handle_event(event_str)

      # drawing
      self.draw()
    # main loop ended
    
    pygame.quit()

    
  def handle_event(self, event_str):
    parts = event_str.split(':')
    elem_id = int(parts[1].split(',')[0].strip())
    action = parts[2].strip()
    if action == 'Press':
      if elem_id == 1:
        self.selection_index -= 1
        if self.selection_index < 0:
          self.selection_index = len(self.launch_entries)-1
      elif elem_id == 2:
        self.selection_index += 1
        if self.selection_index >= len(self.launch_entries):
          self.selection_index = 0
      elif elem_id == 3:
        self.launch_entries[self.selection_index].launch()
        # re-set controllers to launcher menu controls
        for c in self.clients:
          cpt.assign_spec(c.to_string(), "]1,100,50,200,140;2,100,200,200,150;3,500,100,200,200;]]")

      

    
  def draw(self):
    bg_color = (130, 140, 220)
    hl_color = (170, 180, 240)
    if os.getenv('RED') == 'true':
      bg_color = (130, 100, 20)
      hl_color = (170, 140, 40)

    self.screen.fill(bg_color)

    w, h = self.screen.get_size()

    # ip and version
    self.screen.blit(self.ip_text, (5, 5))
    self.screen.blit(self.version_text, (5, h - 24*GUI_SCALE - 5))
    
    y = 5
    i = 0
    for entry in self.launch_entries:
      bg_color = hl_color if i == self.selection_index else None
      text = self.font.render(entry.name, True, (0, 0, 0), bg_color)
      rect = text.get_rect()
      x = (w - rect.width)/2
      self.screen.blit(text, (x, y))
      y += rect.height + 5
      i += 1
    pygame.display.flip()



def main():
  launch_entries = [
    LaunchEntry("Hello", ['echo', "hello"]),
    LaunchEntry("CodeWords", ['/home/requin/rqn/codewords']),
    LaunchEntry("Planet Run", ['python3', "/home/requin/rqn/planet-run.py"]),
  ]
  launcher = Launcher(launch_entries)
  launcher.mainloop()


if __name__ == '__main__':
  main()
