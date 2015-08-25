#!/usr/bin/env python

from ..hud import HUD

class Bomb(HUD):
  transparent_colour = None
  def __init__(self):
    self.pygame = self.get_pygame()
    self.screen = self.get_main().screen
    super(Bomb, self).__init__(29,self.screen.get_height()/2-80)
    self.load_animation_sheet("bomb.anm2")
    self.current_anim = "Idle"
    self.run_anim(0)
    
  def run(self, d_time):
    bombs = self.get_player().bombs
    #print bombs