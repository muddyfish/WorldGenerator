#!/usr/bin/env python

from ..living_base import Living

class Player(Living):
  def __init__(self, x,y):
    super(Player, self).__init__(x,y, 20)
    