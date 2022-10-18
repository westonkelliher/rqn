import pygame
import math, time
import copy
import control_pad_target as cpt

WIDTH, HEIGHT = 1000, 800


def pale(color, i):
  a, b, c = color
  new_col = ((a+240*i)/(i+1),
             (b+240*i)/(i+1),
             (c+240*i)/(i+1))
  return new_col



class Dot():
  def __init__(self, x, y, dx, dy, m, color=(100,100,100), fixed=False,
               name=''):
    self.x = x
    self.y = y
    self.dx = dx
    self.dy = dy
    self.m = m
    self.r =1.5*(1+math.sqrt(self.m))
    self.color = color
    self.fixed = fixed
    self.name = name
    self.old_locations = [(-100,-100)]*10
    self.trapped = None

  def speed(self):
    return math.sqrt(self.dx**2 + self.dy**2)
    
  def tick(self):
    self.old_locations.insert(0, (self.x, self.y))
    self.old_locations = self.old_locations[:-1]
    self.x += self.dx
    self.y += self.dy
    if not self.fixed:
      #damping
      self.dx *= .999
      self.dy *= .999
    if self.trapped:
      if self.x < self.trapped.x1+self.r:
        self.x = self.trapped.x1+self.r
        self.dx = abs(self.dx)
      elif self.x > self.trapped.x2-self.r:
        self.x = self.trapped.x2-self.r
        self.dx = -abs(self.dx)
      if self.y < self.trapped.y1+self.r:
        self.y = self.trapped.y1+self.r
        self.dy = abs(self.dy)
      elif self.y > self.trapped.y2-self.r:
        self.y = self.trapped.y2-self.r
        self.dy = -abs(self.dy)
      return
    #wall collision
    if self.x > WIDTH:
      self.x = WIDTH
      self.dx *= -1
      if not self.fixed:
        self.dx /= 2
    elif self.x < 0:
      self.x = 0
      self.dx *= -1
      if not self.fixed:
        self.dx /= 2
    if self.y > HEIGHT:
      self.y = HEIGHT
      self.dy *= -1
      if not self.fixed:
        self.dy /= 2
    elif self.y < 0:
      self.y = 0
      self.dy *= -1
      if not self.fixed:
        self.dy /= 2

  def apply_acc(self, ax, ay):
    self.dx += ax
    self.dy += ay


  def dist_to(self, d2):
    a = self.x - d2.x
    b = self.y - d2.y
    return math.sqrt(a**2 + b**2)

  def acc_from(self, d2):
    dist = self.dist_to(d2)
    try:
      a = (d2.x - self.x)/dist #normalized
      b = (d2.y - self.y)/dist
    except:
      return 0, 0 # lazy avoid div by 0
    if dist < 15:
      return 0, 0 # when it's real close don't accelerate because too crazy
    dist += 15
    #dist = math.pow(dist, -.32)*100
    return a*d2.m/(dist*self.r), b*d2.m/(dist*self.r)

  def is_hitting(self, d2):
    return self.dist_to(d2) < self.r + d2.r
    
  def draw(self, screen):
    pygame.draw.circle(screen, self.color, (self.x, self.y),
                       self.r)

  def draw_tail(self, screen):
    a, b, c = self.color
    for i in range(len(self.old_locations), 0, -1):
      loc = self.old_locations[i-1]
      col = pale(self.color, i)
      pygame.draw.circle(screen, col, loc,
                         self.r)


class Zone():
  def __init__(self, bounds, balls=1, color=(150, 250, 150), id=''):
    self.x1 = bounds[0]
    self.y1 = bounds[1]
    self.x2 = bounds[2]
    self.y2 = bounds[3]
    self.balls_needed = balls
    self.balls = 0
    self.color = pale(color, 1.5)
    self.id = id

  def dot_within(self, dot):
    return (dot.x > self.x1+dot.r and dot.x < self.x2-dot.r and
            dot.y > self.y1+dot.r and dot.y < self.y2-dot.r)


    
  

