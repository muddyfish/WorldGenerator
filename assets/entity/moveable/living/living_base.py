#!/usr/bin/env python

from ..moveable_base import Moveable

class Living(Moveable):
  def __init__(self, x,y, max_life = 10):
    super(Living, self).__init__(x,y)
    self.max_life = max_life
    self.life = self.max_life
    self.damage_mult = {
      "sword": 1.0,
      "heal":  1.0,
      "magic": 1.0,
      "fire":  1.0,
      "ice":   1.0,
      "light": 1.0,
      "shadow":1.0,
      "spirit":1.0,
      "air":   1.0,
      "water": 1.0}