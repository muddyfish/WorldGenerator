#!/usr/bin/env python

from ..moveable_base import Moveable

class Bomb(Moveable):
  transparent_colour = None
  
  def __init__(self, x, y):
    super(Bomb, self).__init__(x,y)
    self.screen = self.get_main().screen
    self.load_animation_sheet("bomb.anm2")
    self.finish_anim_funcs = {
        "Pulse": self.explode,
        "Explode": self.despawn
      }
    self.current_anim = "Pulse"
    self.run_anim(0)
    self.x_pos, self.y_pos = x, y
    self.center(self.x_pos, self.y_pos)
    
  def run(self, d_time):
    self.run_anim(d_time)
    self.center(self.x_pos, self.y_pos)
    
  def explode(self):
    self.get_main().databin.current_subscription.shaking += 1
    self.load_animation("Explode")
    self.spawn_entity("animated.moveable.explosion", self.x_pos, self.y_pos)