PLAYER_ACC = 0.09
PLAYER_MAX_SPD = 2.8
# dots[0] is the player and dots[1] is the ball
class Level():
  def __init__(self, dots, zones, text, ):
    self.dots = copy.deepcopy(dots)
    self.OG_dots = copy.deepcopy(dots)
    self.zones = copy.deepcopy(zones)
    self.OG_zones = copy.deepcopy(zones)
    self.text = text
    self.stickx = 0
    self.sticky = 0
    self.state = 'playing'

  def reset(self):
    self.dots = copy.deepcopy(self.OG_dots)
    self.zones = copy.deepcopy(self.OG_zones)
    self.state = 'playing'


  def lose(self):
    self.stickx = 0
    self.sticky = 0
    self.state = 'lost'
    self.dots[0].color = (50, 60, 100)

  def win(self):
    self.stickx = 0
    self.sticky = 0
    self.state = 'won'

  def did_win(self):
    for zone in self.zones:
      if zone.balls < zone.balls_needed:
        return False
    return True
    
  def draw_zones(self, screen):
    for z in self.zones:
      pygame.draw.rect(screen, pale(z.color, 2),
                       pygame.Rect(z.x1, z.y1, z.x2-z.x1, z.y2-z.y1))
      pygame.draw.rect(screen, z.color,
                       pygame.Rect(z.x1, z.y1, z.x2-z.x1, z.y2-z.y1), 2)
      if z.balls == z.balls_needed:
        pygame.draw.rect(screen, (20, 20, 20),
                         pygame.Rect(z.x1, z.y1, z.x2-z.x1, z.y2-z.y1), 1)
        
      
  def draw_dots(self, screen):
    for d in reversed(self.dots):
      d.draw(screen)

  def draw_tails(self, screen):
    for d in self.dots:
      d.draw_tail(screen)

  def draw_text(self, screen):
    font = pygame.font.SysFont(None, 24)
    for i, text in enumerate(self.text):
      img = font.render(text, True, (120, 120, 120))
      screen.blit(img, ((WIDTH-img.get_width())/2, 15+i*26))

  def handle_event(self, eventstr):
    if self.state != 'playing':
      return
    if 'Move' in eventstr:
      # TODO parse_event function that returns an object of control_pad_event python class
      parts = eventstr.split('Move')[1].split(',')
      self.stickx = float(parts[0].split('(')[1].strip())
      self.sticky = float(parts[1].split(')')[0].strip())


  def update_dots(self):
    for d1 in self.dots:
      if d1.fixed:
        continue
      ax, ay = 0, 0
      for d2 in self.dots:
        if d1 == d2:
          continue
        
        qax, qay = d1.acc_from(d2)
#        if (d1.name == 'C' and d2.name == 'A' or
#            d1.name == 'A' and d2.name == 'C'):
#          qax *= -1
#          qay *= -1
        ax += qax
        ay += qay
      d1.apply_acc(ax, ay)
      d1.tick()

  def account_for_collisions(self):
    global MYLIST
    for d1 in self.dots:
      for d2 in self.dots:
        if d1 == d2:
          continue
        if 'player' in d1.name and 'deadly' in d2.name:
          if d1.is_hitting(d2):
            self.lose()
      if 'ball' in d1.name:
        ball_id = d1.name.split('ball')[-1]
        for zone in self.zones:
          if (ball_id == zone.id and zone.dot_within(d1) and
              not d1.trapped and not zone.balls == zone.balls_needed):
            d1.trapped = True # have to do this because python is seriously fucked
            d1.trapped = zone
            zone.balls += 1
            if self.did_win():
              self.win()
          

  def tick(self):
    # limit speed
    if self.dots[0].speed() > PLAYER_MAX_SPD:
      self.dots[0].dx *= .9
      self.dots[0].dy *= .9
    # movement control
    self.dots[0].apply_acc(self.stickx*PLAYER_ACC, self.sticky*PLAYER_ACC)
    self.update_dots()
    # things happenning
    if self.state == 'playing':
      self.account_for_collisions()


    
def dist(d1, d2):
  a = d1.x - d2.x
  b = d1.y - d2.y
  return math.sqrt(a**2 + b**2)


def draw_win(screen):
  # box
  w = 350
  h = 100
  x = (WIDTH-w)/2
  y = (HEIGHT-h)/2
  pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(x, y, w, h))
  pygame.draw.rect(screen, (100, 140, 100), pygame.Rect(x, y, w, h), 2)

  # text
  font = pygame.font.SysFont(None, 36)
  img = font.render('Nice!', True, (20, 20, 20))
  tx = x+(w-img.get_width())/2
  screen.blit(img, (tx, y+15))
  img = font.render('Press Space for Next Level', True, (20, 20, 20))
  tx = x+(w-img.get_width())/2
  screen.blit(img, (tx, y+50))

