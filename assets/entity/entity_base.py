#!/usr/bin/env python

import __main__

class Entity(__main__.pygame.sprite.Sprite):
  def __init__(self, x,y):
    self.get_pygame().sprite.Sprite.__init__(self)
    self.pos = [x,y]
    self.x = self.pos[0]
    self.y = self.pos[1]
    self.dirty = True
    self.surf = self.load_surf(self.get_pygame().surface.Surface((32,32)))
    self.rect = self.surf.get_rect()
    self.rect.x = self.pos[0]
    self.rect.y = self.pos[1]
    self.get_entities().append(self)
  
  def __getattribute__(self, attr):
    if attr == "image": return self.surf
    return super(Entity, self).__getattribute__(attr)
  
  def run(self, d_time):
    pass
  
  def get_pygame(self):
    return __main__.pygame
  
  def get_main(self):
    return __main__.main_class

  def get_entities(self):
    return self.get_main().databin.entity_data.entities
  
  def get_blit(self):
    if self.dirty:
      return self.get_main().screen.blit
    return self.get_main().screen.blit_func
  
  def load_surf(self, surf):
    return surf  
  
  def blit(self):
    self.get_blit()(self.surf, (self.x, self.y))
    











