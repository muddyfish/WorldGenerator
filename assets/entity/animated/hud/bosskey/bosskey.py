#!/usr/bin/env python

from ..hud import HUD

class BossKey(HUD):
  transparent_colour = None
  def __init__(self):
    self.key_id = self.get_player().boss_key
    self.spawned = False
    self.pygame = self.get_pygame()
    if self.key_id == 0:
      super(BossKey, self).__init__(0,0)
      self.surf = self.pygame.Surface((0,0))
    else:
      self.screen = self.get_main().screen
      super(BossKey, self).__init__(self.screen.get_width()/2-70,self.screen.get_height()/2-47)
      self.load_animation_sheet("bosskey.anm2")
      self.current_anim = "Idle"
      self.run_anim(0)
    
  def run(self, d_time):
    has_key = self.get_player().boss_key
    if has_key and self.key_id == 0 and not self.spawned:
      BossKey().spawn()
      self.spawned = True
    elif self.key_id == 1 and not has_key: self.despawn()
    if self.key_id == 0 and self.spawned and not has_key:
      self.spawned = False
    if self.key_id != 0:
      self.run_anim(d_time)