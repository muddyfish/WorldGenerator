#!/usr/bin/env python

import glob, os, imp
import event_handler
import __main__

class EventManager(object):
  """A basic event manager that can have
  generic and subscription based event
  handlers. The manager will also attempt to
  automatically find arguments for the call
  event for every handler"""
  def __init__(self):
    self.subscription_events = {}
    self.generic_events = []
    self.subscriber = ""
    
  def add_events(self):
    event_path = os.path.dirname(os.path.abspath(__file__))
    generic_events = glob.glob(os.path.join(event_path, "generic", "*_event.py"))
    generic_event_names = ["assets.events.event_generic_%s"%os.path.basename(event_file)[:-3] for event_file in generic_events]
    self.generic_events.extend(map(self.load_event_file, generic_events, generic_event_names))
    for subscription_id in os.listdir(os.path.join(event_path, "subscription")):
      self.subscription_events[subscription_id] = []
      subscription_events = glob.glob(os.path.join(event_path, "subscription", subscription_id, "*_event.py"))
      for event in subscription_events:
        event_name = "assets.events.event_subscription_%s_%s"%(subscription_id, os.path.basename(event_file)[:-3])
        self.subscription_events[subscription_id].append(self.load_event_file(event, event_name))

  def load_event_file(self, event_file, event_name):
    event_handler = imp.load_source(event_name, event_file)
    for c in event_handler.__dict__.values():
      try:
        if issubclass(c, event_handler.EventHandler) and c is not event_handler.EventHandler:
          return c()
      except TypeError: pass

  def parse_events(self, events):
    """Given a list of events, call the
    current subscription handler as well as
    the generic handler for each event"""
    for event in events:
      self.handle_event_list(event, self.generic_events)
      if self.subscriber in self.subscription_events:
        self.handle_event_list(event, self.subscription_events[self.subscriber])
      
  def handle_event_list(self, event, event_handler_list):
    """For each handler in the list, see if
    the handler wishes to be called and if
    so, call it"""
    for handler in event_handler_list:
      if handler.catch_event(self.get_event_name(event), event.dict):
        self.call_event(handler, event)
      
  def get_event_name(self, event):
    """Given an event, find its name"""
    return __main__.pygame.event.event_name(event.type)
    
  def call_event(self, handler, event):
    """Attempt to call an event handler with
    an event."""
    scopes = [locals(),
              __main__.__dict__,
              __main__.main_class.__dict__]
    scopes.extend(handler.get_scopes())
    func = handler.call_event
    var_names = func.func_code.co_varnames[1:func.func_code.co_argcount]
    var_values = []
    for var_name in var_names:
      done = False
      for scope in scopes:
        if var_name in scope and not done:
          done = True
          var_values.append(scope[var_name])
      if not done:
        raise ValueError("Invalid argument name %s for handler function %s."%(var_name, func))
    func(*var_values)