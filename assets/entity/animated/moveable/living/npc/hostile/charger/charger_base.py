#!/usr/bin/env python

from ..hostile_base import NPCHostile
import random

class Charger(NPCHostile):
  directions = {"UP":   ( 0,-1),
                "DOWN": ( 0, 1),
                "LEFT": (-1, 0),
                "RIGHT":( 1, 0)}
  direction_ids = ["UP", "DOWN", "LEFT", "RIGHT"]
  chance_ignore = 0.5
  ignore_player_time = 2
  reconsider_direction_time_min = 3
  reconsider_direction_time_max = 5
  
  def __init__(self,x,y):
    super(Charger, self).__init__(x,y)
    self.register_event("collide_wall", self.choose_direction)
    self.register_event("player_xy", self.player_direction)
    self.mode = "move"
    self.ignore_time = 0
    self.update_reconsider_time()
  
  def run(self, d_time):
    if self.ignore_time != 0:
      self.ignore_time = max(0, self.ignore_time - d_time)
    if self.reconsider_time != 0:
      self.reconsider_time = max(0, self.reconsider_time - d_time)
    elif self.mode != "attack":
      self.update_reconsider_time()
      self.choose_direction(None)
    super(Charger, self).run(d_time)
    
  def choose_direction(self, wall_id):
    self.direction = random.choice(Charger.directions.keys())
    self.mode = "move"
    self.speed = self.speed_normal
    self.max_dx = self.speed_normal
    self.max_dy = self.speed_normal
    self.set_direction()
    
  def player_direction(self, face):
    new_direction = Charger.direction_ids[face]
    no_charge = False
    no_charge |= self.mode == "attack"
    no_charge |= self.ignore_time != 0
    if self.ignore_time == 0 and \
       random.random() <= self.__class__.chance_ignore and \
       self.get_distance() >= 100:
      no_charge |= (new_direction != self.direction)
      self.ignore_time = self.__class__.ignore_player_time
    if no_charge: return
    self.direction = new_direction
    self.mode = "attack"
    self.speed = self.speed_attack
    self.max_dx = self.speed_attack
    self.max_dy = self.speed_attack
    self.set_direction()
    
  def set_direction(self):
    self.load_animation(("%s %s"%(self.mode, self.direction)).title())
    movement = Charger.directions[self.direction]
    self.cddx = movement[0]*self.speed
    self.cddy = movement[1]*self.speed
    
  def update_reconsider_time(self):
      self.reconsider_time = random.randint(
        self.__class__.reconsider_direction_time_min,
        self.__class__.reconsider_direction_time_max)    