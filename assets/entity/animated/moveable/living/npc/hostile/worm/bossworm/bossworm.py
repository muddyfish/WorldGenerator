#!/usr/bin/env python
import random

from ..worm_base import Worm

class BossWorm(Worm):
  max_life = 10
  min_life = 8
  length = 8
  damage_dealt = 2
  no_acc = True
  directions = {"UP":   ( 0,-1),
                "DOWN": ( 0, 1),
                "LEFT": (-1, 0),
                "RIGHT":( 1, 0)}
  direction_ids = ["UP", "DOWN", "LEFT", "RIGHT"]
  
  def __init__(self, x, y, body_type="Head"):
    super(BossWorm, self).__init__(x,y)
    self.load_animation_sheet("boss_worm.anm2")
    self.finish_anim_funcs = {
        "DeathHead": lambda: self.despawn(),
        "DeathBody01": lambda: self.despawn()
    }
    self.UP_BOUND = 0
    self.LEFT_BOUND = 16
    self.RIGHT_BOUND = 384
    self.DOWN_BOUND = 224
    self.speed = 64
    self.body_type = body_type
    if self.body_type == "Head":      
      self.body_parts = []
      self.head_choose_direction(None)
      self.register_event("collide_wall", self.head_choose_direction)
      self.head = self
      self.body_parts.append(self.spawn_entity("animated.moveable.living.npc.hostile.worm.bossworm", self.x, self.y, "Butt"))
      for i in range(self.length-2):
        self.body_parts.append(self.spawn_entity("animated.moveable.living.npc.hostile.worm.bossworm", self.x, self.y, "Body"))
      for i, part in enumerate(self.body_parts):
        dx, dy = self.directions[self.direction]
        part.x_pos -= dx * (self.length-i) * 12 - dx*8
        part.y_pos -= dy * (self.length-i) * 12 - dy*8
        part.direction = self.direction
        part.center(part.x_pos, part.y_pos)
    else:
      self.milestones = []
    self.run_anim(0)
    self.center(self.x_pos,self.y_pos)
    
  def run(self, d_time):
    self.dx = self.directions[self.direction][0] * self.speed
    self.dy = self.directions[self.direction][1] * self.speed
    super(BossWorm, self).run(d_time)
    self.run_anim(d_time)
    self.center(self.x_pos,self.y_pos)
    if self.body_type != "Head":
      self.check_milestones()
    
  def head_choose_direction(self, cur_dir):
    self.direction = random.choice(BossWorm.direction_ids)
    self.direction = "DOWN"
    self.load_animation(self.get_anim_name())
    for body_part in self.body_parts:
      body_part.add_milestone(self.x_pos, self.y_pos-8, self.direction)
      
  def add_milestone(self, x,y, new_direction):
    self.milestones.append((x,y, new_direction))
    
  def check_milestones(self):
    if self.milestones:
      x, y, new_direction = self.milestones[0]
      print abs(self.x_pos-x), abs(self.y_pos-y)
      if abs(self.x_pos-x) <= 1 and abs(self.y_pos-y) <= 1:
        self.x_pos = x
        self.y_pos = y
        self.direction = new_direction
        self.load_animation(self.get_anim_name())
        del self.milestones[0]

  def get_anim_name(self):
    if self.body_type == "Butt":
      return "Butt"
    direction = self.direction.title()
    if self.body_type == "Body" and direction in ["Left", "Right"]:
      direction = "Hori"
    return "Walk"+self.body_type+direction
  
  @classmethod
  def spawn_method(cls):
    return cls.spawn_central