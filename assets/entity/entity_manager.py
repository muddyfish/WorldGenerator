#!/usr/bin/env python

import os, imp, pkgutil
from ..manager_base import ManagerBase
import entity_base
import __main__

class EntityManager(ManagerBase):
  def __init__(self):
    self.entity_path = os.path.dirname(os.path.abspath(__file__))
    self.entities = {}
    for root, dirs, files in os.walk(self.entity_path):
      import_name = os.path.basename(root)+".py"
      if import_name in files:
        k,v = self.load_entity(root, import_name[:-3])
        self.entities[k] = v

  def load_entity(self, path, entity):
    import_path = os.path.relpath(path, os.path.split(__main__.__file__)[0]).replace(os.sep, ".")
    __import__(import_path)
    mod_name = import_path.split(".")[-1]
    path_var = import_path + "." + mod_name
    file_path = os.path.join(*(import_path.split(".")+[mod_name+".py"]))
    main_module = imp.load_source(path_var, file_path)
    for c in main_module.__dict__.values():
      try:
        if issubclass(c, entity_base.Entity) and c.__name__.lower() == mod_name.lower():
          return ".".join(import_path.split(".")[2:]), c
      except TypeError: pass
      
      
      
      
      
      
      