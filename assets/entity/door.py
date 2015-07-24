#!/usr/bin/env python

from entity_base import Entity

import glob, os

class Door(Entity):
  finished_anim = 12.5
  def __init__(self, pos_id, room, door_id = 1):
    self.pos_id = pos_id
    self.room = room
    self.door_id = door_id
    super(Door, self).__init__(0,0)
    self.config_manager = self.get_main().config_manager
    self.anim_state = self.finished_anim
    self.load_door_surfs()
    self.locked = self.room.locked
    self.open = False
    self.set_pos()
  
  def __setattr__(self, attr, val):
    old_val = getattr(self, attr, None)
    super(Door, self).__setattr__(attr, val)
    if attr in ["open", "locked"]:
      d_time = 0.0001
      if attr == "locked":
        if old_val: self.anim_state = 0.0
        self.room.locked = val
      try:
        self.load_state(d_time)
      except AttributeError: pass
  
  def set_pos(self):
    pos = [0,0]
    coord = 1-self.pos_id%2
    screen = self.get_main().screen
    if self.pos_id>>1:
      pos[coord] = screen.get_size()[coord]-self.surf.get_size()[coord]/2-12
    else:
      pos[coord] = 12
    coord = 1-coord
    pos[coord] = screen.get_center()[coord]-self.surf.get_size()[coord]/4
    self.x, self.y = pos
    #print self.x, self.y, pos_id>>1, pos_id%2
    
  def run(self, d_time):
    if self.anim_state != 0 and self.anim_state < self.finished_anim:
      self.load_state(d_time)
    #elif not self.open:
    #  self.open = True
    #  self.load_state(d_time)
    
  def load_state(self, d_time):
    pygame = self.get_pygame()
    door_r = self.door_r
    if self.locked: door_r = self.door_lock
    if self.open and not self.locked:
      self.anim_state += 40*d_time
      #print self.anim_state
      self.surf = pygame.surface.Surface((128,128), pygame.SRCALPHA)
      self.surf.set_clip((40,36), (50,42))
      self.surf.blit(self.open_surf, (0,0))
      self.surf.blit(self.door_l, (-2*self.anim_state,0))
      self.surf.blit(door_r, (2*self.anim_state,0))
      self.surf.set_clip()
      self.surf.blit(self.frame_surf, (0,0))
    else:
      self.surf = pygame.surface.Surface((128,128), pygame.SRCALPHA)
      self.surf.blit(self.door_l, (0,0))
      self.surf.blit(door_r, (0,0))
      self.surf.blit(self.frame_surf, (0,0))
    self.surf = pygame.transform.rotate(self.surf, 90*self.pos_id)
    #self.surf.fill((0,0,128))
    self.update_collision()
    if self.pos_id%2:
      self.rect.y = self.get_main().screen.get_center()[1]-6
      self.rect.height = 11
    else:
      self.rect.x = self.get_main().screen.get_center()[0]-6
      self.rect.width = 11
    
  def load_door_surfs(self):
    im_path = glob.glob(self.config_manager.get_path(self.get_path("grid"), "door_%02d*.png"%self.door_id))[0]
    surf = self.load_surf(self.get_pygame().image.load(im_path))
    self.frame_surf = surf.subsurface(((0,0),(128,128)))
    self.open_surf = surf.subsurface(((128,0),(128,128)))
    self.door_l = surf.subsurface(((0,128),(128,128)))
    self.door_r = surf.subsurface(((128,128),(128,128)))
    self.door_lock = surf.subsurface((128,256), (128,128))