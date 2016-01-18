#!/usr/bin/env python

import random, math

from ..ui import UI
from assets.map.dungeon_map import DungeonMap
from event_handler import KeyboardHandler
from assets.events.clock import Clock
import time

class MapUI(UI):
  def __init__(self):
    super(MapUI, self).__init__()
    self.config_manager = self.get_main().config_manager
    self.get_main().fonts.register_font("debug")
    self.debug_font = self.get_main().fonts["debug"]
    self.map = DungeonMap(self.config_manager)
    self.draw_rects = False
    self.draw_debug = self.config_manager.config_data["subscription_config"]["draw_debug"]
    self.speedup = self.config_manager.config_data["video_config"]["speedup"]
    self.scrolling = []
    self.shaking = 0
    self.init_scrolling = False
    self.event_manager = self.get_main().event_manager
    self.event_manager.add_subscription_event(self, KeyboardHandler)
    self.event_manager.subscriber = self.subscription_id
    self.entity_manager = self.get_main().entity_manager
    self.entity_list = self.entity_manager.entities
    self.backdrop_ui = self.entity_list["animated.backdrop"]()
    self.backdrop_ui.spawn()
    self.player = self.entity_list["animated.moveable.living.player"](self)
    self.player.spawn()
    self.event_funcs = {
      "move_up":     [self.move, (0,-1)],
      "move_down":   [self.move, (0,1)],
      "move_left":   [self.move, (-1,0)],
      "move_right":  [self.move, (1,0)],
      "use_sword":   [self.player.use_sword],
      "place_bomb":  [self.player.place_bomb],
      "open_doors":  [self.open_doors, True],
      "shake":       [lambda:setattr(self, "shaking", 1)],
      "toggle_rects":[self.toggle_draw_rects],
      "show_databin":[self.print_databin]
    }
    for k,v in self.entity_manager.get_persistant_entities().iteritems():
      if k not in ["animated.backdrop", "animated.moveable.living.player", "animated.hud", "animated.hud.map"]:
        v().spawn()
    self.clock = Clock()
    self.load_dungeon()
    
  def load_dungeon(self):
    try:
      map_entity = self.get_main().databin.entity_data.map.sprites()[0]
    except TypeError:pass
    else:
      map_entity.despawn()
    self.map.load_dungeon()
    self.backdrop_ui.load_new_backdrop()
    self.entity_list["animated.hud.map"](self).spawn()
    self.load_room(self.map.start_node, 0, no_scroll = True)
    self.player.x, self.player.y = self.screen.get_center()
    
  def load_room(self, current_room, room_id, no_scroll = False):
    try:
      no_sword = len(self.get_main().databin.entity_data.sword.sprites()) == 0
    except TypeError:
      no_sword = True
    if not no_sword:
      self.get_main().databin.entity_data.sword.sprites()[0].despawn()
    if not no_scroll:
      self.init_scrolling = True
      self.bg_image = self.get_pygame().surface.Surface(self.screen.size)
      self.draw()
      self.init_scrolling = False
      self.scrolling = (((0,1),(1,0),(0,-1),(-1,0)))[room_id]
    axis = 1-room_id%2
    setattr(self.player, "xy"[axis], self.screen.get_size()[axis]*(1-(room_id>>1))+52*cmp(room_id>>1, 0.5))
    self.clean_entities()
    self.player.invincible = True
    self._load_room(current_room)
  
  def _load_room(self, current_room):
    self.current_room = current_room
    random.seed(self.current_room.seed)
    self.backdrop_ui.load_current_room()
    self.add_doors()
    self.load_entities()
    self.get_main().databin.entity_data.map.sprites()[0].update_room()
    self.current_room.visited = True
    self.clock.tick()

  def add_doors(self):
    if not self.current_room.visited:
      coords = self.map.get_coords(self.current_room)
      for pos_id, d_coord in enumerate(((0,1),(-1,0),(0,-1),(1,0))):
        room = self.map.get_room(map(int.__add__, coords, d_coord))
        if room and room in self.current_room.connections:
          door = self.entity_list["animated.door"](pos_id, room, self.current_room)
          self.current_room.entity_list.append(door)

  def clean_entities(self):
    for entity in self.get_entities():
      if not entity.persistant:
          entity.despawn(killed = False)
  
  def load_entities(self):
    for entity in self.current_room.entity_list:
      entity.spawn()
  
  def room_cleared(self):
    try:
      new_room_list = self.current_room.replace_on_room_clear
    except AttributeError:
      new_room_list = []
    if new_room_list:
      entities = self.get_entities().sprites()[:]
      new_room_name = random.choice(new_room_list)
      old_room = self.current_room
      self.clean_entities()
      new_room = self.map.replace_node(self.current_room, new_room_name, entities)
      new_room.visited = True
      self._load_room(new_room)
      return
    
    auto_cleared = True
    for entity in self.current_room.entity_list:
      if entity.must_kill:
        auto_cleared = False
    if auto_cleared:
      for door in self.get_main().databin.entity_data.door:
        if not door.locked:
          door.open = True
          door.current_anim = "Opened"
    else:
      self.open_doors()
  
  def call_key_event(self, event_name):
    for event in event_name:
      assert(event in self.event_funcs)
      self.event_funcs[event][0](*self.event_funcs[event][1:])
    
  def move(self, delta_offset):
    if delta_offset[0]:
      self.player.cddx = delta_offset[0]*self.player.dd
    if delta_offset[1]:
      self.player.cddy = delta_offset[1]*self.player.dd
    
  def open_doors(self, all_ = False):
    for door in self.get_main().databin.entity_data.door:
      if (not door.locked) or all_:
        door.locked = False
        door.open = True
        
  def toggle_draw_rects(self):
    self.draw_rects = not self.draw_rects

  def calc_scroll(self, in_x_mod, in_y_mod):
    x_mod = self.scrolling[0]
    y_mod = self.scrolling[1]
    sign = map(lambda i: cmp(i, 0), self.scrolling)
    self.scrolling = [i+sign[j]*(200*self.d_time) for j, i in enumerate(self.scrolling)]
    self.screen.blit(self.bg_image, (in_x_mod+x_mod,in_y_mod+y_mod))
    x_mod -= cmp(x_mod, 0)*self.screen.get_size()[0]
    y_mod -= cmp(y_mod, 0)*self.screen.get_size()[1]
    if [cmp(x_mod, 0), cmp(y_mod, 0)] == sign:
      self.scrolling = []
    return in_x_mod+x_mod, in_y_mod+y_mod
      
  def draw(self):
    x_mod = 0
    y_mod = 0
    if self.shaking > 0:
      rs = math.ceil(self.shaking)
      x_mod += random.randrange(-rs,rs)
      y_mod += random.randrange(-rs,rs)
      self.shaking -= self.d_time
      if self.shaking < 0: self.shaking = 0
    if self.scrolling:
      x_mod, y_mod = self.calc_scroll(x_mod, y_mod)
    for entity in self.get_entities():
      if (entity not in self.get_main().databin.entity_data.hud) and (\
           (not (self.scrolling or self.init_scrolling)) or \
           (self.scrolling and entity is not self.player) or \
           (self.init_scrolling and entity is not self.player)
          ):
        if self.draw_rects and entity is not self.backdrop_ui: self.draw_rect(entity.rect)
        else:entity.blit(x_mod,y_mod)
    if not self.init_scrolling:
      for entity in self.get_main().databin.entity_data.hud:
        entity.blit()
    if self.draw_debug:
      self.draw_debug_text()
      
  def draw_debug_text(self):
    cur_room = self.debug_font.render("Current room: %s"%self.current_room, True, (255,255,255))
    self.screen.blit(cur_room, (10,50))
    #cur_room = self.debug_font.render("Keys: %d"%self.player.keys, True, (255,255,255))
    #self.screen.blit(cur_room, (10,70))
    
  def print_databin(self, databin = None, no_tabs = 0):
    if databin is None: databin = self.get_main().databin
    for k,v in databin.__dict__.iteritems():
      if isinstance(v, databin.__class__):
        print "%s%s: {"%(" "*no_tabs,k)
        self.print_databin(v, no_tabs+2)
        print "%s}"%(" "*no_tabs)
      elif isinstance(v, self.get_pygame().sprite.LayeredUpdates):
        print "%s%s: %s"%(" "*no_tabs, k,v.sprites())
      else:
        print "%s%s: %s"%(" "*no_tabs, k,v)
    
  def run(self):
    self.d_time = self.clock.tick()
    self.d_time *= self.speedup
    if self.scrolling: return
    room_cleared = True
    for entity in self.get_entities():
      if entity.must_kill:
        room_cleared = False
      if entity.spawned:
        try:
          entity.run(self.d_time)
        except:
          print "Exception raised in %r whilst running"%entity
          raise
    if room_cleared and not self.current_room.cleared and not self.scrolling:
      self.current_room.cleared = True
      self.room_cleared()
    
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
