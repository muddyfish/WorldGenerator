#!/usr/bin/env python

from ..animate import Animation

class Moveable(Animation):
  speed_loss = 1600
  max_d = 128
  dd = 96
  no_acc = False
  auto_clamp = True
  clamp_cache = {}
  
  LEFT_BOUND  = 32
  RIGHT_BOUND = 400
  UP_BOUND    = 32
  DOWN_BOUND  = 240
  
  def __init__(self, x,y):
    super(Moveable, self).__init__(x,y)
    self.subsurf = self.surf
    self.dx = self.ddx = self.dy = self.ddy = 0
    self.max_dx = self.max_d
    self.max_dy = self.max_d
    self.cddx = 0
    self.cddy = 0
    if self.auto_clamp: self.move_pos(0)
    if self.no_acc: self.move = self.move_speed
    
  def run(self, d_time):
    super(Moveable, self).run(d_time)
    self.moved = self.move(d_time)
    self.dirty = self.dirty or self.moved
    
  def move(self, d_time):
    self.ddx = self.cddx
    self.ddy = self.cddy
    if self.ddx == self.ddy == self.dx == self.dy == 0: return False
    if cmp(self.ddx,0) != cmp(self.dx, 0): self.dx = 0 # Stop if moving the opposite direction
    if cmp(self.ddy,0) != cmp(self.dy, 0): self.dy = 0
    self.dx+=self.ddx*d_time
    self.dy+=self.ddy*d_time
    self.dx = self.normalise(self.dx, d_time)
    self.dy = self.normalise(self.dy, d_time,y=True)
    return self.move_speed(d_time)
  
  def move_speed(self, d_time):
    self.dx = self.clamp(self.max_dx, self.dx)
    self.dy = self.clamp(self.max_dy, self.dy)
    moved = self.dx!=0 or self.dy!=0
    if moved: self.move_pos(d_time)
    return moved
  
  def move_pos(self, d_time):
    if hasattr(self, "x_pos"):
      #x_pos and y_pos are the center of the image so take that into account
      
      x,y = self.x_pos+self.dx*d_time, self.y_pos+self.dy*d_time
      max_x = Moveable.LEFT_BOUND+self.rect.width *1.25 + self.bounding_rect.x/2
      min_x = Moveable.RIGHT_BOUND+self.rect.width/4 + self.bounding_rect.x/2
      max_y = Moveable.UP_BOUND  +self.rect.height*1.25 + self.bounding_rect.y/2
      min_y = Moveable.DOWN_BOUND +self.rect.height/4+ self.bounding_rect.y/2
      self.x_pos=max(max_x, min(min_x,  x))
      self.y_pos=max(max_y, min(min_y, y))
      #self.surf = self.subsurf.at(self.x_pos, self.y_pos)
      if x!=self.x_pos or y!=self.y_pos:
        if y!=self.y_pos:
          if self.y_pos == max_x:wall_id = 0
          else:                  wall_id = 1
        else:
          if self.x_pos == max_y:wall_id = 2
          else:                  wall_id = 3
        self.get_databin().ai_events.collide_wall.is_called(self, wall_id)
    else:
      #Otherwise just do a straight transformation on x and y which are based on (0,0) coords
      x,y = self.x+self.dx*d_time, self.y+self.dy*d_time
      self.x=max(Moveable.LEFT_BOUND, min(Moveable.RIGHT_BOUND-self.rect.width,  x))
      self.y=max(Moveable.UP_BOUND,   min(Moveable.DOWN_BOUND- self.rect.height, y))
      #self.surf = self.subsurf.at(self.x, self.y)
      if x!=self.x or y!=self.y:
        if y!=self.y:
          if self.y == Moveable.UP_BOUND:   wall_id = 0
          else:                             wall_id = 1
        else:
          if self.x == Moveable.LEFT_BOUND: wall_id = 2
          else:                             wall_id = 3
        self.get_databin().ai_events.collide_wall.is_called(self, wall_id)
    self.get_databin().ai_events.player_xy.is_called(self)
  
  def clamp(self, clamp, val):
    h = hash((clamp, val))
    if h in Moveable.clamp_cache:
      return Moveable.clamp_cache[h]
    rtn = max(-clamp, min(clamp, val))
    Moveable.clamp_cache[h] = rtn
    return rtn
  
  def normalise(self, val, amount, y=False):
    if getattr(self, ["ddx","ddy"][y]) != 0.0:
      return val
    orig_sign = cmp(val, 0)
    final = val-orig_sign*amount*self.speed_loss
    new_sign = cmp(final, 0)
    if new_sign != orig_sign:
      return 0
    return final
  