#!/usr/bin/env python

import glob, os, imp
import ai_event_handler
from ..manager_base import ManagerBase

class AiEventManager(ManagerBase):
  def __init__(self):
    self.ai_events = []
    
  def add_events(self):
    event_path = os.path.dirname(os.path.abspath(__file__))
    ai_events = glob.glob(os.path.join(event_path, "ai_events", "*.py"))
    ai_event_names = ["assets.events.event_ai_%s"%os.path.basename(event_file)[:-3] for event_file in ai_events]
    self.ai_events.extend(map(self.load_event_file, ai_events, ai_event_names))
    events_dict = {event.__class__.__name__:event for event in self.ai_events if event}
    for name, event in events_dict.iteritems():
      setattr(self.get_databin().ai_events, name, event)

  def load_event_file(self, event_file, event_name):
    event_handler = imp.load_source(event_name, event_file)
    for c in event_handler.__dict__.values():
      try:
        if issubclass(c, ai_event_handler.AiEventHandler) and c is not ai_event_handler.AiEventHandler:
          return c()
      except TypeError: pass
