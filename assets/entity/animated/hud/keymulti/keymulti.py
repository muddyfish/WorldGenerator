#!/usr/bin/env python

from ..hud import HUD

class KeyMulti(HUD):
  transparent_colour = None
  def __init__(self):
    super(KeyMulti, self).__init__(0,0)
    self.surf = self.get_pygame().Surface((0,0))