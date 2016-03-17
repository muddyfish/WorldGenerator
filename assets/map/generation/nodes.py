import json, random
import __main__

def id_generator():
    i = 0
    while 1:
        yield i
        i+=1

class Node(object):
    def __init__(self, seed = None):
        if seed is None:
            self.seed = random.random()
        else:
            self.seed = seed
        self.connections = []
        self.id = id_gen.next()
        self.transversed = False
        self.cleared = False
        self.been_visited = False
        self.entity_list = []
        
    def __str__(self):
        return "%s (%s): %s"%(self.id, self.name, ", ".join(["(%d: %s)"%(conn.id, conn.name) for conn in self.connections]))

    def visited(self, replaced = False):
        if self.been_visited: return
        self.been_visited = True
        self.entity_list.extend(self.get_entities(replaced))

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

    def get_entities(self, replaced = False):
        entities = []
        seed = random.random()
        entity_list = {}
        if hasattr(self, "entities"):
            entity_list.update(self.get_entity_list(replaced, seed))
        if self.has_monsters:
            entity_list.update(self.get_monster_list(seed))
        print entity_list
        for entity, amount in entity_list.iteritems():
            ent_cls = __main__.main_class.entity_manager.entities[entity]
            if hasattr(ent_cls, "spawn_group"):
                entities.extend(ent_cls.spawn_group(amount))    
            else:
                for i in range(amount):
                    entities.append(ent_cls())
        return entities
    
    def get_entity_list(self, replaced, seed):
        entity_list = {}
        cls_entities = self.entities
        if issubclass(cls_entities.__class__, basestring):
            return nodetypes[self.entities].get_entities()
        # Get the probability for a group to spawn
        if replaced and hasattr(self, "replaced_entities"):
            cls_entities = self.replaced_entities
        chances = [group[0]for group in cls_entities]
        # Which groups have a toatl probability above the seed chosen?
        groups = [sum(chances[:i+1]) > seed for i in range(len(chances))]
        # If none, no entities
        if groups != []:
            # The group chosen is the one with the lowest total chance that got chosen
            group_id = groups.index(True)
            entity_list = cls_entities[group_id][1]
        return entity_list

    def get_monster_list(self, seed):
        entity_list = {}
        max_entities = 7
        entities = __main__.main_class.entity_manager.entities
        possible_entities = []
        for name, entity in entities.iteritems():
            if hasattr(entity, "difficulty") and entity.difficulty != 0:
                possible_entities.append([entity.difficulty, name])
        print possible_entities
        entity_list["animated.moveable.living.npc.hostile.charger.snake"] = int(self.difficulty**(1/2.))
        #entity_list["animated.moveable.living.npc.neutral.spike_trap.wallhugger"] = 10
        #entity_list["animated.moveable.living.npc.neutral.spike_trap.spinner"] = 1
        print entity_list
        return entity_list
        
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
