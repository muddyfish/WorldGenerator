#!/usr/bin/env python

from ..moveable_base import Moveable

class Bomb(Moveable):
  transparent_colour = None
  def __init__(self, x=0, y=0):
    self.pygame = self.get_pygame()
    self.screen = self.get_main().screen
    super(Bomb, self).__init__(x,y)
    self.load_animation_sheet("bomb.anm2")
    self.finish_anim_funcs = {
        "Pulse": self.explode
      }
    self.current_anim = "Pulse"
    self.run_anim(0)
    
  def run(self, d_time):
    self.run_anim(d_time)
    
  def explode(self):
    self.get_main().databin.current_subscription.shaking += 1
    self.load_animation("Explode")