#!/usr/bin/env python

from ..living_base import Living

class Player(Living):
  persistant = True
  door_d = 6
  max_life = 20
  min_life = 20
  
  def __init__(self, parent):
    self.parent = parent
    super(Player, self).__init__(*parent.screen.get_center())
    self.config_manager = self.get_main().config_manager
    self.load_animation_sheet("player.anm2")
    self.current_anim = "WalkUp"
    self.run_anim(0)
    self.center()
    del self.x_pos
    del self.y_pos
    self.x -= self.surf.get_width()
    self.y -= self.surf.get_height()
    self.prev_dx = 0
    self.prev_dy = 0
    self.keys = 0
    self.multi_keys = 0
    self.boss_key = 0
    self.bombs = 200
    self.cooldown_timers = {
      "bomb": [0,0.5]
    }

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
    #Get the previous dx and dy state - what direction has the player moved in recently
    c_dx = cmp(self.dx, 0)
    c_dy = cmp(self.dy, 0)
    if c_dx or c_dy: self.prev_dx, self.prev_dy = c_dx, c_dy
    #Handle going through doors
    if old_x != self.x or old_y != self.y: return
    for axis in ((self.dx, self.door_d), (self.dy, self.door_d)):
      if abs(axis[0]) >= axis[1]:
        door = self.get_pygame().sprite.spritecollideany(self, self.get_entity_data().door, self.door_collide)
        if door and door.locked and door.unlockable():
          self.dx = self.dy = self.ddx = self.ddy = 0
        elif door and door.current_anim in ["Opened", "BrokenOpen"]:
          self.parent.load_room(door.room, door.pos_id)

  def take_damage(self, amount):
    if self.invincible: return
    self.life -= amount
    if self.life <= 0:
      return
    self.invincible = True
    
  def door_collide(self, s, door):
    #print s.rect.clip(door.rect).size[door.pos_id%2]
    return s.rect.clip(door.rect).size[door.pos_id%2]>=8
  
  def place_bomb(self):
    if self.bombs != 0 and self.cooldown_timers["bomb"][0] == 0:
      self.cooldown_timers["bomb"][0] = self.cooldown_timers["bomb"][1]
      self.bombs -= 1
      self.spawn_entity("animated.moveable.bomb", self.x+self.surf.get_width()/4, self.y+self.surf.get_height()/4)
      
  def use_sword(self):
    try:
      no_sword = len(self.get_entity_data().sword.sprites()) == 0
    except TypeError:
      no_sword = True
    if no_sword and not self.parent.scrolling:
      self.spawn_entity("animated.moveable.sword")