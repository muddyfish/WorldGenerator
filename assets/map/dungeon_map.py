#!/usr/bin/env python

from generation.node_grammer import Nodes

class DungeonMap(object):
  def __init__(self, config_manager):
    self.config_manager = config_manager
    self.tile_manager = config_manager.get_main_class().tile_manager
    self.chains_json = self.config_manager["dungeon_chains"]
    self.nodes_json = self.config_manager["dungeon_nodes"]
  
  def load_dungeon(self):
    self.nodes = Nodes(self.chains_json, self.nodes_json)
    self.nodes.create_dungeon()
    self.map = self.nodes.map.map
    self.start_node = self.nodes.entrance
    self.end_node = self.nodes.exit
    
  def get_coords(self, node):
    return self.nodes.map.find_obj(node)
  
  def get_room(self, coords):
    if -1 in coords: return None
    d_size = self.nodes.map.map_size
    if coords[0] == d_size[0]+1 or \
       coords[1] == d_size[1]+1:
      return None
    return self.map[coords[0]][coords[1]]