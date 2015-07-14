#!/usr/bin/env python

import os, imp, pkgutil, glob
from ...manager_base import ManagerBase
import tile

class TileManager(ManagerBase):
  BLACKLIST = ["tile_manager",
               "tile",
               "__init__"]
  
  def __init__(self):
    self.tile_names = glob.glob(os.path.join(os.path.dirname(os.path.realpath(__file__)), "*.py"))
    self.tiles = {}
    for tile_path in self.tile_names:
      tile_name = os.path.basename(tile_path)[:-3]
      if tile_name not in TileManager.BLACKLIST:
        self.tiles[tile_name] = self.load_tile(tile_name, tile_path)
    print self.tiles
  
  def __getattr__(self, value):
    if value in self.__dict__:
      return self.__dict__[value]
    return self.tiles[value]()
      
  def load_tile(self, tile_name, tile_path):
    path_var = "assets.map.tiles.%s"%tile_name
    tile_module = imp.load_source(path_var, tile_path)
    for c in tile_module.__dict__.values():
      try:
        if issubclass(c, tile.Tile) and c is not tile.Tile:
          return c
      except TypeError: pass