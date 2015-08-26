#!/usr/bin/env python

from ..collectable import Collectable

class Key(Collectable):
  transparent_colour = None
  def __init__(self):
    self.screen = self.get_main().screen
    super(Key, self).__init__(0,0)
    self.finish_anim_funcs = {
      "Appear": lambda: self.load_animation("Idle"),
      "Collect": lambda: self.__del__()
    }
    self.load_animation_sheet("key.anm2")
    self.current_anim = "Appear"
    self.run_anim(0)
    self.pygame = self.get_pygame()
    self.x_pos = self.screen.get_width()/4
    self.y_pos = self.screen.get_height()/4
    self.setter = "keys"