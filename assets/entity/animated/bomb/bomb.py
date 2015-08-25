#!/usr/bin/env python

from ..animate import Animation

class Bomb(Animation):
  transparent_colour = None
  def __init__(self):
    self.screen = self.get_main().screen
    super(Key, self).__init__(0,0)
    self.finish_anim_funcs = {
      "Appear": lambda: self.load_animation("Idle"),
      "Collect": lambda: self.__del__()
    }
    self.load_animation_sheet("bomb.anm2")
    self.current_anim = "Appear"
    self.run_anim(0)
    
  def run(self, d_time):
    self.run_anim(d_time)
    self.x = self.screen.get_width()/4-self.surf.get_width()/4
    self.y = self.screen.get_height()/4-self.surf.get_height()/4
    if "Collect" != self.current_anim:
      for entity in self.get_collide():
        if "player" in entity.groups:
          entity.bomb += 1
          self.current_anim = "Collect"