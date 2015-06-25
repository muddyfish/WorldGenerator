#!/usr/bin/env python

import os, imp, pkgutil
from ..manager_base import ManagerBase
import ui

class SubscriptionManager(ManagerBase):
  def __init__(self):
    self.subscription_path = os.path.dirname(os.path.abspath(__file__))
    self.subscription_folders = [dir for dir in os.listdir(self.subscription_path) if os.path.isdir(os.path.join(self.subscription_path,dir))]
    self.subscriptions = dict(map(self.load_subscription_folder, self.subscription_folders))
    self.current_subscription_id = self.get_default_subscription_id()
    self.current_subscription = self.subscriptions[self.current_subscription_id]()
    
  def get_default_subscription_id(self):
    return self.get_config_manager()["subscription_config", "default"]
  
  def run_subscription(self):
    self.current_subscription.run()
    self.current_subscription.draw()
  
  def load_subscription_folder(self, subscription):
    __import__("assets.ui.%s"%subscription)
    path_var = "assets.ui.%s.main"%subscription
    file_path = os.path.join(self.subscription_path, subscription, "main.py")
    main_module = imp.load_source(path_var, file_path)
    
    for c in main_module.__dict__.values():
      try:
        if issubclass(c, ui.UI) and c is not ui.UI:
          return subscription, c
      except TypeError: pass