#!/usr/bin/env python

import random
from coord import Coord
from constants import *

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
    