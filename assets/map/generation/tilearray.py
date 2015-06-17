#!/usr/bin/env python

import random, sys
seed = random.randint(0, sys.maxint)
random.seed(seed)
#print "RANDOM SEED:", seed
#random.seed(368637554)
CELL_X = 23
CELL_Y = 23
ROOM_OFFSET = 2
ROOM_BOUND_RECT = 2
MAX_ROOM_X = 18
MAX_ROOM_Y = 18
MIN_ROOM_X = 15 # Cant be less than 2*ROOM_BOUND_RECT
MIN_ROOM_Y = 15
POINTS_PER_RECT = 3
DOOR_CHANCE = 1
SPACE = 0
WALL = 1
DOOR = 2
CORRIDOR = 3


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
        return (self.x-1)/(CELL_X+ROOM_OFFSET), \
               (self.y-1)/(CELL_Y+ROOM_OFFSET)
        

class BBox(object):
    """A basic bounding box"""
    def __init__(self, offsets):
        self.offsets = offsets
        
    def __str__(self):
        return str(self.offsets)

class TileArray(object):
    """The map of the dungeon tiles. Takes a dungeon map style ExtendableMap,
    Spits out a full map of rooms with attached corridors"""
    def __init__(self, input_array):
        self.map = [[WALL for i in range(len(input_array[0])*(CELL_X+ROOM_OFFSET)+1)]
            for j in range(len(input_array)*(CELL_Y+ROOM_OFFSET)+1)]
        self.input_array = input_array
        self.add_rooms()
        self.add_corridors()
                    
    def __str__(self):
        "A visual representation of the map"
        chars = {SPACE: " ", WALL: "#", DOOR: "D", CORRIDOR: "C"}
        out = ""
        for row in self.map:
            out += "".join([chars[i] for i in row])+"\n"
        return out    
    
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
                    
    def set_space(self, space, value):
        self.map[space.y][space.x] = value
        
    def get_nesw_dir(self, x,y):
        return ((y-1,x), (y+1,x), (y,x-1), (y,x+1))
        
    def get_neswc(self, space):
        x,y = space.get_pos()
        n = self.map[y-1][x]
        s = self.map[y+1][x]
        w = self.map[y][x-1]
        e = self.map[y][x+1]
        c = self.map[y][x]
        return n,e,s,w,c
        
    def is_wall(self, value):
        return value == WALL
    
    def get_room(self, room_pos):
        return filter(lambda node: node.room.x==room_pos[0] and node.room.y==room_pos[1], self.rooms)[0]
    
    
class Room(object):
    def __init__(self, tilearray, x, y):
        self.tilearray = tilearray
        self.map = self.tilearray.map
        self.x = x
        self.y = y
        x_pos = x*(CELL_X+ROOM_OFFSET)+ROOM_BOUND_RECT
        y_pos = y*(CELL_Y+ROOM_OFFSET)+ROOM_BOUND_RECT
        room_size = [random.randint(MIN_ROOM_X, MAX_ROOM_X),
                     random.randint(MIN_ROOM_Y, MAX_ROOM_Y)]
        self.offsets = [x_pos+random.randrange(CELL_X-room_size[0]-ROOM_BOUND_RECT),
                        y_pos+random.randrange(CELL_Y-room_size[1]-ROOM_BOUND_RECT)]
        self.offsets.insert(1, self.offsets[0]+room_size[0])
        self.offsets.insert(4, self.offsets[2]+room_size[1])
        self.clear_space()

    def clear_space(self):
        upper_rect = (self.offsets[0]+3, self.offsets[1]-3), (self.offsets[2],   self.offsets[2]+2)
        lower_rect = (self.offsets[0]+3, self.offsets[1]-3), (self.offsets[3]-2, self.offsets[3])
        left_rect =  (self.offsets[0],   self.offsets[0]+2), (self.offsets[2]+3, self.offsets[3]-3)
        right_rect = (self.offsets[1]-2, self.offsets[1]),   (self.offsets[2]+3, self.offsets[3]-3)
        rects = [upper_rect, right_rect, lower_rect, left_rect]
        points = []
        for num, rect in enumerate(rects):
            rect_points = []
            for i in range(POINTS_PER_RECT):
                rect_points.append((random.randint(*rect[0]), random.randint(*rect[1])))
            rect_points.sort(key=lambda x: x[num%2], reverse = bool(num/2))
            points.extend(rect_points)
        for i in range(len(points)):
            self.line((points[i-1], points[i]))
        self.floodfill(((self.offsets[0]+self.offsets[1])/2, (self.offsets[2]+self.offsets[3])/2))
        
    def line(self, points):
        "Bresenham's line algorithm"
        (x0,y0), (x1,y1) = points
        dx = abs(x1 - x0)
        dy = abs(y1 - y0)
        x, y = x0, y0
        sx = -1 if x0 > x1 else 1
        sy = -1 if y0 > y1 else 1
        if dx > dy:
            err = dx / 2.0
            while x != x1:
                self.map[y][x] = SPACE
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                self.map[y][x] = SPACE
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy        
        self.map[y][x] = SPACE
        
    def floodfill(self, pos):
        if not self.map[pos[1]][pos[0]]:
            return
        self.map[pos[1]][pos[0]] = SPACE
        for x in [-1,1]:
            self.floodfill((pos[0], pos[1]+x))
        for y in [-1,1]:
            self.floodfill((pos[0]+y, pos[1]))
    
    def get_random_point(self):
        return Coord(
                random.randrange(self.offsets[0]+1,self.offsets[1]),
                random.randrange(self.offsets[2]+1,self.offsets[3]))
   
    def get_pos(self):
        return Coord(self.x, self.y)
    
class Corridor(object):
    def __init__(self, tilearray, start_room, end_room):
        self.tilearray = tilearray
        self.map = self.tilearray.map
        self.start_room = start_room
        self.end_room = end_room
        raw_spaces = self.get_corridor() # Find the actual corridor spaces
        corridor_space = []
        for space in raw_spaces: # Setup for door sweeper
            if self.map[space.y][space.x] == 1:
                self.tilearray.set_space(space, SPACE)
        for space in raw_spaces:
            if self.door_allowed(space): 
                corridor_space.append(space)
                #self.set_space(space, 3)
        #print len(corridor_space)
        if random.randrange(DOOR_CHANCE) == 0:
            self.tilearray.set_space(random.choice(corridor_space), DOOR)
        self.corridor_space = corridor_space
    
    def get_corridor(self):
        #Find the start and end of the corridor
        start = Coord(0,0) # Setup start
        end = Coord(0,0) # Setup end
        while self.map[start.y][start.x] != SPACE:
            start = self.start_room.get_random_point() # Find a random spot in the start room
        while self.map[end.y][end.x] != SPACE:
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
            #assert(self.tilearray.get_room(space.get_room_pos()) in [start_room, end_room])
            if set(self.tilearray.get_neswc(space))!={WALL}: # If touching a not wall
                if space.get_room_pos() == start.get_room_pos():
                    start_pos = current_pos # Start the corridor here
                else:
                    return corridor[start_pos:current_pos+1]
        #print "END", start_pos
        return corridor[start_pos:] # End the corridor at the end
               
    def door_allowed(self, space):
        n,e,s,w,c = map(self.tilearray.is_wall, self.tilearray.get_neswc(space))
        return (n&s and not(e|w)) or (e&w and not(n|s))
     
    
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