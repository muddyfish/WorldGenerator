from Assets.Utility.asset_loader import asset_loader
import pygame
class Spritesheet():
  def __init__(self, spritesheet, w=32, h=32):
    self.spritesheet = spritesheet
    if isinstance(self.spritesheet, basestring):
      self.spritesheet = asset_loader.load_image(self.spritesheet, True, "")
    self.size = self.spritesheet.get_size()
    self.no_tiles = [self.size[0]/w,self.size[1]/h]
    self.tiles = []
    for ch in range(0, self.size[1], h):
      self.tiles.append([])
      for cw in range(0, self.size[0], w):
        self.tiles[-1].append(pygame.Surface((w,h)))
        self.tiles[-1][-1].blit(self.spritesheet, (-cw,-ch))

  def get_1d_tiles(self):
    tiles = []
    for row in self.tiles:
      tiles.extend(row)
    return tiles

  def split(self, x,y, w=32,h=32):
    return Spritesheet(self.tiles[x][y], w,h)
