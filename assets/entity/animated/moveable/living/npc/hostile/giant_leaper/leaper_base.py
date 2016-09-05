#!/usr/bin/env python

from ..hostile_base import NPCHostile
import random

class GiantLeaper(NPCHostile):  
  def __init__(self,x,y):
    super(GiantLeaper, self).__init__(x,y)
  
  def run(self, d_time):
    super(GiantLeaper, self).run(d_time)
    