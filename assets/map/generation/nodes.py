import json
import random

def id_generator():
    i = 0
    while 1:
        yield i
        i+=1

class Node(object):
    def __init__(self):
        self.connections = []
        self.id = id_gen.next()
        self.transversed = False
        self.seed = random.random()
        self.locked = self.name.startswith("Lock")
        
    def __str__(self):
        return "%s (%s): %s"%(self.id, self.name, [conn.id for conn in self.connections])

    def connect(self, node):
        if node not in self.connections:
            self.connections.append(node)
        if self not in node.connections:
            node.connections.append(self)

    def disconnect(self, node):
        self.connections.remove(node)
        node.connections.remove(self)

    def get_connected(self, connected = []):
        connected = connected[:]
        connected.append(self)
        for conn in self.connections:
            if conn not in connected:
                connected = conn.get_connected(connected)
        return connected

    def untransverse(self):
        self.transversed = False
        for conn in self.connections:
            if conn.transversed: conn.untransverse()
    
    def kill_conns(self):
        for conn in self.connections[:]:
            self.disconnect(conn)
            conn.kill_conns()

def print_nodes(nodelist):
    for node in nodelist: print node

try: id_gen
except NameError: id_gen = id_generator()

def load_nodes(nodes_json):
    nodetypes = {}
    for nodetype in nodes_json:
        nodes_json[nodetype]["name"] = nodetype
        nodetypes[nodetype] = type(str(nodetype), (Node,), nodes_json[nodetype])
    globals()["nodetypes"] = nodetypes

if __name__ == "__main__":
    nodes = [nodetypes["Chain"]() for i in range(4)]
    nodes[1].connect(nodes[2])
    print nodes[1].name
