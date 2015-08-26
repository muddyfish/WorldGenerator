#!/usr/bin/env python

from ..living_base import Living

class Player(Living):
  persistant = True
  door_dd = 6
  
  def __init__(self, parent):
    self.parent = parent
    super(Player, self).__init__(0,0, 20)
    self.x,self.y = self.get_main().screen.get_center()
    self.config_manager = self.get_main().config_manager
    self.keys = 0
    self.bombs = 5
    
  def move_pos(self, d_time):
    #print self.ddx, self.ddy
    old_x, old_y =  self.x, self.y
    super(Player, self).move_pos(d_time)
    if old_x != self.x or old_y != self.y: return
    for axis in ((self.ddx, self.door_dd), (self.ddy, self.door_dd)):
      if abs(axis[0]) >= axis[1]:
        door = self.get_pygame().sprite.spritecollideany(self, self.get_entity_data().door, self.door_collide)
        if door and door.locked and self.keys != 0:
          self.keys -= 1
          door.locked = False
          door.open = True
          door.current_anim = "KeyOpen"
          self.ddx = self.ddy = 0
        elif door and door.current_anim == "Opened":
          self.parent.load_room(door.room, door.pos_id)
  
  def door_collide(self, s, door):
    #print s.rect.clip(door.rect).size[door.pos_id%2]
    return s.rect.clip(door.rect).size[door.pos_id%2]>=8