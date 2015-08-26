#!/usr/bin/env python

from ..animate import Animation

class Collectable(Animation):
  setter = ""
  function = lambda self,x: x+1
  
  def run(self, d_time):
    self.run_anim(d_time)
    self.x = self.x_pos-self.surf.get_width()/4
    self.y = self.y_pos-self.surf.get_height()/4
    if "Collect" != self.current_anim:
      for entity in self.get_collide():
        if "player" in entity.groups:
          setattr(entity, self.setter, self.function(getattr(entity, self.setter)))
          self.current_anim = "Collect"