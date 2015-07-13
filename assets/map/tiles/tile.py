#!/usr/bin/env python

class Tile(object):
    def __init__(self):
        self.collides = True
        self.move_speed = 1.0
    
    def __str__(self):
        return "?"
    
    def collides(self, entity):
        return True

    def interact(self, entity):
        pass