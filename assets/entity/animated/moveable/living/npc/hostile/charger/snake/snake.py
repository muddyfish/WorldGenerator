#!/usr/bin/env python

from ..charger_base import Charger

class Snake(Charger):
  anim_speed = 1.0/30
  max_health = 16
  min_health = 8
  circle_radius = 80
  spawn_method = staticmethod(lambda: Snake.circular)
  
  def __init__(self,x,y):
    self.no_fails = 10
    super(Snake, self).__init__(x,y)
    self.load_animation_sheet("snake.anm2")
    self.finish_anim_funcs = {
        "Appear":      lambda: self.choose_direction()
      }
    self.current_anim = "Appear"
    self.ai_events = {
      "collide_wall": self.choose_direction}
    self.x_pos, self.y_pos = self.x, self.y
    self.run_anim(0)
    self.center(self.x_pos,self.y_pos)
    
  def run(self, d_time):
    super(Snake, self).run(d_time)
    self.run_anim(d_time)
    self.center(self.x_pos,self.y_pos)
    
  def choose_direction(self):
    self.load_animation("Move Down")
    self.cddx = 0
    self.cddy = 20