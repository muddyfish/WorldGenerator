#!/usr/bin/env python

class ExtendableMap(object):
    def __init__(self, centre):
        self.map = [[centre]]
        self.get_map_size()
    
    def __str__(self):
        s = ""
        for row in self.map:
            for col in row:
                if col == None: s+=" "
                elif hasattr(col, "name"): s+=col.name[0]
                else: s+=str(col)[0]
            s+="\n"
        return s[:-1]
    
    def get_map_size(self):
        self.map_size = (len(self.map)-1, len(self.map[0])-1)
    
    def find_obj(self, obj):
        for i, row in enumerate(self.map):
            if obj in row: return [i, row.index(obj)]
            
    def remove_obj(self, obj):
        pos = self.find_obj(obj)
        if pos is not None:
            self.map[pos[0]][pos[1]] = None
    
    def append(self, comp, obj, dir):
        assert(dir in "NESW")
        pos = self.find_obj(comp)
        if   dir == "N": pos[0]-=1
        elif dir == "E": pos[1]+=1
        elif dir == "S": pos[0]+=1
        elif dir == "W": pos[1]-=1
        if pos[0] == -1:
            self.map.insert(0, [None for i in range(self.map_size[1]+1)])
            self.map[0][pos[1]] = obj
        elif pos[1] == -1:
            for row in self.map: row.insert(0, None)
            self.map[pos[0]][0] = obj
        elif pos[0] > self.map_size[0]:
            self.map.append([None for i in range(self.map_size[1]+1)])
            self.map[-1][pos[1]] = obj
        elif pos[1] > self.map_size[1]:
            for row in self.map: row.append(None)
            self.map[pos[0]][-1] = obj
        else:
            if self.map[pos[0]][pos[1]] is not None: return pos
            self.map[pos[0]][pos[1]] = obj
        self.get_map_size()
        assert(self.find_obj(obj))
        return True
    
    def autocrop(self):
        self._autocrop_dim()
        self.map = zip(*self.map) # Rotate the map
        self._autocrop_dim()
        self.get_map_size()
        
    def _autocrop_dim(self):
        j = len(self.map)
        for val in [len(filter(None, i))==0 for i in self.map][::-1]:
            j-=1
            if val: del self.map[j]
    
if __name__ == '__main__':
    m = ExtendableMap(0)
    m.append(0, 1, "E")
    m.append(1, 2, "N")
    m.append(0, 3, "W")
    m.append(0, 4, "S")
    m.append(3, 5, "N")
    print m