def draw_lose(screen):
  # box
  w = 350
  h = 100
  x = (WIDTH-w)/2
  y = (HEIGHT-h)/2
  pygame.draw.rect(screen, (150, 150, 150), pygame.Rect(x, y, w, h))
  pygame.draw.rect(screen, (140, 100, 100), pygame.Rect(x, y, w, h), 2)

  # text
  font = pygame.font.SysFont(None, 36)
  img = font.render('You lost!', True, (20, 20, 20))
  tx = x+(w-img.get_width())/2
  screen.blit(img, (tx, y+15))
  img = font.render('Press Space to Restart Level', True, (20, 20, 20))
  tx = x+(w-img.get_width())/2
  screen.blit(img, (tx, y+50))
  

    

def xywh(x, y, w, h):
  x1 = x - w/2
  x2 = x + w/2
  y1 = y - h/2
  y2 = y + h/2
  return (x1, y1, x2, y2)
  
def main():

  #cpt.initiate("1001,20,30,100,100;]1002,550,200,120;")#1003,380,300,50;")
  
  # colors
  playercolor = (20, 50, 250)
  green = (10, 200, 30)
  red = (200, 20, 20)
  brown = (110, 90, 70)
  yellow = (180, 200, 30)
  purple = (200, 20, 150)

  # player planets
  player0 = Dot(900, 100, 0, 0, 10, color=playercolor, name='player')
  player1 = Dot(100, 100, 0, 0, 10, color=playercolor, name='player')
  player2 = Dot(200, 650, 0, 0, 10, color=playercolor, name='player')
  player7 = Dot(500, 400, 0, 0, 8, color=playercolor, name='player')
  player8 = Dot(50, 400, 0, 0, 10, color=playercolor, name='player')
  player9 = Dot(350, 350, 0, 0, 11, color=playercolor, name='player')
  player10 = Dot(150, 380, 0.5, 0, 10, color=playercolor, name='player')
  player11 = Dot(500, 400, 0, 0, 10, color=playercolor, name='player')
  player12 = Dot(150, 150, 0, 0, 12, color=playercolor, name='player')

  # goal planets
  rball0 = Dot(800, 100, .5, 0, 8, color=red, name='deadlyballA')
  gball1 = Dot(200, 600, .5, 0, 8, color=green, name='ballA')
  rball1 = Dot(100, 700, .5, 0, 8, color=red, name='deadlyballA')
  rball2 = Dot(500, 400, 0, 0, 70, color=red, name='deadlyballA')
  gball4 = Dot(500, 450, 1.0, 0, 8,  color=green, name='ballG')
  rball4 = Dot(500, 350, -1.0, 0, 8, color=red, name='deadlyballR')
  gball7 = Dot(100, 400, 0, 0, 4,  color=green, name='ballG')
  yball7 = Dot(900, 400, 0, 0, 4,  color=yellow, name='ballY')
  rball7 = Dot(500, 100, 0, 0, 4, color=red, name='deadlyballR')
  pball7 = Dot(500, 700, 0, 0, 4, color=purple, name='deadlyballP')
  rball8a = Dot(200, 10, 0, 0, 4, color=red, name='adeadlyballR')
  rball8b = Dot(500, 10, 0, 0, 4, color=red, name='bdeadlyballR')
  rball8c = Dot(800, 10, 0, 0, 4, color=red, name='cdeadlyballR')
  rball8d = Dot(200, 990, 0, 0, 4, color=red, name='ddeadlyballR')
  rball8e = Dot(500, 990, 0, 0, 4, color=red, name='edeadlyballR')
  rball8f = Dot(800, 990, 0, 0, 4, color=red, name='fdeadlyballR')
  gball9a = Dot(50, 400, -0.5, 0, 10, color=green, name='ballG')
  gball9b = Dot(950, 400, 0, 0, 25, color=green, name='ballG')
  rball10 = Dot(850, 380, .5, 0, 5, color=red, name='deadlyballR')
  gball11a = Dot(200, 200, -.2, .2, 4, color=green, name='ballG')
  gball11b = Dot(800, 200, .2, .2, 4, color=green, name='ballG')
  gball11c = Dot(200, 600, -.2, -.2, 4, color=green, name='ballG')
  gball11d = Dot(800, 600, .2, -.2, 4, color=green, name='ballG')
  gball12a = Dot(890, 640, .05, .15, 2, color=green, name='ballG')
  gball12b = Dot(890, 642, .05, .16, 2, color=green, name='ballG')
  gball12c = Dot(890, 644, .05, .17, 2, color=green, name='ballG')
  

  # obstacle planets
  fixed5  = Dot(500, 400, 0, 0, 12, color=brown, fixed = True, name='fixed')
  fixed10a = Dot(150, 400, 0, 0, 36, color=brown, fixed = True, name='fixed')
  fixed10b = Dot(850, 400, 0, 0, 20, color=brown, fixed = True, name='fixed')
  fixed11a = Dot(150, 100, 0, 0, 25, color=brown, fixed = True, name='fixed')
  fixed11b = Dot(850, 100, 0, 0, 25, color=brown, fixed = True, name='fixed')
  fixed11c = Dot(150, 700, 0, 0, 25, color=brown, fixed = True, name='fixed')
  fixed11d = Dot(850, 700, 0, 0, 25, color=brown, fixed = True, name='fixed')
  fixed12a = Dot(420, 500, 0, 0, 13, color=brown, fixed = True, name='fixed')
  fixed12b = Dot(580, 580, 0, 0, 14, color=brown, fixed = True, name='fixed')
  fixed12c = Dot(740, 620, 0, 0, 15, color=brown, fixed = True, name='fixed')
  fixed12d = Dot(900, 640, 0, 0, 17, color=brown, fixed = True, name='fixed')
  fixed12e = Dot(960, 640, 0, 0, 8, color=brown, fixed = True, name='fixed')
  fixed12f = Dot(320, 400, 0, 0, 10, color=brown, fixed = True, name='fixed')
  
  # zones
  gzone0 = Zone((730, 120, 780, 170), color=green, id='A')
  rzone0 = Zone((830, 120, 880, 170), color=red, id='A')
  rzone3 = Zone((730, 120, 880, 270), color=red, id='A')
  gzone4 = Zone((10, 350, 90, 430), color=green, id='G')
  rzone4 = Zone((910, 350, 990, 430), color=red, id='R')
  gzone5 = Zone((10, 250, 90, 330), color=green, id='G')
  rzone5 = Zone((910, 450, 990, 530), color=red, id='R')
  gzone7 = Zone(xywh(50, HEIGHT/2, 80, 80), color=green, id='G')
  yzone7 = Zone(xywh(WIDTH-50, HEIGHT/2, 80, 80), color=yellow, id='Y')
  rzone7 = Zone(xywh(WIDTH/2, 50, 80, 80), color=red, id='R')
  pzone7 = Zone(xywh(WIDTH/2, HEIGHT-50, 80, 80), color=purple, id='P')
  rzone8 = Zone(xywh(800, 400, 100, 100), balls=6, color=red, id='R')
  gzone9a = Zone(xywh(200, 400, 100, 100), color=green, id='G')
  gzone9b = Zone(xywh(800, 400, 18, 18), color=green, id='G')
  rzone10 = Zone(xywh(200, 250, 80, 80), color=red, id='R')
  gzone11 = Zone(xywh(500, 400, 100, 100), balls=4, color=green, id='G')
  gzone12 = Zone(xywh(240, 300, 100, 100), balls=3, color=green, id='G')


  
  # level texts
  level1_text = ['Use the arrow keys to control the blue planet',
                 'Guide the green planet to the green zone']
  level2_text = ['Guide the red planet to the red zone',
                 'But don\'t let it touch you :O']
  level3_text = ['Oh a big one!']
  level4_text = ['Pretty self explanatory tbh']
  level5_text = ['Brown doesn\'t move']
  level6_text = ['This could get tricky']
  level7_text = ['', '', '', '',
                 'Yellow planets are like green planets: friends!',
                 'Purple planets are like red planets: hurty friends!']
  level8_text = ['Everybody in!']
  level9_text = ['If it fits it ships',
                 '(press \'R\' to restart)']
  level10_text = ['"To become an astronaut one only need run fast enough" \
-Abe Lincoln']
  level11_text = ['Round \'em up']
  level12_text = ['For a second there you thought this would be easy',
                  'This is the final level so I couldn\'t go easy on ya']


  # levels
  level0 = Level([player0, rball0], [rzone0], level1_text)
  level1 = Level([player2, gball1], [gzone0], level1_text)
  level2 = Level([player2, rball1], [rzone0], level2_text)
  level3 = Level([player1, rball2], [rzone3], level3_text)
  level4 = Level([player1, rball4, gball4], [rzone4, gzone4], level4_text)
  level5 = Level([player1, gball4, fixed5], [gzone5],
                 level5_text)
  level6 = Level([player1, rball4, gball4, fixed5], [rzone5, gzone5],
                 level6_text)
  level7 = Level([player7, rball7, gball7, yball7, pball7],
                 [rzone7, gzone7, yzone7, pzone7],
                 level7_text)
  level8 = Level([player8,
                  rball8a, rball8b, rball8c, rball8d, rball8e, rball8f],
                 [rzone8],
                 level8_text)
  level9 = Level([player9, gball9a, gball9b], [gzone9a, gzone9b],
                 level9_text)
  level10 = Level([player10, rball10, fixed10a, fixed10b], [rzone10],
                 level10_text)
  level11 = Level([player11, gball11a, gball11b, gball11c, gball11d,
                   fixed11a, fixed11b, fixed11c, fixed11d],
                  [gzone11],
                 level11_text)
  level12 = Level([player12, gball12a, gball12b, gball12c,
                   fixed12a, fixed12b, fixed12c, fixed12d, fixed12e, fixed12f],
                  [gzone12],
                 level12_text)

  all_levels = [level1, level2, level3, level4, level5, level6, level11,
                level8, level7, level9, level10, level12]


  # pygame stuff
  pygame.init()
  pygame.display.set_caption("Grav Go")
  clock = pygame.time.Clock()
    
  
  screen = pygame.Surface((WIDTH,HEIGHT))
  fscreen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
  fscreen.fill((0, 0, 0))
  
  running = True

  level_index = 0
  level = all_levels[level_index]
  dots = level.dots

  font = pygame.font.SysFont(None, 16)
  reset_img = font.render('Press \'R\' to reset', True, (180, 180, 180))

  
  #leftovers = cpt.get_client_info() # clear out anythin in dims
  #print("leftover dims: {}", leftovers)
  clients = []
      
  while running:
    clock.tick(60)

    if cpt.clients_changed():
      clients = []
      for cli_str in cpt.get_client_info().split(";")[:-1]:
        clients.append(cli_str)
      print(clients);
      for cli_str in clients:
        clid = int(cli_str.split(':')[0])
        if clid  == 0:
          cpt.assign_spec(cli_str, "]1001,20,30,100,100;]1002,550,200,120;") # TODO spec_from_dims
        else:
          cpt.assign_spec(cli_str, "]1001,20,30,100,100;]")
        print("Assigned spec for player " + str(clid))
    

    
    # control pad events
    for cli_str in clients:
      for eventstr in cpt.get_events(cli_str).split(']')[:-1]:
        if 'Press' in eventstr:
          if level.state == 'won':
            level_index += 1
            level = all_levels[level_index]
          else:
            level.reset()
        level.handle_event(eventstr)

    # keyboard events
    endit = False
    for event in pygame.event.get():
      if event.type == pygame.KEYDOWN and event.key == ord('w'):
        level.win()
      if event.type == pygame.QUIT:
        endit = True
        break;
    if endit:
      break
  

    # do things
    level.tick()
    screen.fill((240, 240, 240))
    
    screen.blit(reset_img, (WIDTH - 100, HEIGHT - 20))
    
    level.draw_zones(screen)
    level.draw_text(screen)
    level.draw_tails(screen)
    level.draw_dots(screen)

    if level.state == 'won':
      draw_win(screen)
    elif level.state == 'lost':
      draw_lose(screen)

    fsx,fsy = fscreen.get_size()
    sx = (fsx - WIDTH)/2
    sy = (fsy - HEIGHT)/2
    fscreen.blit(screen, (sx, sy))
    pygame.display.flip()
        
            
if __name__=="__main__":
    main()
