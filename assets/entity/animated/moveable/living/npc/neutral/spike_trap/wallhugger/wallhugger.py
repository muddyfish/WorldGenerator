#!/usr/bin/env python

from ..spike_trap_base import SpikeTrap

import random

class WallHugger(SpikeTrap):
  invincible = True
  speed = 128
  max_d = 128
  difficulty = 1
  auto_clamp = False
  update_bounding_box = False
  spawn_method = staticmethod(lambda: WallHugger.spawn_wall)
  surf_perm = 128
  
  def __init__(self,x,y, wall_id = 0):
    self.bounding_rect = self.get_pygame().Rect([16,16,64,64])
    self.rect = self.bounding_rect.copy()
    super(WallHugger, self).__init__(x,y)
    self.load_animation_sheet("wall hugger.anm2")
    self.load_animation("No-Spikes")
    self.register_event("collide_wall", self.choose_direction)
    self.x_pos += self.surf.get_width()*1.5
    self.y_pos += self.surf.get_height()*1.5
    self.start_direction(wall_id)
    self.center(self.x_pos, self.y_pos)
    self.cur_time = random.randrange(4)
    self.run(0)
    
  def run(self, d_time):
    super(WallHugger, self).run(d_time)
    self.run_anim(d_time)
    self.center(self.x_pos,self.y_pos)
    
  def choose_direction(self, wall_id):
    if   wall_id==0: self.direction = "RIGHT"
    elif wall_id==1: self.direction = "LEFT"
    elif wall_id==2: self.direction = "UP"
    elif wall_id==3: self.direction = "DOWN"
    self.set_direction()
    
  def start_direction(self, wall_id):
    if   wall_id==0: self.direction = "RIGHT"
    elif wall_id==1: self.direction = "DOWN"
    elif wall_id==2: self.direction = "LEFT"
    elif wall_id==3: self.direction = "UP"
    self.set_direction()