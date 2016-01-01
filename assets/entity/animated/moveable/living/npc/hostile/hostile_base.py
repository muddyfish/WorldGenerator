#!/usr/bin/env python

from ..npc_base import NPC

class NPCHostile(NPC):
  must_kill = True
  no_respawn = True
  damage_dealt = 2
  
  def __init__(self,x,y):
    super(NPCHostile, self).__init__(x,y)
    self.register_event("collide_player", lambda: self.get_player().take_damage(self.damage_dealt))