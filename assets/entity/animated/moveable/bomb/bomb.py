#!/usr/bin/env python

from ..moveable_base import Moveable

class Bomb(Moveable):
  transparent_colour = None
  explosion_radius = 60
  
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
    for entity in self.get_entity_data().living:
      if not entity.invincible and entity is not self.get_player():
        if (entity.x-self.x)**2 + (entity.y-self.y)**2 <= Bomb.explosion_radius**2:
          entity.despawn()