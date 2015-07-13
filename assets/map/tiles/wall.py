#!/usr/bin/env python
import tile

class Wall(tile.Tile):
    def __str__(self):
        return "#"