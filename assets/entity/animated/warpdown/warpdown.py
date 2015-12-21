#!/usr/bin/env python

from ..animate import Animation

class WarpDown(Animation):
  transparent_colour = None
  def __init__(self):
    self.pygame = self.get_pygame()
    self.screen = self.get_main().screen
    super(WarpDown, self).__init__(0,0)
    self.load_animation_sheet("warpdown.anm2")
    self.finish_anim_funcs = {
        "Open Animation": lambda: self.load_animation("Opened")
      }
    self.current_anim = "Open Animation"
    self.run_anim(0)
    
  def run(self, d_time):
    self.run_anim(d_time)
    self.center()
    if self.current_anim == "Opened" and self.touching_player():
      self.get_databin().current_subscription.load_dungeon()