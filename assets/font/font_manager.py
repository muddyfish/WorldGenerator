#!/usr/bin/env python

from ..manager_base import ManagerBase


class FontManager(ManagerBase):
  def __init__(self):
    self.font_module = self.get_pygame().font
    self.fonts = {}
  
  def __getitem__(self, name):
    return self.fonts[name]
  
  def __hasitem__(self, name):
    return name in self.fonts  
    
  def register_font(self, store_name, font_name = "verdana", size = 12, bold = False, italic = False):
    self.fonts[store_name] = self.font_module.SysFont(font_name, size, bold, italic)
  