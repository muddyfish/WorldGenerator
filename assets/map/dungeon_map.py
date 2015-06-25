#!/usr/bin/env python

import glob

from generation.node_grammer import Nodes
from generation.tilearray import TileArray

class DungeonMap(object):
  def __init__(self, config_manager):
    self.config_manager = config_manager
    self.chains_json = self.config_manager["dungeon_chains"]
    self.nodes_json = self.config_manager["dungeon_nodes"]
    
    self.load_sprites()
    
    self.nodes = Nodes(self.chains_json, self.nodes_json)
    self.nodes.create_dungeon()
    self.tile_array = TileArray(self.nodes.map.map)
  
  def load_sprites(self):
    self.tileset_path = self.config_manager.parse_path(self.config_manager["path_config", "dungeon_tileset_path"])
    self.tilesets = glob.glob(self.config_manager.get_path(self.tileset_path, "tileset_*.png"))
    self.tileset_id = 2
    self.tile_size = 24
    #print self.tilesets[self.tileset_id]
    pygame = self.config_manager.get_pygame()
    colours = [(0,0,0), (127,255,127), (255,0,255)]
    self.sprites = []
    for colour in colours:
      self.sprites.append(pygame.surface.Surface((self.tile_size, self.tile_size)))
      self.sprites[-1].fill(colour)
    