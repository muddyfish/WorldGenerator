#!/usr/bin/env python

import glob
import random

from generation.node_grammer import Nodes
from generation.tilearray import TileArray


class DungeonMap(object):
  def __init__(self, config_manager):
    self.config_manager = config_manager
    self.tile_manager = config_manager.get_main_class().tile_manager
    self.chains_json = self.config_manager["dungeon_chains"]
    self.nodes_json = self.config_manager["dungeon_nodes"]
    self.tileset_path = self.config_manager.parse_path(self.config_manager["path_config", "dungeon_tileset_path"])
    self.sprite_info = self.config_manager["dungeon_tile_config"]
    self.sprite_tilemap = self.sprite_info["tilemap"]
    self.setup_tilemap()
    
  def setup_tilemap(self):
    self.tile_values = {}
    for k,v in self.sprite_info["tile_values"].iteritems():
      mask = 0
      bit_field = 0
      for y in [0,1,2]:
        for x in [0,1,2]:
          cur_bit = y*3+x
          if v[y][x] != 2:
            mask |= 1<<cur_bit
            bit_field |= v[y][x]<<cur_bit
      self.tile_values[(mask, bit_field)] = int(k)
    self.tile_keys = self.tile_values.keys()
    
    self.tiles_lookup = {}
    
    self.load_sprites()
    
    self.nodes = Nodes(self.chains_json, self.nodes_json)
    self.nodes.create_dungeon()
    self.tile_array = TileArray(self.nodes.map.map, self.config_manager)
  
  def load_sprites(self):
    self.tilesets = glob.glob(self.config_manager.get_path(self.tileset_path, "tileset_*.png"))
    self.tile_size = 24
    self.tiles = self.load_spritesheet(random.choice(self.tilesets))
  
  def load_spritesheet(self, spritesheet_name):
    #print spritesheet_name
    tiles = {}
    pygame = self.config_manager.get_pygame()
    sheet = pygame.image.load(spritesheet_name)
    for y, row in enumerate(range(0, sheet.get_height(), self.tile_size+1)):
      for x, column in enumerate(range(0, sheet.get_width(), self.tile_size+1)):
        rect = pygame.Rect((column, row),(24,24))
        sprite = sheet.subsurface(rect)
        tile_id = self.sprite_tilemap[y][x]
        if tile_id not in tiles:
          tiles[tile_id] = []
        tiles[tile_id].append(sprite)
    return tiles
  
  def get_tile(self, x,y):
    tiles = 0
    bit = 0
    for dy in [-1,0,1]:
      for dx in [-1,0,1]:
        try:
          value = self.tile_array[y+dy,x+dx]
        except IndexError:
          value = 1
        tiles |= value<<bit
        bit+=1
    return self.get_best(tiles)
    
  def get_best(self, tiles):
    if tiles in self.tiles_lookup:
      return self.tiles_lookup[tiles]
    best_tile = [0,[]]
    for t in self.tile_keys:
      if self.tile_equal(t, tiles):
        score = self.get_tile_score(t)
        if score >= best_tile[0]:
          best_tile = [score, t]
        if score == 9: break
    rtn = self.tile_values[best_tile[1]]
    self.tiles_lookup[tiles] = rtn
    return rtn

  def tile_equal(self, t, tile):
    for bit in range(9):
      if (t[0]>>bit)&1 and (t[1]>>bit)&1!=(tile>>bit)&1:
        return False
    return True
            
  def get_tile_score(self, t):
    return bin(t[0]).count("1")