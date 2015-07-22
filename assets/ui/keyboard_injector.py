#!/usr/bin/env python

from ..manager_base import ManagerBase
from itertools import compress

class KeyboardInjector(ManagerBase):
    def __init__(self):
        self.key_range = range(323)
        
    def run(self):
        pygame = self.get_pygame()
        for key in compress(self.key_range, pygame.key.get_pressed()):
            pygame.event.post(pygame.event.Event(pygame.KEYDOWN, {
               "unicode": "",
               "key": key,
               "mod": 0}))