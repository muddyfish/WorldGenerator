#!/usr/bin/env python

import time
from ..ui import UI
from assets.entity.animated.logo.logo import Logo

class MapUI(UI):
  def __init__(self):
    super(MapUI, self).__init__()
    self.config_manager = self.get_main().config_manager
    self.old_time = time.clock()
    self.logo = Logo(self)
    
  def draw(self):
    self.screen.fill((0,0,0))
    self.get_blit(self.logo.dirty)(self.logo.surf, (0,0))
      
  def run(self):
    c_time = time.clock()
    self.d_time = c_time - self.old_time
    self.old_time = c_time
    self.logo.run(self.d_time)
  
  def get_blit(self, dirty):
    if dirty:
      return self.screen.blit
    return self.screen.blit_func
  
  def finish(self):
    self.get_main().subscription_manager.current_subscription_id = "map_viewer"
    self.get_main().subscription_manager.load_subscription()