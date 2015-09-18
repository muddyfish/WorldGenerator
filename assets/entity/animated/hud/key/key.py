#!/usr/bin/env python

from ..hud import HUD

class Key(HUD):
  transparent_colour = None
  def __init__(self):
    self.key_id = self.old_keys = self.get_player().keys
    self.pygame = self.get_pygame()
    if self.key_id == 0:
      super(Key, self).__init__(0,0)
      self.surf = self.pygame.Surface((0,0))
    else:
      self.screen = self.get_main().screen
      self.finish_anim_funcs = {
        "Appear": lambda: self.load_animation("Idle")
      }
      super(Key, self).__init__(7+24*self.key_id,self.screen.get_height()/2-48)
      self.load_animation_sheet("key.anm2")
      self.current_anim = "Appear"
      self.run_anim(0)
    
  def run(self, d_time):
    keys = self.get_player().keys
    if keys > self.old_keys and self.key_id == 0:
      Key().spawn()
    elif keys < self.key_id: self.despawn()
    if self.key_id != 0:
      self.run_anim(d_time)
    self.old_keys = keys