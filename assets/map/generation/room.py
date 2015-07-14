#!/usr/bin/env python

import random
from coord import Coord

class Room(object):
    def __init__(self, tilearray, x, y):
        self.tilearray = tilearray
        self.config = self.tilearray.config
        self.tile_manager = self.tilearray.tile_manager
        self.map = self.tilearray.map
        self.x = x
        self.y = y
        x_pos = x*(self.config["cell_x"]+self.config["room_offset"])+self.config["room_bound_rect"]
        y_pos = y*(self.config["cell_y"]+self.config["room_offset"])+self.config["room_bound_rect"]
        room_size = [random.randint(self.config["min_room_x"], self.config["max_room_x"]),
                     random.randint(self.config["min_room_y"], self.config["max_room_y"])]
        self.offsets = [x_pos+random.randrange(self.config["cell_x"]-room_size[0]-self.config["room_bound_rect"]),
                        y_pos+random.randrange(self.config["cell_y"]-room_size[1]-self.config["room_bound_rect"])]
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
            for i in range(self.config["points_per_rect"]):
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
                self.map[y][x] = self.tile_manager.space
                err -= dy
                if err < 0:
                    y += sy
                    err += dx
                x += sx
        else:
            err = dy / 2.0
            while y != y1:
                self.map[y][x] = self.tile_manager.space
                err -= dx
                if err < 0:
                    x += sx
                    err += dy
                y += sy        
        self.map[y][x] = self.tile_manager.space
        
    def floodfill(self, pos):
        if not self.map[pos[1]][pos[0]].collides:
            return
        self.map[pos[1]][pos[0]] = self.tile_manager.space
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
    