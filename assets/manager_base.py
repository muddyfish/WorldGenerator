#!/usr/bin/envpython

import __main__

class ManagerBase(object):
    def get_main_class(self):
        return __main__.main_class
    
    def get_pygame(self):
        return __main__.pygame
    
    def get_main_dict(self):
        return __main__.__dict__
    
    def get_config_manager(self):
        return self.get_main_class().config_manager