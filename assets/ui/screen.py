#!/usr/bin/env python

import inspect

class Screen(object):
  def __init__(self, surf):
    self.blit_rects = []
    self.blit_rects_old = []
    for name, val in inspect.getmembers(surf):
      if name != "blit":
        try: setattr(self, name, val)
        except TypeError: pass
      else:
        self.blit_func = val
    self.size = self.get_size()
    
  def blit(self, *args, **kargs):
    self.blit_rects.append(self.blit_func(*args, **kargs))
    
  def blit_all(self):
    self.blit_rects=[((0,0), self.size)]
    