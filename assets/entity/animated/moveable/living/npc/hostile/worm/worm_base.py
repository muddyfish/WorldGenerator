#!/usr/bin/env python

from ..hostile_base import NPCHostile
import random

class Worm(NPCHostile):  
  def __init__(self,x,y):
    super(Worm, self).__init__(x,y)
  
  def run(self, d_time):
    self.register_event("collide_player", self.hurt_player)
    super(Worm, self).run(d_time)
    
    
  def hurt_player(self):
    if self.spiked:
      self.get_player().take_damage(self.damage_dealt)