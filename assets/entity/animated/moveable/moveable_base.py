#!/usr/bin/env python

from ..animate import Animation
from assets.ui.subpixelsurface import SubPixelSurface

class Moveable(Animation):
  speed_loss = 12
  clamp_cache = {}
  normalise_cache = {}
  
  def __init__(self, x,y, max_d=80, max_dd = 10, sub_level = 4):
    self.sub_level = sub_level
    super(Moveable, self).__init__(x,y)
    self.subsurf = self.surf
    self.dx = 0
    self.max_dx = max_d
    self.ddx = 0
    self.max_ddx = max_dd
    self.dy = 0
    self.max_dy = max_d
    self.ddy = 0
    self.max_ddy = max_dd
    self.max_d = max_d
    self.max_dd = max_dd
    self.move_pos(0)
    
  def run(self, d_time):
    super(Moveable, self).run(d_time)
    moved = self.move(d_time)
    self.dirty = moved
    
  def move(self, d_time):
    if self.ddx == self.ddy == self.dx == self.dy == 0: return False
    self.ddx = self.normalise(self.ddx, self.max_dd*d_time)
    self.ddy = self.normalise(self.ddy, self.max_dd*d_time)
    self.ddx = self.clamp(self.max_ddx, self.ddx)
    self.ddy = self.clamp(self.max_ddy, self.ddy)
    self.dx+=self.ddx*d_time
    self.dy+=self.ddy*d_time
    self.dx = self.normalise(self.dx, self.max_d*d_time)
    self.dy = self.normalise(self.dy, self.max_d*d_time)
    self.dx = self.clamp(self.max_dx, self.dx+self.ddx)
    self.dy = self.clamp(self.max_dy, self.dy+self.ddy)
    moved = self.dx!=0 or self.dy!=0
    if moved: self.move_pos(d_time)
    return moved
  
  def move_pos(self, d_time):
    self.x=max(52, min(433-self.surf.get_width(), self.x+self.dx*d_time))
    self.y=max(52, min(277-self.surf.get_height(), self.y+self.dy*d_time))
    self.surf = self.subsurf.at(self.x, self.y)
  
  def clamp(self, clamp, val):
    h = hash((clamp, val))
    if h in Moveable.clamp_cache:
      return Moveable.clamp_cache[h]
    rtn = max(-clamp, min(clamp, val))
    Moveable.clamp_cache[h] = rtn
    return rtn
  
  def normalise(self, val, amount):
    h = hash((val, amount))
    if h in Moveable.normalise_cache:
      return Moveable.normlise_cache[h]
    orig_sign = cmp(val, 0)
    #print amount
    final = val-orig_sign*amount*self.speed_loss
    new_sign = cmp(final, 0)
    #print val, final, orig_sign, new_sign
    if new_sign != orig_sign:
      Moveable.clamp_cache[h] = 0
      return 0
    Moveable.clamp_cache[h] = final
    return final
  
  def load_surf(self, surf):
    surf = super(Moveable, self).load_surf(surf)
    return SubPixelSurface(surf, self.sub_level)
  