#!/usr/bin/env python

from ..hud import HUD

class Bomb(HUD):
  transparent_colour = None
  def __init__(self):
    self.pygame = self.get_pygame()
    self.screen = self.get_main().screen
    self.get_main().fonts.register_font("bomb_count", "verdana", 18)
    super(Bomb, self).__init__(24,self.screen.get_height()/2-80)
    self.load_animation_sheet("bomb.anm2")
    self.finish_anim_funcs = {
        "Collect_Pulse": lambda: self.load_animation("Idle")
      }
    self.current_anim = "Idle"
    self.run_anim(0)
    self.old_bombs = self.get_player().bombs
    self.clean_surf = self.surf
    self.update_surf()
    
  def run(self, d_time):
    updated = self.run_anim(d_time)
    bombs = self.get_player().bombs
    if bombs != self.old_bombs:
      self.old_bombs = bombs
      self.update_surf()
      updated = True
      self.current_anim = "Collect_Pulse"
    if updated:
      self.surf.blit(self.amount, (8,32))
    #print bombs
    
  def update_surf(self):
    self.amount = self.get_main().fonts["bomb_count"].render("%d"%self.old_bombs, True, (255,255,255))