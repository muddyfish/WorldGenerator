#!/usr/bin/env python

from ..entity_base import Entity

class Animation(Entity):
  def load_animation(self, anim_name):
    config_manager = self.get_main().config_manager
    print anim_name