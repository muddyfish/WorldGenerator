#!/usr/bin/env python

import __main__

class UI(object):
  def __init__(self):
    self.get_pygame().key.set_repeat()
    self.subscription_id = self.__class__.__name__
    self.screen = self.get_screen()
    
  def get_main(self):
    return __main__.main_class
    
  def get_screen(self):
    return self.get_main().screen
    
  def get_pygame(self):
    return __main__.pygame
    
  def run(self):
    pass
    
  def draw(self):
    pass