#!/usr/bin/env python

from ..collectable import Collectable

class Heart(Collectable):
  def __init__(self):
    self.screen = self.get_main().screen
    super(Heart, self).__init__(0,0)
    self.finish_anim_funcs = {
      "Appear": lambda: self.load_animation("Idle"),
      "Collect": self.despawn
    }
    self.load_animation_sheet("heart.anm2")
    self.current_anim = "Appear"
    self.run_anim(0)
    self.pygame = self.get_pygame()
    self.x_pos = self.screen.get_width()/4
    self.y_pos = self.screen.get_height()/4
    
    
  def collected(self, entity):
    entity.life += 4
    entity.life = min(entity.life, entity.max_life)