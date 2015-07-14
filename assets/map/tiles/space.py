#!/usr/bin/env python

import tile

class Space(tile.Tile):
    def __str__(self):
        return " "
    
    def collides(self, entity = None):
        return False
    
    