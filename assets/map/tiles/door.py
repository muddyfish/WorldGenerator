#!/usr/bin/env python

import tile

class Door(tile.Tile):
    def __init__(self):
        super(Door.__init__, self)
        self.open = False
    
    def __str__(self):
        return "D"
    
    
    def collides(self, entity):
        return not self.open
    
    def interact(self, entity):
        self.open = not self.open
    
    
