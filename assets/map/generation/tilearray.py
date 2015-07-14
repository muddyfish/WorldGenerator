#!/usr/bin/env python

from bounding_box import BBox
from room import Room
from corridor import Corridor
from coord import Coord

class TileArray(object):
    """The map of the dungeon tiles. Takes a dungeon map style ExtendableMap,
    Spits out a full map of rooms with attached corridors"""
    def __init__(self, input_array, config_manager, tile_manager):
        self.config_manager = config_manager
        self.config = self.config_manager["dungeon_map_config"]
        self.tile_manager = tile_manager
        Coord.CELL_X = self.config["cell_x"]
        Coord.CELL_Y = self.config["cell_y"]
        Coord.ROOM_OFFSET = self.config["room_offset"]
        self.map = \
        [[self.tile_manager.wall for i in range(len(input_array[0])*(self.config["cell_x"]+self.config["room_offset"])+1)]
            for j in range(len(input_array)*(self.config["cell_y"]+self.config["room_offset"])+1)]
        self.input_array = input_array
        self.add_rooms()
        self.add_corridors()
        self.smooth()
    
    def __getitem__(self, index):
        if not isinstance(index, tuple):
            index = (index,)
        pos = self.map
        for i in range(len(index)):
            pos = pos[index[i]]
        return pos
    
    def add_rooms(self):
        "Adds every room to the map"
        self.rooms = []
        for y, row in enumerate(self.input_array):
            for x, column in enumerate(row):
                if column is not None:
                    column.room = Room(self, x, y)
                    self.rooms.append(column)

    def add_corridors(self):
        donenodes = []
        self.corridors = []
        for node in self.rooms:
            donenodes.append(node)
            for conn in node.connections:
                if conn not in donenodes:
                    self.corridors.append(Corridor(self, node.room, conn.room))
    
    def smooth(self):
        smoothed = False
        for y in range(len(self.map)):
            for x in range(len(self.map[y])):
                try:
                    n,e,s,w,c = self.get_neswc(Coord(x,y))
                except IndexError: pass
                else:
                    if n+e+s+w == 3-c*2:
                        if c == 1: self.map[y][x] = self.tile_manager.space
                        else: self.map[y][x] = self.tile_manager.wall
                        smoothed = True
        if smoothed: self.smooth()
    
    def set_space(self, space, value):
        self.map[space.y][space.x] = value
        
    def get_nesw_dir(self, x,y):
        return ((y-1,x), (y+1,x), (y,x-1), (y,x+1))
        
    def get_neswc(self, space):
        x,y = space.get_pos()
        n = self.map[y-1][x].collides
        s = self.map[y+1][x].collides
        w = self.map[y][x-1].collides
        e = self.map[y][x+1].collides
        c = self.map[y][x].collides
        return n,e,s,w,c
        
    def is_wall(self, value):
        return value == self.tile_manager.wall
    
    def get_room(self, room_pos):
        return filter(lambda node: node.room.x==room_pos[0] and node.room.y==room_pos[1], self.rooms)[0]
    
if __name__ == '__main__':
    n = None
    f = True
    ta = TileArray([
        [n,f,f,n,f],
        [n,n,f,f,f],
        [n,f,f,n,f],
        [f,f,n,n,f],
        [f,f,n,n,f]])
    print ta