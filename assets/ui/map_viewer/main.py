#!/usr/bin/env python

import random, time, math

from ..ui import UI
from assets.map.dungeon_map import DungeonMap
from event_handler import KeyboardHandler

class MapUI(UI):
  def __init__(self):
    super(MapUI, self).__init__()
    self.config_manager = self.get_main().config_manager
    self.get_main().fonts.register_font("debug")
    self.debug_font = self.get_main().fonts["debug"]
    self.map = DungeonMap(self.config_manager)
    self.draw_rects = False
    self.draw_debug = True
    self.dirty = True
    self.scrolling = []
    self.shaking = 0
    self.init_scrolling = False
    self.event_funcs = {
      "move_up":     [self.move, (0,-1)],
      "move_down":   [self.move, (0,1)],
      "move_left":   [self.move, (-1,0)],
      "move_right":  [self.move, (1,0)],
      "open_doors":  [self.open_doors, True],
      "toggle_rects":[self.toggle_draw_rects]
    }
    self.event_manager = self.get_main().event_manager
    self.event_manager.add_subscription_event(self, KeyboardHandler)
    self.event_manager.subscriber = self.subscription_id
    self.get_main().databin.entity_data.entities = []
    self.entity_manager = self.get_main().entity_manager
    self.entity_list = self.entity_manager.entities
    self.backdrop_ui = self.entity_list["animated.backdrop"]()
    self.player = self.entity_list["animated.moveable.living.player"](self)
    self.door = self.entity_list["animated.door"]
    self.load_dungeon()
    self.old_time = time.clock()
    
  def load_dungeon(self):
    self.map.load_dungeon()
    self.backdrop_ui.load_new_backdrop()
    self.load_room(self.map.nodes.entrance, 0, True)
    
  def load_room(self, current_room, room_id, no_scroll = False):
    if not no_scroll:
      self.init_scrolling = True
      self.bg_image = self.get_pygame().surface.Surface(self.screen.size)
      self.draw()
      self.init_scrolling = False
      self.scrolling = (((0,1),(1,0),(0,-1),(-1,0)))[room_id]
    axis = 1-room_id%2
    setattr(self.player, "xy"[axis], self.screen.get_size()[axis]*(1-(room_id>>1))+52*cmp(room_id>>1, 0.5))
    self.current_room = current_room
    random.seed(self.current_room.seed)
    self.backdrop_ui.load_current_room()
    self.clean_entities()
    self.load_entities()
    self.add_doors()
    self.old_time = time.clock()

  def add_doors(self):
    coords = self.map.get_coords(self.current_room)
    for pos_id, d_coord in enumerate(((0,1),(-1,0),(0,-1),(1,0))):
      room = self.map.get_room(map(int.__add__, coords, d_coord))
      if room and room in self.current_room.connections:
        d = self.door(pos_id, room, self.current_room)
        d.run_anim(0)

  def clean_entities(self):
    for entity in self.get_entities():
      if not entity.persistant:
          entity.__del__()
  
  def load_entities(self):
    for entity in self.current_room.get_entities():
      self.entity_list[entity]()
  
  def call_key_event(self, event_name):
    for event in event_name:
      assert(event in self.event_funcs)
      self.event_funcs[event][0](*self.event_funcs[event][1:])
    
  def move(self, delta_offset):
    self.player.ddx += delta_offset[0]
    self.player.ddy += delta_offset[1]
    
  def open_doors(self, all_ = False):
    for door in self.get_main().databin.entity_data.door:
      if (not door.locked) or all_:
        door.auto_update = False
        door.locked = False
        door.open = True
        door.current_anim = "Open"
        door.auto_update = True
        door.load_animation()
        
  def toggle_draw_rects(self):
    self.draw_rects = not self.draw_rects

  def calc_scroll(self, x_mod, y_mod):
    x_mod += self.scrolling[0]
    y_mod += self.scrolling[1]
    sign = map(lambda i: cmp(i, 0), self.scrolling)
    self.scrolling = [i+sign[j]*(200*self.d_time) for j, i in enumerate(self.scrolling)]
    self.screen.blit(self.bg_image, (x_mod,y_mod))
    x_mod -= cmp(x_mod, 0)*self.screen.get_size()[0]
    y_mod -= cmp(y_mod, 0)*self.screen.get_size()[1]
    if [cmp(x_mod, 0), cmp(y_mod, 0)] == sign:
      self.scrolling = []
    return x_mod, y_mod
      
  def draw(self):
    x_mod = 0
    y_mod = 0
    if self.shaking > 0:
      rs = math.ceil(self.shaking)
      x_mod += random.randrange(-rs,rs)
      y_mod += random.randrange(-rs,rs)
      self.shaking -= self.d_time
    if self.scrolling:
      x_mod, y_mod = self.calc_scroll(x_mod, y_mod)
    for entity in self.get_entities():
      if not (self.scrolling or self.init_scrolling) or entity is not self.player:
        self.get_blit(entity.dirty)(entity.surf, (entity.x+x_mod,entity.y+y_mod))
        if self.draw_rects: self.draw_rect(entity.rect)
    if self.draw_debug:
      self.draw_debug_text()
      
  def draw_debug_text(self):
    cur_room = self.debug_font.render("Current room: %s"%self.current_room, True, (255,255,255))
    self.screen.blit(cur_room, (10,50))
    cur_room = self.debug_font.render("Keys: %d"%self.player.keys, True, (255,255,255))
    self.screen.blit(cur_room, (10,70))
    
  def run(self):
    self.d_time = time.clock() - self.old_time
    self.old_time = time.clock()
    if self.scrolling: return
    for entity in self.get_entities():
      entity.run(self.d_time)
    #print d_time
  
  def get_blit(self, dirty):
    if self.init_scrolling: return self.blit_bg_im
    if dirty:
      return self.screen.blit
    return self.screen.blit_func
  
  def draw_rect(self, o_rect):
    rect = o_rect.copy()
    rect.x*=2
    rect.y*=2
    rect.height*=2
    rect.width*=2
    self.screen.fill((0,0,0), rect)
    self.screen.blit_rects.append(rect)
  
  def blit_bg_im(self, surf, pos):
    self.bg_image.blit(surf, (pos[0]*2, pos[1]*2))
  
  def get_entities(self):
    return self.get_main().databin.entity_data.entity
