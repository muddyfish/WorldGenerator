#!/usr/bin/env python

import  random

from ..ui import UI
from ..basic_sprite import BasicSprite
from assets.map.dungeon_map import DungeonMap
import assets.map.generation.constants
from event_handler import KeyboardHandler

class MapUI(UI):
  def __init__(self):
    super(MapUI, self).__init__()
    assets.map.generation.constants.setup(self.get_main().config_manager)
    pygame = self.get_pygame()
    pygame.key.set_repeat(1,1)
    self.map = DungeonMap(self.get_main().config_manager)
    self.tiles = []
    self.sprite_group = pygame.sprite.LayeredDirty()
    self.sprite_group.set_clip(((0,0), self.screen.get_size()))
    self.find_map_sprites()
    self.add_sprites()
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
    for y in range(len(self.map.tile_array.map)):
      self.tiles.append([])
      for x in range(len(self.map.tile_array[y])):
        surf = self.get_tile(x,y)
        self.tiles[-1].append(surf)
 
  def get_tile(self, x,y):
    return random.choice(self.map.tiles[self.map.get_tile(x,y)])

  def add_sprites(self):
    for y in range(self.map_size[1]):
      for x in range(self.map_size[0]):
        self.sprite_group.add(BasicSprite(self.tiles[y][x], x*self.tile_size, y*self.tile_size))

  def call_key_event(self, event_name):
    for event in event_name:
      assert(event in self.event_funcs)
      self.event_funcs[event][0](*self.event_funcs[event][1:])
    
  def move(self, delta_offset):
    for i, v in enumerate(delta_offset):
      self.offset[i]+=v
    for sprite in self.sprite_group.sprites():
      x,y = sprite.x/self.tile_size,sprite.y/self.tile_size
      sprite.image = self.tiles[y+self.offset[1]][x+self.offset[0]]
    self.dirty = True

  def draw(self):
    if self.dirty:
      self.sprite_group.draw(self.screen)
      self.dirty = False
      
  def redraw(self, rect):
    self.sprite_group.repaint_rect(rect)
