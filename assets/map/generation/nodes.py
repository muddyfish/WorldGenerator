import json, random
import __main__

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
        self.cleared = False
        self.entity_list = []
        if hasattr(self, "entities"):
            self.entity_list = self.get_entities()
        
    def __str__(self):
        return "%s (%s): %s"%(self.id, self.name, ", ".join(["(%d: %s)"%(conn.id, conn.name) for conn in self.connections]))

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

    def get_entities(self):
        entities = []
        seed = random.random()
        # Get the probability for a group to spawn
        chances = [group[0]for group in self.entities]
        # Which groups have a toatl probability above the seed chosen?
        groups = [sum(chances[:i+1]) > seed for i in range(len(chances))]
        # If none, no entities
        if groups == []: return []
        # The group chosen is the one with the lowest total chance that got chosen
        group_id = groups.index(True)
        for entity, amount in self.entities[group_id][1].iteritems():
            cls = __main__.main_class.entity_manager.entities[entity]
            try:
                entities.extend(cls.spawn_group(amount))    
            except AttributeError:
                for i in range(amount):
                    entities.append(cls())
        return entities

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
