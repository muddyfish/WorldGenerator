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
  
  def __init__(self, x,y):
    super(Living, self).__init__(x,y)
    self.life = random.randrange(self.min_life, self.max_life+1)  
  
  @classmethod
  def spawn_group(cls, amount):
    return cls.spawn_method()(amount)
    
  @classmethod
  def spawn_circular(cls, amount):
    entities = []
    screen = __main__.main_class.screen
    center = [screen.get_width()/4, screen.get_height()/4]
    for i in range(amount):
      x = cls.circle_radius * math.sin((2*math.pi*i)/amount)
      y = cls.circle_radius * math.cos((2*math.pi*i)/amount)
      entities.append(cls(center[0]+x,center[1]+y))
    return entities
  
  @classmethod
  def spawn_wall(cls, amount):
    entities = []
    x_length = Living.RIGHT_BOUND - Living.LEFT_BOUND# - cls.surf_perm/2
    y_length = Living.DOWN_BOUND - Living.UP_BOUND #- cls.surf_perm/2
    perimeter = (y_length)*2 + \
                (x_length)*2
    #Get a random point on the perimeter
    current_pos = 0#random.randrange(perimeter)
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