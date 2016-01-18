#!/usr/bin/env python

import os, sys, inspect
import __main__

class Entity(__main__.pygame.sprite.Sprite):
  persistant = False
  no_spawn = False
  no_respawn = False
  update_bounding_box = True
  spawned = False
  must_kill = False
  
  def __init__(self, x,y):
    super(Entity, self).__init__()
    self.mro_groups = [cls.__name__.lower() for cls in inspect.getmro(self.__class__)[:-2]]
    self.dirty = True
    self.ai_events = []
    self.groups = []
    if not hasattr(self, "surf"):
      self.surf = self.load_surf(self.get_pygame().surface.Surface((32,32)))
    self.x = x
    self.y = y
    self.update_collision()
  
  def __repr__(self):
    return "%s(%d,%d)"%(self.__class__.__name__, self.x, self.y)
  
  def spawn(self):
    self.spawned = True
    if self.no_spawn: return
    #Add this entity to it's parents groups
    self.groups = self.mro_groups[:]
    for group in self.groups:
      attr = getattr(self.get_entity_data(), group)
      #If any of this entities parents haven't been added before, add them to to the databin
      if isinstance(attr, self.get_main().databin.__class__):
        attr = self.get_pygame().sprite.LayeredUpdates()
        setattr(self.get_entity_data(), group, attr)
      attr.add(self)
  
  def despawn(self, killed = True):
    self.spawned = False
    self.groups = []
    if self.no_respawn and killed: self.no_spawn = True
    self.kill()
  
  def register_event(self, event, *args, **kwargs):
    handler = getattr(self.get_databin().ai_events, event)
    self.ai_events.append(handler.add_listener(*([self]+list(args)), **kwargs))
  
  def run(self, d_time):
    self.update_collision()
  
  def center(self, x_pos = None, y_pos = None):
    if None==x_pos==y_pos:
      x_pos,y_pos = self.screen.get_center()
    self.x = x_pos-self.surf.get_width()/4
    self.y = y_pos-self.surf.get_height()/4
  
  def get_pygame(self):
    return __main__.pygame
  
  def get_main(self):
    return __main__.main_class

  def get_databin(self):
    return self.get_main().databin
  
  def get_subscription(self):
    return self.get_databin().current_subscription
  
  def get_entity_data(self):
    return self.get_databin().entity_data
  
  def get_player(self):
    return self.get_entity_data().player.sprites()[0]
  
  def touching_player(self):
    return self.get_collide([self.get_player()])
  
  def get_blit(self):
    return self.get_subscription().get_blit(self.dirty)
  
  def load_surf(self, surf):
    if self.update_bounding_box:
      self.bounding_rect = surf.get_bounding_rect()
      self.rect = self.bounding_rect
    try:
      self.update_collision()
    except AttributeError:
      pass
    return surf
  
  def get_path(self, dirname = None):
    return os.path.join(*[os.path.dirname(__main__.__file__)]+self.__class__.__module__.split(".")[:-1])+os.sep
  
  def blit(self, x_mod=0, y_mod=0):
    self.get_blit()(self.surf, (self.x+x_mod, self.y+y_mod))
    
  def update_collision(self):
    self.rect.x = self.x + self.bounding_rect.x/2
    self.rect.y = self.y + self.bounding_rect.y/2
    self.rect.size = self.bounding_rect.size
    self.rect.width/=2
    self.rect.height/=2

  def get_collide(self, entities = None):
    if entities == None: entities = self.get_entity_data().entity
    collide = self.get_pygame().sprite.spritecollide(self, entities, False)
    try:
      collide.remove(self)
    except ValueError: pass
    return collide
  
  def spawn_entity(self, entity_name, *args, **kwargs):
    entity = self.get_main().entity_manager.entities[entity_name](*args, **kwargs)
    entity.spawn()
    return entity

  @staticmethod
  def memoize(func):
    def mem_func(*args, **kwargs):
      memory_name = func.__name__ + "_memory"
      if memory_name not in globals():
        globals()[memory_name] = {}
      h = hash((args, frozenset(kwargs.items())))
      if h not in globals()[memory_name]:
        globals()[memory_name][h] = func(*args, **kwargs)
        print "not remembered!", len(globals()[memory_name])
      else:
        print "remembered"
      return globals()[memory_name][h]
    return mem_func
  



