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