#!/usr/bin/env python

import random
from coord import Coord
from constants import *

class Corridor(object):
    def __init__(self, tilearray, start_room, end_room):
        self.tilearray = tilearray
        self.tile_manager = self.tilearray.tile_manager
        self.map = self.tilearray.map
        self.start_room = start_room
        self.end_room = end_room
        raw_spaces = self.get_corridor() # Find the actual corridor spaces
        corridor_space = []
        for space in raw_spaces: # Setup for door sweeper
            if self.map[space.y][space.x].collides:
                self.tilearray.set_space(space, self.tile_manager.space)
        for space in raw_spaces:
            if self.door_allowed(space): 
                corridor_space.append(space)
                #self.set_space(space, 3)
        #print len(corridor_space)
        #if random.randrange(DOOR_CHANCE) == 0:
        #    self.tilearray.set_space(random.choice(corridor_space), DOOR)
        self.corridor_space = corridor_space
    
    def get_corridor(self):
        #Find the start and end of the corridor
        start = Coord(0,0) # Setup start
        end = Coord(0,0) # Setup end
        while self.map[start.y][start.x].collides:
            start = self.start_room.get_random_point() # Find a random spot in the start room
        while self.map[end.y][end.x].collides:
            end = self.end_room.get_random_point() # Find a random spot in the end room        

        door_spaces = []
        corridor = []
        #Add the corridor in order it appears
        #print start.x, end.x, start.y, end.y
        if start.x!=end.x: #Catch range errors if starts and ends on same X
            for i in range(start.x, end.x, cmp(end.x, start.x)): # CMP to count in the right direction
                corridor.append(Coord(i, start.y))
        if start.y!=end.y:
            for j in range(start.y, end.y, cmp(end.y, start.y)):
                corridor.append(Coord(end.x, j))
        start_pos = 0 # Setup
        for current_pos, space in enumerate(corridor): 
            #print "SET", self.tilearray.get_neswc(space)
            if set(self.tilearray.get_neswc(space))!={True}: # If touching a not wall
                if space.get_room_pos() == start.get_room_pos():
                    start_pos = current_pos # Start the corridor here
                else:
                    return corridor[start_pos:current_pos+1]
        #print "END", start_pos
        return corridor[start_pos:] # End the corridor at the end
               
    def door_allowed(self, space):
        n,e,s,w,c = map(self.tilearray.is_wall, self.tilearray.get_neswc(space))
        return (n&s and not(e|w)) or (e&w and not(n|s))
