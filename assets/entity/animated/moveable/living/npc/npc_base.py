#!/usr/bin/env python

from ..living_base import Living

class NPC(Living):
  def __init__(self, x,y):
    super(NPC, self).__init__(x,y)