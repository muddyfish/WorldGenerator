#!/usr/bin/env python

import glob
import json
import os
from ..manager_base import ManagerBase


class ConfigManager(ManagerBase):
  def __init__(self):
    self.config_location = os.path.dirname(os.path.abspath(__file__))
    self.config_files = glob.glob(self.get_path(self.config_location, "*.json"))
    self.config_data = {}
    for config_path in self.config_files:
      config = self.parse_config_file(config_path)
      self.config_data[config[0]] = config[1]
  
  def __getitem__(self, path):
    if not isinstance(path, tuple):
      path = (path,)
    data = self.config_data
    for index in path:
      data = data[index]
    return data

  def parse_config_file(self, config_path):
    config_file = open(config_path)
    contents = json.load(config_file)
    config_file.close()
    return os.path.basename(config_path)[:-5], contents
  
  def parse_path(self, path):
    return os.path.join(os.getcwd(), *path.split("."))
  
  def get_path(self, directory, filename):
    return os.path.join(directory, filename)
  
  def get_screen_properties(self):
    props = self["video_config", "screen_properties"]
    return props["size"], props["fullscreen"]