#!/usr/bin/env python

class Coord(object):
    """A coordinate that has methods to get and set it's position,
    work out equality with other types of coordinate and get the
    room the coordinate is in"""
    def __init__(self, x,y):
        self.set_pos(x,y)
        
    def __str__(self):
        return "Coord (%i, %i)"%(self.x, self.y)

    def __eq__(self, coord):
        if isinstance(coord, Coord):
            return self.get_pos()==coord.get_pos()
        elif type(coord) is tuple:
            return tuple(self.get_pos()) == coord
        elif type(coord) is list:
            return self.get_pos() == coord
        return False

    def set_pos(self, x,y):
        self.x = x
        self.y = y
    
    def get_pos(self):
        return self.x, self.y
    
    def get_room_pos(self):
        return (self.x-1)/(self.CELL_X+self.ROOM_OFFSET), \
               (self.y-1)/(self.CELL_Y+self.ROOM_OFFSET)
