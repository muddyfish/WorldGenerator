#!/usr/bin/env python

from ..moveable_base import Moveable

class Bomb(Moveable):
  transparent_colour = None
  def __init__(self, x, y):
    self.pygame = self.get_pygame()
    self.screen = self.get_main().screen
    super(Bomb, self).__init__(x,y)
    self.load_animation_sheet("bomb.anm2")
    self.finish_anim_funcs = {
        "Collect_Pulse": lambda: self.load_animation("Idle")
      }
    self.current_anim = "Idle"
    self.run_anim(0)
    self.clean_surf = self.surf
    self.update_surf()
    
  def run(self, d_time):
    self.run_anim(d_time)