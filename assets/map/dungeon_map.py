#!/usr/bin/env python

from generation.node_grammer import Nodes
import generation.nodes

class DungeonMap(object):
  def __init__(self, config_manager):
    self.config_manager = config_manager
    self.chains_json = self.config_manager["dungeon_chains"]
    self.nodes_json = self.config_manager["dungeon_nodes"]
  
  def load_dungeon(self):
    try:
      difficulty = self.end_node.difficulty
    except AttributeError:
      difficulty = 0
    self.nodes = Nodes(self.chains_json, self.nodes_json)
    self.nodes.create_dungeon(difficulty)
    if self.config_manager.get_main_class().debug:
      if 1:
        i=1
        print "Creating dungeon", i
        size = (0,0)
        while size != (7,7):
          print("Retrying")
          self.nodes.create_dungeon(difficulty)
          map = self.nodes.map.map
          size = len(map[0]), len(map)
          print size
        self.nodes.save_nodes("graph_%s"%i)
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
  
  def replace_node(self, old_node, new_node, carry_entities = []):
    coords = self.get_coords(old_node)
    if isinstance(new_node, basestring):
      node_class = generation.nodes.nodetypes[new_node]
      new_node = node_class(old_node.seed)
    else:
      new_node.seed = old_node.seed
    new_node.difficulty = old_node.difficulty
    self.map[coords[0]][coords[1]] = new_node
    for conn in old_node.connections[:]:
      conn.disconnect(old_node)
      conn.connect(new_node)
      
    for entity in carry_entities:
      if not entity.spawned:
        new_node.entity_list.append(entity)
        if "door" in entity.mro_groups:
          entity.current_room = new_node
    for conn in new_node.connections:
      for entity in conn.entity_list:
        if "door" in entity.mro_groups:
          if entity.room is old_node:
            entity.room = new_node
    return new_node