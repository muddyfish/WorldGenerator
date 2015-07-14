#!/usr/bin/env python

class Tile(object):
    def __init__(self):
        self.move_speed = 1.0
    
    def __str__(self):
        return "?"
    
    def __getattribute__(self, attr):
        if attr == "collides":
            return object.__getattribute__(self, attr)(self)
        return object.__getattribute__(self, attr)
    
    
    def collides(self, entity = None):
        return True

    def interact(self, entity):
        pass