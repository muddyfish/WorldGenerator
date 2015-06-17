import json

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
        self.bbox = []

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

nodes_file = open("nodes.json")
nodetype_data = json.load(nodes_file)
nodes_file.close()
nodetypes = {}
for nodetype in nodetype_data:
    nodetype_data[nodetype]["name"] = nodetype
    nodetypes[nodetype] = type(str(nodetype), (Node,), nodetype_data[nodetype])


if __name__ == "__main__":
    nodes = [nodetypes["Chain"]() for i in range(4)]
    nodes[1].connect(nodes[2])
    print nodes[1].name
