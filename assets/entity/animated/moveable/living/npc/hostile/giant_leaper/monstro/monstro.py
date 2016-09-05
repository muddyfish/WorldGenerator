#!/usr/bin/env python

from ..leaper_base import GiantLeaper

class Monstro(GiantLeaper):
  anim_speed = 1.0/30
  max_life = 10
  min_life = 8
  difficulty = 5
  
  def __init__(self, x, y):
    super(Monstro, self).__init__(x,y)
    self.load_animation_sheet("monstro.anm2")
    self.finish_anim_funcs = {
        "Appear": lambda: self.load_animation("Death"),
        "Death": lambda: self.load_animation("JumpUp"),
        "JumpDown": lambda: self.load_animation("JumpUp"),
        "JumpUp": lambda: self.load_animation("Taunt"),
        "Taunt": lambda: self.load_animation("Walk"),
        "Walk": lambda: self.load_animation("Walk"),
      }
    self.run_anim(0)
    self.center(self.x_pos,self.y_pos)
    
  def run(self, d_time):
    super(Monstro, self).run(d_time)
    self.run_anim(d_time)
    self.center(self.x_pos,self.y_pos)
  
  @classmethod
  def spawn_method(cls):
    return cls.spawn_central