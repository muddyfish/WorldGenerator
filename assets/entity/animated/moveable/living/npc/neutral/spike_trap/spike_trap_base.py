#!/usr/bin/env python

from ..neutral_base import NPCNeutral

class SpikeTrap(NPCNeutral):
  dd = 128
  max_d = 128
  no_acc = True
  directions = {"UP":   ( 0,-1),
                "DOWN": ( 0, 1),
                "LEFT": (-1, 0),
                "RIGHT":( 1, 0)}
    
  def set_direction(self):
    movement = SpikeTrap.directions[self.direction]
    self.dx = movement[0]*self.speed
    self.dy = movement[1]*self.speed