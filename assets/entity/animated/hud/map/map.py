#!/usr/bin/env python

from ..hud import HUD

class Map(HUD):
  transparency = 128
  path_colour = (128,128,128)
  cur_room_colour = (0,0,255)
  visited_room_colour = (64,64,64)
  unvisited_room_colour = (128,128,128)
  reward_room_colour = (255,128,0)
  
  def __init__(self, main):
    self.pygame = self.get_pygame()
    super(Map, self).__init__(0,0)
    self.main_sub = main
    self.map = main.map
    self.map_size = self.map.nodes.map.map_size
    self.has_compass = False
    #print self.map.nodes.map
    self.setup_surf()
    #self.show_whole_dungeon()
    #self.draw_compass()
    
  def __repr__(self):
    return "\n"+str(self.map.nodes.map)+"\n"
    
  def setup_surf(self):
    self.internal_surf = self.pygame.Surface(((self.map_size[0]+3)*16, (self.map_size[1]+3)*8))
    self.internal_surf.set_alpha(Map.transparency)
    self.internal_surf.set_colorkey((255,255,255))
    self.internal_surf.fill((255,255,255))
    self.x = self.get_main().screen.get_width()/2-self.internal_surf.get_width()
    self.y = 0
    
  def run(self, d_time):pass
  
  def scale_surf(self):
    self.surf = self.pygame.transform.scale2x(self.internal_surf)
  
  def show_whole_dungeon(self):
    old_surf = self.internal_surf.copy()
    self.setup_surf()
    for y in range(self.map_size[0]+1):
      for x in range(self.map_size[1]+1):
        room = self.map.map[y][x]
        if room:
          colour = Map.unvisited_room_colour
          if room and self.has_compass and hasattr(room, "replace_on_room_clear"):
            colour = Map.reward_room_colour
          self.blit_conns(room, colour)
    self.internal_surf.blit(old_surf, (0,0), None, self.pygame.BLEND_RGB_MIN)
    cur_room = self.main_sub.current_room
    self.blit_coords(self.map.get_coords(cur_room), Map.cur_room_colour)
    self.scale_surf()
    
  def draw_compass(self):
    self.has_compass = True
    for y in range(self.map_size[0]+1):
      for x in range(self.map_size[1]+1):
        room = self.map.map[y][x]
        if room and hasattr(room, "replace_on_room_clear"):
          self.blit_coords((y,x), Map.reward_room_colour)
    self.scale_surf()
  
  def update_room(self):
    cur_room = self.main_sub.current_room
    self.blit_conns(cur_room, Map.cur_room_colour)
    self.scale_surf()
    
  def blit_conns(self, cur_room, cur_room_colour):
    cur_pos = self.blit_coords(self.map.get_coords(cur_room), cur_room_colour)
    if cur_pos is None: return
    cur_pos = [cur_pos[0]+7, cur_pos[1]+3]
    for conn in cur_room.connections:
      if self.has_compass and hasattr(conn, "replace_on_room_clear"):
        old_room_colour = Map.reward_room_colour
      elif conn.been_visited:
        old_room_colour = Map.visited_room_colour
      else:
        old_room_colour = (128,128,128)
      pos = self.blit_coords(self.map.get_coords(conn), old_room_colour)
      pos = [pos[0]+7, pos[1]+3]
      self.pygame.draw.line(self.internal_surf, Map.path_colour, cur_pos, pos)
      self.blit_coords(self.map.get_coords(conn), old_room_colour)
    self.blit_coords(self.map.get_coords(cur_room), cur_room_colour)
    
  def blit_coords(self, coords, colour):
    try:
      coords = [coords[0]+1, self.map_size[1]-coords[1]+1]
    except TypeError: return 
    pos = (coords[0]*16,coords[1]*8)
    self.internal_surf.fill(colour, (pos,(15,7)))
    return pos