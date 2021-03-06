#!/usr/bin/env python

from ..animate import Animation
import os, __main__

class Logo(Animation):
  auto_resize = False
  def __init__(self):
    self.screen = self.get_main().screen
    super(Logo, self).__init__(0,0)
    self.finish_anim_funcs = {
      "BlueEyedGames": lambda: self.load_animation("OKGraphics"),
      "OKGraphics": lambda: self.get_main().databin.current_subscription.finish()
    }
    self.load_animation_sheet("logo.anm2")
    self.run_anim(0)
    self.pygame = self.get_pygame()
    
  
  def run(self, d_time):
    self.run_anim(d_time)
  
  def load_spritesheets(self):
    self.spritesheets = {k: self.screen.old_im_load(
      os.path.join(os.path.dirname(__main__.__file__), "assets", "entity", "animated", "logo", "gfx", spritesheet))
     for k, spritesheet in self.spritesheet_xml.iteritems()}