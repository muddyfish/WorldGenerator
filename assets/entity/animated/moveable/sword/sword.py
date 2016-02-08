#!/usr/bin/env python

from ..moveable_base import Moveable
import math

class Sword(Moveable):
  speed = 10.0
  circle_radius = 30
  damage_dealt = 2
  update_bounding_box = False
  no_respawn = True
  
  def __init__(self):
    self.screen = self.get_main().screen
    self.bounding_rect = self.get_pygame().Rect([4,4,40,40])
    self.rect = self.bounding_rect.copy()
    x,y = self.get_player().x, self.get_player().x
    super(Sword, self).__init__(x,y)
    self.load_animation_sheet("sword.anm2")
    self.finish_anim_funcs = {
        "Rotation": lambda: self.despawn()
      }
    self.load_animation("Rotation")
    
    self.player = self.get_player()
    dx = self.player.prev_dx
    dy = self.player.prev_dy
    self.offset = {(-1, 0): 1  ,# W
                   (-1, 1): 1  ,
                   (-1,-1): 0  ,#NW 
                   ( 0, 0):-1  ,#Default
                   ( 0, 1): 2  ,#S
                   ( 0,-1):-1  ,#N
                   ( 1, 0):-2  ,# E
                   ( 1, 1):-0.5,
                   ( 1,-1):-1.5,#NE
                   }[(dx,dy)]
    self.run(0)
      
  def run(self, d_time):
    self.offset -= d_time * self.speed
    self.rotate_amount = self.offset/math.pi*180
    super(Sword, self).run(d_time)
    self.run_anim(d_time)
    self.x = self.player.x + self.player.rect.width/2  + self.circle_radius * math.sin(self.offset)
    self.y = self.player.y + self.player.rect.height/2 + self.circle_radius * math.cos(self.offset)
    hurtable = self.get_entity_data().living
    for entity in self.get_collide(hurtable):
      if entity is not self.player:
        entity.take_damage(self.damage_dealt)