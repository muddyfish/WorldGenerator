#!/usr/bin/env python

from ..charger_base import Charger

SNAKE_NORMAL_SPEED = 48

class Snake(Charger):
  anim_speed = 1.0/30
  max_health = 12
  min_health = 4
  speed_normal = SNAKE_NORMAL_SPEED
  speed_attack = SNAKE_NORMAL_SPEED*3
  circle_radius = 80
  spawn_method = staticmethod(lambda: Snake.spawn_circular)
  
  def __init__(self,x,y, spawn_id):
    super(Snake, self).__init__(x,y)
    self.load_animation_sheet("snake.anm2")
    self.finish_anim_funcs = {
        "Appear":      lambda: self.choose_direction(0)
      }
    self.run_anim(0)
    self.center(self.x_pos,self.y_pos)
    
  def run(self, d_time):
    super(Snake, self).run(d_time)
    self.run_anim(d_time)
    self.center(self.x_pos,self.y_pos)
    