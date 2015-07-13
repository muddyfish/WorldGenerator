#!/usr/bin/env python

import tile

class Corridor(tile.Tile):
    def __str__(self):
        return "C"
    
    def collides(self, entity):
        return False
    
