#!/usr/bin/env python

from ..manager_base import ManagerBase

class KeyboardInjector(ManagerBase):
    def run(self):
        pygame = self.get_pygame()
        for key, state in enumerate(pygame.key.get_pressed()):
            if state:
                pygame.event.post(pygame.event.Event(2, {
                    "unicode": "",
                    "key": key,
                    "mod": 0}))