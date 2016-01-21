#!/usr/bin/env python

from ..animate import Animation

import glob, os

class Door(Animation):
  def __init__(self, pos_id, room, cur_room):
    self.config_manager = self.get_main().config_manager
    self.pos_id = pos_id
    self.room = room
    self.current_room = cur_room
    #Set the door id so that both sides of the door have the same graphic
    #The id's are ordered in suvh a way that higher priority id's are higher
    self.door_id = max(self.room.door_id, cur_room.door_id)
    if self.door_id in [26]: self.transparent_colour = None
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
    self.locked = bool(self.room.locked)
    self.keytype = room.locked
    self.open = cur_room.cleared and not self.locked
    self.set_pos()
    if self.locked: self.current_anim = "KeyClosed"
    self.broken = False
    self.first_tick = True
    self.run_anim(0)
  
  def __setattr__(self, attr, val):
    if attr in ["open", "locked"]:
      if attr == "locked":
        if val == False:
          self.room.locked = val
      else:
        try:
          self.get_anim_state(val, getattr(self, attr))
        except AttributeError: pass
    super(Door, self).__setattr__(attr, val)
  
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

  def get_anim_state(self, opened, old_opened):
    if self.broken:
      self.current_anim = "BrokenOpen"
    elif self.locked:
      self.current_anim = "KeyClosed"
    elif opened:
      if old_opened:
        self.current_anim = "Opened"
      else:
        self.current_anim = "Open"
    else:
      if old_opened:
        self.current_anim = "Close"
      else:
        self.current_anim = "Closed"
    
  def run(self, d_time):
    if self.first_tick:
      #Only update the animation state of the door after the scrolling is finished
      self.first_tick = False
      self.get_anim_state(self.open, True)
    self.run_anim(d_time)
      
  def unlockable(self):
    """Is a door unlockable"""
    if not self.current_room.cleared:
      #Rooms must be cleared before any doors can be unlocked
      return False
    player = self.get_player()
    #How many keys are required to open the door
    required = 1
    #Multi-keys need 3 to open a door
    if self.keytype == "multi_keys":
      required = 3
    amount = getattr(player, self.keytype)
    if amount >= required:
      setattr(player, self.keytype, amount-required)
      self.unlock()
      return True
    return False
      
  def unlock(self):
    """Unlock a door"""
    self.locked = False
    self.open = True
    self.current_anim = "KeyOpen"
    
  def update_collision(self):
    """Update the collision detection for a door"""
    if not hasattr(self, "frames"): return
    self.rect = self.frames[3][0].surf.get_bounding_rect()
    self.rect.width, self.rect.height = (self.rect.width/2-14, self.rect.height/2-14)[::cmp(self.pos_id%2,0.5)]
    if self.pos_id%2:
      self.rect.x, self.rect.y = self.x+7, self.y+23
    else:
      self.rect.x, self.rect.y = self.x+23, self.y+7
    #print self.pos_id, self.pos_id%2, self.rect
    
  def load_door_surfs(self):
    """Load the correct animation file for a door"""
    anm_filename = glob.glob(os.path.join(self.get_path(), "anm", "door_%02d_*.anm2"%self.door_id))[0]
    self.load_animation_sheet(anm_filename)
    