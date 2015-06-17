#!/usr/bin/env python

class EventHandler(object):
  """A base event handler that can handle a
  event that is passed to it"""
  def __init__(self):
    pass
    
  def catch_event(self, event_name, event_dict):
    """Given the event name and data, does
    this handler want to look at the event"""
    return True

  def call_event(self, event):
    """Called when an event is parsed and
    the catch event function returns True.
    The event manager will attempt to find
    any additional arguments passed to this
    function."""
    raise NotImplementedError()
  
  def get_scopes(self):
    """Returns a list containing dictionary
    like objects that contain any variables
    which are expected for 'call event"""
    return []