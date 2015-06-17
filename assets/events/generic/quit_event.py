#!/usr/bin/env python

import sys

from event_handler import EventHandler

class QuitEvent(EventHandler):
  def catch_event(self, event_name, event_dict):
    #Quit event or escape key pressed
    return (event_name == "Quit") or \
           (event_name == "KeyDown" and event_dict["key"] == 27)

  def call_event(self, pygame):
    pygame.quit()
    sys.exit()
