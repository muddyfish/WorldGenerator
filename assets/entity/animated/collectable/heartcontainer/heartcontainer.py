#!/usr/bin/env python

from ..collectable import Collectable

class HeartContainer(Collectable):
  def __init__(self):
    self.screen = self.get_main().screen
    super(HeartContainer, self).__init__(0,0)
    self.finish_anim_funcs = {
      "Appear": lambda: self.load_animation("Idle"),
      "Collect": self.despawn
    }
    self.load_animation_sheet("heartcontainer.anm2")
    self.current_anim = "Appear"
    self.x_pos = self.screen.get_width()/4
    self.y_pos = self.screen.get_height()/4
    self.run_anim(0)
    self.center()
    
  def collected(self, entity):
    entity.life += 4
    entity.max_life += 4