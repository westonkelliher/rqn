import os
import pygame
import math, time
import subprocess as sp
import socket
import json

import control_pad_target as cpt

# cutoffs of minor versions (numbers in between are patches)
VERSION_CUTOFFS = [
  13, # OTA updates working
  16, # JSON IO and WebCP
]

GUI_SCALE = 2

class Client:
  def __init__(self, s):
    q = json.loads(s)
    self.client_id = q['id']
    self.w = q['w']
    self.h = q['h']

    
  def to_string(self):
    return '{{"w":{},"h":{},"id":{}}}'.format(self.w, self.h, self.client_id)

  def get_json_spec(self):
    btn_up = '{{"id":{},"x":{},"y":{},"w":{},"h":{},"depressed":false}}'.format(
      1, int(self.w*1/8), int(self.h*1/9), int(self.h*3/9), int(self.h*3/9)
    )
    btn_down = '{{"id":{},"x":{},"y":{},"w":{},"h":{},"depressed":false}}'.format(
      2, int(self.w*1/8), int(self.h*5/9), int(self.h*3/9), int(self.h*3/9)
    )
    btn_go = '{{"id":{},"x":{},"y":{},"w":{},"h":{},"depressed":false}}'.format(
      3, int(self.w*5/8), int(self.h*2/9), int(self.h*5/9), int(self.h*5/9)
    )
    panels       = '"panels":[]'
    buttons      = '"buttons":[{},{},{}]'.format(btn_up, btn_down, btn_go)
    joysticks    = '"joysticks":[]'
    joystickpads = '"joystickpads":[]'
    json_str = '{{{},{},{},{}}}'.format(panels, buttons, joysticks, joystickpads)
    return json_str

  

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
    # restore resolution in case app changed it
    set_screen_res()


# change resolution to 1920x1080
# TODO: screens that don't support 1920x1080 or don't make sense for it
def set_screen_res():
  sp.call(['xrandr', '-s', '1920x1080'])
  #sp.call(['xrandr', '--output', '$(xrandr -q | grep " connected" | cut -f1 -d" " | head -1)', '--mode', '1920x1080'])

    
class Launcher:
  def __init__(self, launch_entries):
    set_screen_res()
    pygame.init()
    all_entries = [LaunchEntry("Quit", ['/sbin/shutdown', '0'])]
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
    self.clients = [ Client(q) for q in cpt.get_client_info().split('\n')[:-1] ]
    for c in self.clients:
      cpt.assign_spec(c.to_string(), c.get_json_spec())
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
    patch_v = f.read().strip()
    f.close()
    v_str = 'v0.' + str(len(VERSION_CUTOFFS)+1) + '.' + str(int(patch_v) - VERSION_CUTOFFS[-1])
    self.version_text = sub_font.render(v_str, True, (40, 40, 40))
    ip_str = ' . '.join(self.ip.split('.')) + ' : 3000'
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
        self.clients = [ Client(q) for q in cpt.get_client_info().split('\n')[:-1] ]
        for c in self.clients:
          cpt.assign_spec(c.to_string(), c.get_json_spec())

      # control pad events
      for c in self.clients:
        for event_str in cpt.get_events(c.to_string()).split('\n')[:-1]:
          self.handle_event(event_str)

      # drawing
      self.draw()
    # main loop ended
    
    pygame.quit()

    
  def handle_event(self, event_str):
    e = json.loads(event_str)
    if e['datum'] == 'Press':
      if e["element_id"] == 1:
        self.selection_index -= 1
        if self.selection_index < 0:
          self.selection_index = len(self.launch_entries)-1
      elif e["element_id"] == 2:
        self.selection_index += 1
        if self.selection_index >= len(self.launch_entries):
          self.selection_index = 0
      elif e["element_id"] == 3:
        app = self.launch_entries[self.selection_index]
        app.launch()
        # re-set controllers to launcher menu controls after app exits
        for c in self.clients:
          cpt.assign_spec(c.to_string(), c.get_json_spec())

      

    
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
    LaunchEntry("Planet Run", ['echo', 'Planet Run out of service']),
  ]
  launcher = Launcher(launch_entries)
  launcher.mainloop()


if __name__ == '__main__':
  main()
