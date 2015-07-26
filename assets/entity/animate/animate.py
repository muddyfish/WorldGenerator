#!/usr/bin/env python

from ..entity_base import Entity

class Animation(Entity):
  def load_animation(self, anim_name):
    print anim_name