#!/usr/bin/env python
from ..moveable_base import Moveable
import random, math, __main__

class Living(Moveable):
  max_life = 16
  min_life = 16
  vulnerable = []
  ineffective = []
  immune = []
  invincible = False
  invincible_time = 0.5
  use_random = True
  
  def __init__(self, x,y):
    self.life = random.randrange(self.min_life, self.max_life+1)  
    self.screen = self.get_main().screen
    self.x_pos, self.y_pos = x, y
    self.x, self.y = x, y
    super(Living, self).__init__(x,y)
  
  def take_damage(self, amount):
    if self.invincible: return
    self.life -= amount
    if self.life <= 0:
      self.despawn()
      return
    self.invincible = True
    
  def run(self, d_time):
    super(Living, self).run(d_time)
    if self.invincible and not self.__class__.invincible:
      self.invincible_time -= d_time
      if self.invincible_time <= 0:
        self.invincible_time = self.__class__.invincible_time
        self.invincible = False
  
  def get_blit(self):
    if self.invincible and not self.__class__.invincible:
      if int(self.invincible_time*10)%2:
        return lambda x,y:0
    return self.get_subscription().get_blit(self.dirty)
  
  @classmethod
  def spawn_group(cls, amount):
    return cls.spawn_method()(amount)
    
  @classmethod
  def spawn_circular(cls, amount):
    entities = []
    screen = __main__.main_class.screen
    center = screen.get_center()
    if cls.use_random:
      offset = random.random()*2*math.pi
    else:
      offset = 0
    for i in range(amount):
      x = cls.circle_radius * math.sin((2*math.pi*i+offset)/amount)
      y = cls.circle_radius * math.cos((2*math.pi*i+offset)/amount)
      entities.append(cls(center[0]+x,center[1]+y, spawn_id = i))
    return entities
  
  @classmethod
  def spawn_wall(cls, amount):
    entities = []
    x_length = Living.RIGHT_BOUND - Living.LEFT_BOUND
    y_length = Living.DOWN_BOUND - Living.UP_BOUND
    perimeter = (y_length)*2 + \
                (x_length)*2
    #Get a random point on the perimeter
    if cls.use_random:
      current_pos = random.randrange(perimeter)
    else:
      current_pos = 0
    for i in range(amount):
      x_pos = 0
      y_pos = 0
      wall_id = 0
      if current_pos < x_length:
        wall_id = 0
        x_pos = current_pos + cls.surf_perm/4
        y_pos = Living.UP_BOUND
      elif current_pos < x_length+y_length:
        wall_id = 1
        x_pos = Living.RIGHT_BOUND - cls.surf_perm/4
        y_pos = current_pos-x_length
      elif current_pos < x_length*2+y_length:
        wall_id = 2
        x_pos = 2*x_length + y_length - current_pos + cls.surf_perm/4
        y_pos = Living.DOWN_BOUND - cls.surf_perm/4
      else:
        wall_id = 3
        x_pos = Living.LEFT_BOUND
        y_pos = 2*x_length + 2*y_length - current_pos
      entities.append(cls(x_pos, y_pos, wall_id = wall_id))
      #Add an even amount to the perimeter each time and wrap it
      current_pos = (current_pos + perimeter/float(amount)) % perimeter
    return entities