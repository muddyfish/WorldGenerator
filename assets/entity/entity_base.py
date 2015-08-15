#!/usr/bin/env python

import os, sys, inspect
import __main__

class Entity(__main__.pygame.sprite.Sprite):
  group_spawn = 1
  persistant = False
  
  def __init__(self, x,y):
    self.get_pygame().sprite.Sprite.__init__(self)
    self.dirty = True
    if not hasattr(self, "surf"):
      self.surf = self.load_surf(self.get_pygame().surface.Surface((32,32)))
    self.pos = [x,y]
    self.x = self.pos[0]
    self.y = self.pos[1]
    self.update_collision()
    self.groups = [cls.__name__.lower() for cls in inspect.getmro(self.__class__)[:-2]]
    for group in self.groups:
      attr = getattr(self.get_entity_data(), group)
      if isinstance(attr, self.get_main().databin.__class__):
        attr = self.get_pygame().sprite.LayeredUpdates()
        setattr(self.get_entity_data(), group, attr)
      attr.add(self)      
  
  def __getattribute__(self, attr):
    if attr == "image": return self.surf
    return super(Entity, self).__getattribute__(attr)
  
  def __setattr__(self, attr, val):
    if attr in ["x", "y"]:
      setattr(self.rect, attr, val)
      self.pos[attr=="y"] = val
    super(Entity, self).__setattr__(attr, val)
  
  def __del__(self):
    self.kill()
  
  def run(self, d_time):
    pass
  
  def get_pygame(self):
    return __main__.pygame
  
  def get_main(self):
    return __main__.main_class

  def get_entity_data(self):
    return self.get_main().databin.entity_data
  
  def get_player(self):
    return self.get_main().databin.entity_data.player.sprites()[0]
  
  def get_blit(self):
    if self.dirty:
      return self.get_main().screen.blit
    return self.get_main().screen.blit_func
  
  def load_surf(self, surf):
    self.rect = surf.get_rect()
    try:
      self.rect.x = self.x
      self.rect.y = self.y
    except AttributeError: pass
    return surf
  
  def get_path(self, dirname = None):
    return os.path.join(*[os.path.dirname(__main__.__file__)]+self.__class__.__module__.split(".")[:-1])+os.sep
  
  def blit(self):
    self.get_blit()(self.surf, (self.x, self.y))
    
  def update_collision(self):
    self.rect.size = self.surf.get_size()
    self.rect.width/=2
    self.rect.height/=2

  def get_collide(self, entities = None):
    if entities == None: entities = self.get_entity_data().entity
    collide = self.get_pygame().sprite.spritecollide(self, entities, False)
    try:
      collide.remove(self)
    except ValueError: pass
    return collide







