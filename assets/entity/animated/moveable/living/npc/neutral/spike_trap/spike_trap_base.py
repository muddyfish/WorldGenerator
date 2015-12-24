#!/usr/bin/env python

from ..neutral_base import NPCNeutral

class SpikeTrap(NPCNeutral):
  dd = 128
  max_d = 128
  spike_time = 2
  no_acc = True
  directions = {"UP":   ( 0,-1),
                "DOWN": ( 0, 1),
                "LEFT": (-1, 0),
                "RIGHT":( 1, 0)}
  
  def __init__(self, x,y):
    super(SpikeTrap, self).__init__(x,y)
    self.spiked = False
    self.cur_time = 0
    
  def run(self, d_time):
    super(SpikeTrap, self).run(d_time)
    self.cur_time += d_time
    if self.cur_time >= self.spike_time:
      self.cur_time -= self.spike_time
      self.spiked = not self.spiked
      if self.spiked:    
        self.load_animation("Spikes")
      else:
        self.load_animation("No-Spikes")
  
  def set_direction(self):
    movement = SpikeTrap.directions[self.direction]
    self.dx = movement[0]*self.speed
    self.dy = movement[1]*self.speed