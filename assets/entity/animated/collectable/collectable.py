#!/usr/bin/env python

from ..animate import Animation

class Collectable(Animation):
  setter = ""
  function = lambda self,x: x+1
  
  def run(self, d_time):
    self.run_anim(d_time)
    self.center(self.x_pos, self.y_pos)
    if "Collect" != self.current_anim:
      for entity in self.get_collide():
        if "player" in entity.groups:
          setattr(entity, self.setter, self.function(getattr(entity, self.setter)))
          self.current_anim = "Collect"        
          self.no_respawn = True