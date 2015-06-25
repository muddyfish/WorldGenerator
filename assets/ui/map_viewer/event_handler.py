#!/usr/bin/env python

from assets.events.event_handler import EventHandler

class KeyboardHandler(EventHandler):
  def __init__(self, subscriber):
    self.subscriber = subscriber
    self.pygame = self.subscriber.get_pygame()
    config_manager = self.subscriber.get_main().config_manager
    self.event_map = {}
    for k, v in config_manager["key_config"].iteritems():
      self.event_map[v] = self.event_map.get(v, [])
      self.event_map[v].append(k)
    
  def catch_event(self, event_name, event_dict):
    if event_name == "KeyDown":
      key_name = self.pygame.key.name(event_dict["key"])
      if key_name in self.event_map:
        return True

  def call_event(self, event):
    self.subscriber.call_key_event(self.event_map[self.pygame.key.name(event.dict["key"])])
  