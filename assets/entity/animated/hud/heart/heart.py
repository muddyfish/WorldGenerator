#!/usr/bin/env python

from ..hud import HUD
import os

class Heart(HUD):
  transparent_colour = None
  seperate_amount = 4

  def __init__(self):
    self.screen = self.get_main().screen
    self.life = self.get_player().life
    self.max_life = self.get_player().max_life
    self.pygame = self.get_pygame()
    super(Heart, self).__init__(24,32)
    self.get_surfs()
    self.update_surf()
    
  def run(self, d_time):
    life = self.get_player().life
    max_life = self.get_player().max_life
    if life != self.life or max_life != self.max_life:
      self.life = life
      self.max_life = max_life
      self.update_surf()
      
  def get_surfs(self):
    self.spritesheet = self.get_pygame().image.load(os.path.join(self.get_path(), "gfx", "heart.png"))
    self.surfs = []
    size = self.spritesheet.get_size()
    for surf_id in range(5):
      rect = (size[0]/5*surf_id, 0, 20, size[1])
      self.surfs.append(self.spritesheet.subsurface(rect))
      
  def update_surf(self):
    no_hearts, pieces = divmod(self.life, 4)
    max_life = self.max_life/4
    length = max_life*(Heart.seperate_amount+20)
    self.surf = self.pygame.Surface((length, 18), self.pygame.SRCALPHA)
    for heart_id in range(max_life):
      pos = (heart_id*(Heart.seperate_amount+20),0)
      if heart_id < no_hearts:
        self.surf.blit(self.surfs[0], pos)
      elif heart_id == no_hearts:
        self.surf.blit(self.surfs[4-pieces], pos)
      else:
        self.surf.blit(self.surfs[4], pos)