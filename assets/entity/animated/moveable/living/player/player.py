#!/usr/bin/env python

from ..living_base import Living
from ...bomb.bomb import Bomb

class Player(Living):
  persistant = True
  door_d = 6
  max_life = 20
  min_life = 20
  
  def __init__(self, parent):
    self.parent = parent
    super(Player, self).__init__(0,0)
    self.screen = self.get_main().screen
    self.config_manager = self.get_main().config_manager
    self.load_animation_sheet("player.anm2")
    self.current_anim = "WalkUp"
    self.keys = 0
    self.multi_keys = 0
    self.boss_key = 0
    self.bombs = 2
    self.cooldown_timers = {
      "bomb": [0,0.5]
    }
    self.run_anim(0)

  def run(self, d_time):
    super(Player, self).run(d_time)
    self.run_anim(d_time)
    for timer in self.cooldown_timers:
      self.cooldown_timers[timer][0] = max(0, self.cooldown_timers[timer][0]-d_time)
    self.cddx = 0
    self.cddy = 0
    
  def move_pos(self, d_time):
    #print self.ddx, self.ddy
    old_x, old_y =  self.x, self.y
    super(Player, self).move_pos(d_time)
    if old_x != self.x or old_y != self.y: return
    for axis in ((self.dx, self.door_d), (self.dy, self.door_d)):
      if abs(axis[0]) >= axis[1]:
        door = self.get_pygame().sprite.spritecollideany(self, self.get_entity_data().door, self.door_collide)
        if door and door.locked and door.unlockable():
          self.dx = 0
          self.dy = 0
          self.ddx = 0
          self.ddy = 0
        elif door and door.current_anim == "Opened":
          self.parent.load_room(door.room, door.pos_id)
  
  def door_collide(self, s, door):
    #print s.rect.clip(door.rect).size[door.pos_id%2]
    return s.rect.clip(door.rect).size[door.pos_id%2]>=8
  
  def place_bomb(self):
    if self.bombs != 0 and self.cooldown_timers["bomb"][0] == 0:
      self.cooldown_timers["bomb"][0] = self.cooldown_timers["bomb"][1]
      self.bombs -= 1
      bomb = Bomb(self.x, self.y)
      bomb.spawn()