#!/usr/bin/env python

from ..hostile_base import NPCHostile
import random

class Charger(NPCHostile):
  directions = {"UP":   ( 0,-1),
                "DOWN": ( 0, 1),
                "LEFT": (-1, 0),
                "RIGHT":( 1, 0)}
  
  def __init__(self,x,y):
    super(Charger, self).__init__(x,y)
    self.register_event("collide_wall", self.choose_direction)
    self.register_event("player_xy", self.player_direction)
    self.mode = "move"
    
  def choose_direction(self, wall_id):
    self.direction = random.choice(Charger.directions.keys())
    self.mode = "move"
    self.speed = self.speed_normal
    self.max_dx = self.speed_normal
    self.max_dy = self.speed_normal
    self.set_direction()
    
  def player_direction(self, face):
    if self.mode == "attack":return
    if   face==0: self.direction = "UP"
    elif face==1: self.direction = "DOWN"
    elif face==2: self.direction = "LEFT"
    elif face==3: self.direction = "RIGHT"
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