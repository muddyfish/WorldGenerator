#!/usr/bin/env python

from ..entity_base import Entity

import glob, os

class Door(Entity):
  finished_anim = 12.5
  def __init__(self, pos_id, door_id = 1):
    self.door_id = door_id
    self.pos_id = pos_id
    super(Door, self).__init__(0,0)
    self.config_manager = self.get_main().config_manager
    self.open = False
    self.locked = False
    self.anim_state = 0
    self.load_door_surfs()
    self.load_state(0)
    pos = [100,100]
    coord = 1-pos_id%2
    screen = self.get_main().screen
    if pos_id>>1:
      pos[coord] = screen.get_size()[coord]-self.surf.get_size()[coord]/2-12
    else:
      pos[coord] = 12
    coord = pos_id%2
    pos[coord] = screen.get_center()[coord]-self.surf.get_size()[coord]/4
    self.x, self.y = pos
    #print self.x, self.y, pos_id>>1, pos_id%2
    
  def run(self, d_time):
    if self.anim_state != 0 and self.anim_state < self.finished_anim:
      self.load_state(d_time)
    elif not self.open:
      self.open = True
      self.load_state(d_time)
    
  def load_state(self, d_time):
    pygame = self.get_pygame()
    if self.open:
      self.anim_state += 40*d_time
      #print self.anim_state
      self.surf = pygame.surface.Surface((128,128), pygame.SRCALPHA)
      self.surf.set_clip((40,36), (50,42))
      self.surf.blit(self.open_surf, (0,0))
      self.surf.blit(self.door_l, (-2*self.anim_state,0))
      self.surf.blit(self.door_r, (2*self.anim_state,0))
      self.surf.set_clip()
      self.surf.blit(self.frame_surf, (0,0))
    else:
      self.surf = pygame.surface.Surface((128,128), pygame.SRCALPHA)
      self.surf.blit(self.door_l, (0,0))
      self.surf.blit(self.door_r, (0,0))
      self.surf.blit(self.frame_surf, (0,0))
    self.surf = pygame.transform.rotate(self.surf, 90*self.pos_id)
    
  def load_door_surfs(self):
    im_path = self.config_manager.get_path(self.get_path(), "door_%02d.png"%self.door_id)
    surf = self.load_surf(self.get_pygame().image.load(im_path))
    self.frame_surf = surf.subsurface(((0,0),(128,128)))
    self.open_surf = surf.subsurface(((128,0),(128,128)))
    self.door_l = surf.subsurface(((0,128),(128,128)))
    self.door_r = surf.subsurface(((128,128),(128,128)))