#!/usr/bin/env python

import random, time

from ..ui import UI
from assets.map.dungeon_map import DungeonMap
from event_handler import KeyboardHandler
from ...entity.backdrop import Backdrops
from ...entity.moveable.living.player.player import Player

class MapUI(UI):
  def __init__(self):
    super(MapUI, self).__init__()
    self.config_manager = self.get_main().config_manager
    self.map = DungeonMap(self.config_manager)
    self.dirty = True
    self.event_funcs = {
      "move_up":    [self.move, (0,-1)],
      "move_down":  [self.move, (0,1)],
      "move_left":  [self.move, (-1,0)],
      "move_right": [self.move, (1,0)]
    }
    self.event_manager = self.get_main().event_manager
    self.event_manager.add_subscription_event(self, KeyboardHandler)
    self.event_manager.subscriber = self.subscription_id
    self.get_main().databin.entity_data.entities = []
    self.backdrop_ui = Backdrops()
    print 
    self.player = Player(*self.screen.get_center())
    self.load_dungeon()
    self.old_time = time.clock()
    
  def call_key_event(self, event_name):
    for event in event_name:
      assert(event in self.event_funcs)
      self.event_funcs[event][0](*self.event_funcs[event][1:])
    
  def move(self, delta_offset):
    self.player.ddx += delta_offset[0]
    self.player.ddy += delta_offset[1]

  def draw(self):
    for entity in self.get_entities():
      self.get_blit(entity.dirty)(entity.surf, (entity.x,entity.y))
    
  def run(self):
    d_time = time.clock() - self.old_time
    for entity in self.get_entities():
      entity.run(d_time)
    #print d_time
    self.old_time = time.clock()
  
  def get_blit(self, dirty):
    if dirty:
      return self.screen.blit
    return self.screen.blit_func
  
  def get_entities(self):
    return self.get_main().databin.entity_data.entities
  
  def load_dungeon(self):
    self.map.load_dungeon()
    self.current_room = self.map.nodes.entrance
    self.backdrop_ui.load_new_backdrop()
    self.backdrop_ui.load_current_room()
    
    
    
    
    
    
