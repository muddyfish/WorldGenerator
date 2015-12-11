#!/usr/bin/env python

from ..animate import Animation
from assets.ui.subpixelsurface import SubPixelSurface

class Moveable(Animation):
  speed_loss = 1600
  dd = 128
  clamp_cache = {}
  
  def __init__(self, x,y, max_d=96, sub_level = 3):
    self.sub_level = sub_level
    super(Moveable, self).__init__(x,y)
    self.subsurf = self.surf
    self.dx = self.ddx = self.dy = self.ddy = 0
    self.max_d = max_d
    self.max_dx = max_d
    self.max_dy = max_d
    self.move_pos(0)
    
  def run(self, d_time):
    super(Moveable, self).run(d_time)
    self.moved = self.move(d_time)
    self.dirty = self.dirty or self.moved
    
  def move(self, d_time):
    if self.ddx == self.ddy == self.dx == self.dy == 0: return False
    if cmp(self.ddx,0) != cmp(self.dx, 0): self.dx = 0 # Stop if moving the opposite direction
    if cmp(self.ddy,0) != cmp(self.dy, 0): self.dy = 0
    self.dx+=self.ddx*d_time
    self.dy+=self.ddy*d_time
    self.dx = self.normalise(self.dx, d_time)
    self.dy = self.normalise(self.dy, d_time,y=True)
    self.dx = self.clamp(self.max_dx, self.dx)
    self.dy = self.clamp(self.max_dy, self.dy)
    
    self.ddx = 0
    self.ddy = 0
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
  
  def normalise(self, val, amount, y=False):
    if getattr(self, ["ddx","ddy"][y]) != 0.0:
      return val
    orig_sign = cmp(val, 0)
    final = val-orig_sign*amount*self.speed_loss
    new_sign = cmp(final, 0)
    if new_sign != orig_sign:
      return 0
    return final
  
  def load_surf(self, surf):
    surf = super(Moveable, self).load_surf(surf)
    return SubPixelSurface(surf, self.sub_level)
  