#!/usr/bin/env python

import inspect

class Screen(object):
  def __init__(self, surf, pygame):
    self.pygame = pygame
    names = ["blit", "get_size"]
    self.blit_rects = []
    self.blit_rects_old = []
    for name, val in inspect.getmembers(surf):
      if name not in names:
        try: setattr(self, name, val)
        except TypeError: pass
      elif name == "blit":
        self.blit_old = val
    self.size = surf.get_size()
    self.patch_im_load()
    
  def blit(self, *args, **kwargs):
    self.blit_rects.append(self.blit_func(*args, **kwargs))
    
  def blit_func(self, *args, **kwargs):
    args = list(args)
    args[1] = (args[1][0]*2, args[1][1]*2)
    return self.blit_old(*args, **kwargs)
    
  def blit_all(self):
    self.blit_rects=[self.get_rect()]
  
  def get_size(self):
    return (self.size[0]/2, self.size[1]/2)
  
  def get_center(self):
    return (self.size[0]/4, self.size[1]/4)
  
  def patch_im_load(self):
    self.old_im_load = self.pygame.image.load  
    self.pygame.image.load = self.im_load_patch
  
  def im_load_patch(self, *args, **kwargs):
    surf = self.old_im_load(*args, **kwargs)
    surf = self.pygame.transform.scale2x(surf)
    return surf
  