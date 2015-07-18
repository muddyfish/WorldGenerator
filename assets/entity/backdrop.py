#!/usr/bin/env python

from entity_base import Entity
import glob, os, random

class Backdrops(Entity):
  def __init__(self):
    super(Backdrops, self).__init__(0,0)
    self.pygame = self.get_pygame()
    self.config_manager = self.get_main().config_manager
    self.backdrop_path = self.config_manager.parse_path(self.config_manager["path_config", "dungeon_backdrop_path"])
    self.load_backdrops()
    
  def load_current_room(self):
    self.surf = self.pygame.surface.Surface((936,624))
    backdrop = random.choice(self.backdrops)
    for i in range(4):
      self.surf.blit(self.pygame.transform.flip(backdrop, i>>1, i%2),
                    (468*(i>>1), 312*(i%2)))
    
  def load_backdrops(self):
    self.backdrop_sheets = {}
    backdrop_ids = glob.glob(self.config_manager.parse_path(self.backdrop_path+".*_*png"))
    for backdrop in backdrop_ids:
      key = int(os.path.basename(backdrop)[:2], 16)
      self.backdrop_sheets[key] = self.pygame.image.load(backdrop)
  
  def load_new_backdrop(self):
    self.backdrop_spritesheet = random.choice(self.backdrop_sheets.values())
    self.backdrop_spritesheet = self.backdrop_sheets[1]
    self.backdrops = []
    for x in range(2):
      for y in range(3):
        self.backdrops.append(self.backdrop_spritesheet.subsurface(
          (x*468,y*312), (468,312)))