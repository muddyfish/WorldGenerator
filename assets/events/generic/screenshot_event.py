#!/usr/bin/env python

import glob

from event_handler import EventHandler

class ScreenshotEvent(EventHandler):
  def catch_event(self, event_name, event_dict):
    # ` pressed (above tab)
    return event_name == "KeyDown" and event_dict["key"] == 96
    
  def call_event(self, pygame, config_manager, screen):
    print("Taking screenshot")
    screenshot_path = config_manager["path_config", "screenshot_path"]
    screenshot_paths = glob.glob(config_manager.get_path(screenshot_path, "*.png"))
    screenshot_ids = map(lambda path: int(path[:-4].split("_")[-1]), screenshot_paths)
    screenshot_ids.append(0)
    latest_num = max(screenshot_ids)
    pygame.image.save(screen.copy(), config_manager.get_path(screenshot_path, "screenshot_%i.png" %(latest_num+1)))
