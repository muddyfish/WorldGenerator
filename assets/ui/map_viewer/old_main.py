#!/usr/bin/env python

import sys, os, random

from ..ui import UI
from assets.map.dungeon_map import DungeonMap
sys.path.insert(0, os.path.realpath(os.path.abspath(os.path.split(__file__)[0])))
from event_handler import KeyboardHandler

class MapUI(UI):
  def __init__(self):
    super(MapUI, self).__init__()
    self.get_pygame().key.set_repeat(1,1)
    self.map = DungeonMap(self.get_main().config_manager)
    self.find_map_sprites()
    self.offset = [0,0]
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
    
  def find_map_sprites(self):
    self.tile_size = self.map.tile_size
    self.map_size = [coord/self.tile_size+1 for coord in self.screen.get_size()]
    self.tiles = [[None for i in j] for j in self.map.tile_array]
    
#    print self.tiles

  def get_tile(self, x,y):
    return random.choice(self.map.tiles[self.map.get_tile(x,y)])

  def call_key_event(self, event_name):
    for event in event_name:
      assert(event in self.event_funcs)
      self.event_funcs[event][0](*self.event_funcs[event][1:])
    
  def move(self, delta_offset):
    for i, v in enumerate(delta_offset):
      self.offset[i]+=v
    self.dirty = True

  def draw(self):
    if self.dirty:
      self.screen.fill((0,0,0))
      self.dirty = False
      for y, row in enumerate(self.tiles[self.offset[1]:self.offset[1]+self.map_size[1]]):
        for x, sprite in enumerate(row[self.offset[0]:self.offset[0]+self.map_size[0]]):
          if sprite is None:
            sprite = self.tiles[y+self.offset[1]][x+self.offset[0]] = self.get_tile(x+self.offset[0],y+self.offset[1])
          self.screen.blit(sprite, (x*self.tile_size,y*self.tile_size))
      self.screen.blit_all()
