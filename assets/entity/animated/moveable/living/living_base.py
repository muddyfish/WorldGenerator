#!/usr/bin/env python
from ..moveable_base import Moveable
import random, math, __main__

class Living(Moveable):
  max_life = 16
  min_life = 16
  vulnerable = []
  ineffective = []
  immune = []
  no_respawn = False
  
  def __init__(self, x,y):
    super(Living, self).__init__(x,y)
    self.life = random.randrange(self.min_life, self.max_life+1)  
  
  @classmethod
  def spawn_group(cls, amount):
    return cls.spawn_method()(amount)
    
  @classmethod
  def circular(cls, amount):
    entities = []
    screen = __main__.main_class.screen
    center = [screen.get_width()/4, screen.get_height()/4]
    for i in range(amount):
      x = cls.circle_radius * math.sin((2*math.pi*i)/amount)
      y = cls.circle_radius * math.cos((2*math.pi*i)/amount)
      entities.append(cls(center[0]+x,center[1]+y))
    return entities