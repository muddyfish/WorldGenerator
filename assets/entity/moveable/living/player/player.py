#!/usr/bin/env python

from ..living_base import Living

class Player(Living):
  def __init__(self, parent):
    self.parent = parent
    x,y = self.get_main().screen.get_center()
    super(Player, self).__init__(x,y, 20)
    self.config_manager = self.get_main().config_manager
    #self.load_surfs()
    
  def move_pos(self, d_time):
    old_x, old_y =  self.x, self.y
    super(Player, self).move_pos(d_time)
    if old_x != self.x or old_y != self.y: return
    for axis in ((self.ddx, self.max_ddx), (self.ddy, self.max_ddy)):
      if abs(axis[0]) == axis[1]:
        door = self.get_pygame().sprite.spritecollideany(self, self.get_entity_data().door, self.door_collide)
        if door and door.open:
          self.parent.load_room(door.room, door.pos_id)
  
  def door_collide(self, s, door):
    return s.rect.clip(door.rect).size[door.pos_id%2]>=3
    
  #def load_surfs(self):
  #  im_path = self.config_manager.get_path(self.get_path(), "frames.png")
  #  surf = self.load_surf(self.get_pygame().image.load(im_path))
  #  self.subsurf = self.load_surf(surf.subsurface(((64,0),(64,64))))