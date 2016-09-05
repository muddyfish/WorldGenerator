#!/usr/bin/env python

from ..moveable_base import Moveable

class Explosion(Moveable):
  transparent_colour = (0,0,0)
  anim_speed = 1.0/12
  no_respawn = True
  damage_dealt = 4
  
  def __init__(self, x, y):
    self.pygame = self.get_pygame()
    self.screen = self.get_main().screen
    super(Explosion, self).__init__(x,y)
    self.load_animation_sheet("explosion.anm2")
    self.finish_anim_funcs = {
        "Explode": self.despawn
      }
    self.run_anim(0)
    self.center(x,y)
    
  def run(self, d_time):
    self.run_anim(d_time)
    self.bounding_rect = self.surf.get_bounding_rect()
    self.update_collision()
    hurtable = self.get_entity_data().living
    for entity in self.get_collide(hurtable):
      entity.take_damage(self.damage_dealt)
    doors = self.get_entity_data().door
    for door in self.get_collide(doors):
      if not door.locked:
        door.open = True
        door.broken = True
        door.current_anim = "BrokenOpen"
    bombs = self.get_entity_data().bomb
    for bomb in self.get_collide(bombs):
      bomb.explode()