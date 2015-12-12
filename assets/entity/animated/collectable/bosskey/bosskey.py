#!/usr/bin/env python

from ..collectable import Collectable

class BossKey(Collectable):
  transparent_colour = None
  def __init__(self):
    self.screen = self.get_main().screen
    super(BossKey, self).__init__(0,0)
    self.finish_anim_funcs = {
      "Appear": lambda: self.load_animation("Idle"),
      "Collect": self.despawn
    }
    self.load_animation_sheet("bosskey.anm2")
    self.current_anim = "Appear"
    self.run_anim(0)
    self.pygame = self.get_pygame()
    self.x_pos = self.screen.get_width()/4
    self.y_pos = self.screen.get_height()/4
    self.setter = "boss_key"