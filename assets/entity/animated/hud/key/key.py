#!/usr/bin/env python

from ..hud import HUD

class Key(HUD):
  transparent_colour = None
  def __init__(self, overwrite_kid = None):
    self.screen = self.get_main().screen
    self.key_id = self.old_keys = self.get_player().keys
    self.is_boss_key = False
    if overwrite_kid:
      self.key_id = self.old_keys = overwrite_kid
    self.pygame = self.get_pygame()
    if self.key_id == 0:
      super(Key, self).__init__(0,0)
      self.surf = self.pygame.Surface((0,0))
    else:
      self.finish_anim_funcs = {
        "Appear": lambda: self.load_animation("Idle")
      }
      super(Key, self).__init__(7+24*self.key_id,self.screen.get_height()/2-48)
      if self.is_boss_key:
        self.load_animation_sheet("bosskey.anm2")
      else:
        self.load_animation_sheet("key.anm2")
      self.current_anim = "Appear"
      self.run_anim(0)
    
  def run(self, d_time):
    keys = self.get_player().keys
    has_boss_key = self.get_player().boss_key
    if keys > self.old_keys and self.key_id == 0:
      key = Key()
      key.spawn()
      if self.is_boss_key:
        key.x += 24
    elif keys < self.key_id: self.despawn()
    if self.key_id == 0 and has_boss_key and not self.is_boss_key:
      self.spawn_boss_key()
    if self.key_id == 0 and not has_boss_key and self.is_boss_key:
      self.is_boss_key = False
      self.x = self.y = 0
      self.surf = self.pygame.Surface((0,0))
      for key in self.get_entity_data().key:
        if key.key_id > 0:
          key.x -= 24
    if self.key_id != 0 or self.is_boss_key:
      self.run_anim(d_time)
    self.old_keys = keys
    
  def spawn_boss_key(self):
    self.is_boss_key = True
    self.x = 31
    self.y = self.screen.get_height()/2-48
    self.load_animation_sheet("bosskey.anm2")
    self.current_anim = "Appear"
    for key in self.get_entity_data().key:
      if key.key_id > 0:
        key.x += 24
      if key.key_id == self.get_player().keys:
        key.current_anim = "Appear"