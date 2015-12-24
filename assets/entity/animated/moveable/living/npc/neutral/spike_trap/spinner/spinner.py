#!/usr/bin/env python

from ..spike_trap_base import SpikeTrap
import math

class Spinner(SpikeTrap):
  invincible = True
  speed = 1.0
  update_bounding_box = False
  spawn_method = staticmethod(lambda: Spinner.spawn_circular)
  circle_radius = 50
  spike_time = 1
  max_spawned = 5
  use_random = False
  
  def __init__(self,x,y, spawn_id):
    self.spawn_id = spawn_id
    self.offset = 0
    self.screen = self.get_main().screen
    self.bounding_rect = self.get_pygame().Rect([16,16,64,64])
    self.rect = self.bounding_rect.copy()
    super(Spinner, self).__init__(x,y)
    self.load_animation_sheet("spinner.anm2")
    self.load_animation("No-Spikes")
    self.x_pos += self.surf.get_width()/2
    self.y_pos += self.surf.get_height()/2
    self.run_anim(0)
    self.center(self.x_pos, self.y_pos)
    self.first_run = True
    
  def run(self, d_time):
    if self.first_run:
      self.setup_first_run()
      self.first_run = False
    self.offset += d_time * self.speed * (Spinner.max_spawned - self.total_spinners)
    super(Spinner, self).run(d_time)
    self.run_anim(d_time)
    self.x_pos = self.screen.get_center()[0] + self.circle_radius * math.sin(2*math.pi*self.spawn_id/float(self.total_spinners)+self.offset)+self.bounding_rect.width/4
    self.y_pos = self.screen.get_center()[1] + self.circle_radius * math.cos(2*math.pi*self.spawn_id/float(self.total_spinners)+self.offset)+self.bounding_rect.height/4
    self.center(self.x_pos,self.y_pos)

  def setup_first_run(self):
    self.total_spinners = len(self.get_databin().entity_data.spinner)