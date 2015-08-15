#!/usr/bin/env python

from ..animate import Animation

import glob, os

class Door(Animation):
  def __init__(self, pos_id, room, cur_room):
    self.config_manager = self.get_main().config_manager
    self.pos_id = pos_id
    self.room = room
    self.door_id = max(self.room.door_id, cur_room.door_id)
    if self.door_id in [26]: self.transparent_colour = None
    self.auto_update = True
    super(Door, self).__init__(0,0)
    self.rotate_amount = 90*self.pos_id
    self.old_anim = ""
    self.finish_anim_funcs = {
      "KeyOpen": lambda: self.load_animation("Opened"),
      "Open": lambda: self.load_animation("Opened"),
      "KeyOpenNoKey": lambda: self.load_animation("Opened"),
      "GoldenKeyOpen": lambda: self.load_animation("Opened"),
      "Close": lambda: self.load_animation("Closed"),
      "Break": lambda: self.load_animation("BrokenOpen")
    }
    self.load_door_surfs()
    self.locked = self.room.locked
    self.open = False#not self.room.locked
    self.set_pos()
    self.current_anim = "Opened"
    if self.locked: self.current_anim = "KeyClosed"
    self.first_tick = True
  
  def __setattr__(self, attr, val):
    super(Door, self).__setattr__(attr, val)
    if attr in ["open", "locked"] and self.auto_update:
      if attr == "locked":
        self.room.locked = val
      try:
        self.get_anim_state()
      except AttributeError: pass
  
  def set_pos(self):
    pos = [0,0]
    coord = 1-self.pos_id%2
    screen = self.get_main().screen
    if self.pos_id>>1:
      pos[coord] = screen.get_size()[coord]-self.surf.get_size()[coord]-28
    else:
      pos[coord] = 12
    coord = 1-coord
    pos[coord] = screen.get_center()[coord]-self.surf.get_size()[coord]
    self.x, self.y = pos
    #print self.x, self.y, pos_id>>1, pos_id%2

  def get_anim_state(self):
    anim = ""
    if self.locked:
      anim += "Key"
    if self.open:
      anim += "Open"
      if self.current_anim == "Opened": anim += "ed"
    else:
      anim += "Close"
      if self.locked: anim += "d"
    self.current_anim = anim
    
  def run(self, d_time):
    self.run_anim(d_time)
    if self.first_tick:
      self.first_tick = False
      self.get_anim_state()
    
  def update_collision(self):
    if not hasattr(self, "frames"): return
    self.rect = self.frames[3][0].surf.get_bounding_rect()
    self.rect.width, self.rect.height = (self.rect.width/2-14, self.rect.height/2-14)[::cmp(self.pos_id%2,0.5)]
    if self.pos_id%2:
      self.rect.x, self.rect.y = self.x+7, self.y+23
    else:
      self.rect.x, self.rect.y = self.x+23, self.y+7
    #print self.pos_id, self.pos_id%2, self.rect
    
  def load_door_surfs(self):
    im_path = glob.glob(os.path.join(self.get_path(), "gfx", "door_%02d*.png"%self.door_id))[0]
    anm_filename = glob.glob(os.path.join(self.get_path(), "anm", "door_%02d_*.anm2"%self.door_id))[0]
    self.load_animation_sheet(anm_filename)
    