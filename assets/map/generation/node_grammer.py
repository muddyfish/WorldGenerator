#!/usr/bin/env python

import json, random
from ..extendable_map import ExtendableMap
import nodes

MAP_DIFFICULTY = 0.25
COMPASS_DIFFICULTY = 0.75

class Nodes(object):
    def __init__(self, chains_json, nodes_json):
        nodes.load_nodes(nodes_json)
        self.chains = []
        for chainlist in chains_json:
            self.chains.extend(chainlist) # Add all chains to the list
        self.keys = [] # A list of every set of replacements
        self.start_keys = [] # A list of every node that can be replaced
        for chain in self.chains:
            self.keys.append([n.split("_") for n in chain.keys()][0]) # Add the correct keys to the list
            self.start_keys.append(self.keys[-1][0]) # Add the start key to the list
        self.start = nodes.nodetypes["Start"]() # The first node

    def save_nodes(self, filename="graph"):
        print "Saving graph..."
        from graphviz import Digraph
        dot = Digraph(comment='Dungeon Example')
        nodes = self.linear_nodes(self.nodes)
        for node in nodes: dot.node(str(node.id), node.name+" "+str(node.id))
        for node in nodes:
            for edge in node.connections:
                dot.edge(str(node.id), str(edge.id))
        dot.render(filename)
        print "Graph saved"
    
    def linear_nodes(self, nodes):
        node_list = []
        for node in nodes:
            if isinstance(node, dict):
                node_list.append(node.keys()[0])
                node_list.extend(self.linear_nodes(node.values()[0]))
            else:
                node_list.append(node)
        return node_list
    
    def prettyprint(self, nodes, indent = 0):
        for node in nodes:
            if isinstance(node, dict):
                print " "*indent+node.keys()[0].name
                self.prettyprint(node.values()[0], indent+2)
            else:
                print " "*indent+node.name
    
    def create_nodes(self, key, modular = False, prev_node = None):
        chain_nodes = []
        if prev_node: # Is key a chain or key?
            chain = key
        else:
            chain = self.chains[random.choice([i for i, val in enumerate(self.keys) if val == key])].values()[0]
        if isinstance(chain, list) and isinstance(chain[0], basestring) and not modular: #Only linear chains
            chain_nodes.append(nodes.nodetypes[chain[0]]())
            for node in chain[1:]:
                chain_nodes.append(nodes.nodetypes[node]())
                chain_nodes[-1].connect(chain_nodes[-2])
            return chain_nodes
        # Only modular chains now
        if not modular: # First time modular
            chain = chain[0]
            prev_node = None
        if isinstance(chain, dict):
            chain_nodes.append(nodes.nodetypes[chain.keys()[0]]())
            if prev_node: chain_nodes[-1].connect(prev_node)
            cur_node = chain_nodes[-1]
            for node in chain.values()[0]:
                if isinstance(node, basestring):        
                    chain_nodes.append(nodes.nodetypes[node]())
                    chain_nodes[-1].connect(cur_node)
                else:
                    self.create_nodes(node, True, cur_node)
        return chain_nodes[0].get_connected()
    
    def create_dungeon(self, start_difficulty):
        self.core_grammer()
        self.entrance = filter(lambda x: x.name == "Entrance", self.nodes)[0]
        self.exit = filter(lambda x: x.name == "BossLevel", self.nodes)[0]
        self.shuffle_nodes([self.entrance])
        self.entrance.untransverse()
        self.nodes = self.absorb_nodes([self.entrance])
        self.entrance.untransverse()
        self.entrance.kill_conns()
        self.connect_nodes(self.nodes)
        self.entrance.difficulty = start_difficulty
        self.add_difficulty(self.entrance)
        self.add_rewards()
        done = False
        repeats = 0
        while (not done) and repeats != 10:
            self.map = ExtendableMap(self.entrance)
            self.add_map(self.entrance)
            count = filter(None, [filter(None, i) for i in self.map.map])
            done = sum([len(i) for i in count]) == self.count_nodes(self.entrance)
            repeats += 1
        if repeats == 10: self.create_dungeon(start_difficulty)
        else:
            self.map.autocrop()
                
    
    def core_grammer(self):
        connections = self.start.get_connected()
        done = True
        while done:
            done = False
            for node in connections:
                if node.name in self.start_keys:
                    done = True
                    valid_keys = [self.keys[i] for i, val in enumerate(self.start_keys)
                                  if val == node.name and
                                  ((len(self.keys[i]) == 2 and
                                    self.keys[i][1] in [n.name for n in node.connections])
                                    or len(self.keys[i]) == 1)]
                    key = random.choice(valid_keys)
                    replace = self.create_nodes(key)
                    replace_node = None
                    for conn in node.connections[:]:
                        if len(key) == 2 and conn.name == key[1] and replace_node == None:
                            replace_node = conn
                        else:
                            conn.connect(replace[0])
                        conn.disconnect(node)
                    if replace_node != None:
                        for conn in replace_node.connections[:]:
                            conn.connect(replace[-1])
                            conn.disconnect(replace_node)
                    connections = replace[0].get_connected()
                    break
        self.nodes = connections
    
    def shuffle_nodes(self, node_list):
        nodes = []
        returned = []
        for conn in node_list:
            if not conn.transversed:
                conn.transversed = True
                connnodes, connreturned = self.shuffle_nodes(conn.connections)
                returned.extend(connreturned)
                if conn.backtrackable:
                    nodes.append(conn)
                    nodes.extend(connnodes)
                else:
                    nodes.append({conn: connnodes})
                    
        for node in returned[:]:
            if node_list == [self.entrance]:
                returned.remove(node)
                nodes[0].values()[0].insert(0, node)
            elif random.random() >= node.returnchance:
                returned.remove(node)
                nodes.insert(0, node)
        for node in nodes[:]:
            try:
                if node_list != [self.entrance] and random.random() < node.returnchance:
                    nodes.remove(node)
                    returned.append(node)
            except AttributeError: pass
        return nodes, returned
    
    def connect_nodes(self, nodes, cur_node=None):
        for node in nodes:
            if isinstance(node, dict):
                if cur_node: cur_node.connect(node.keys()[0])
                self.connect_nodes(node.values()[0], node.keys()[0])
            else:
                cur_node.connect(node)
                
    def absorb_nodes(self, node_list, cur_node = None):
        nodes = []
        for conn in node_list:
            if not conn.transversed:
                conn.transversed = True
                connnodes = self.absorb_nodes(conn.connections, conn)
                absorbable = hasattr(conn, "absorbable") and conn.absorbable                
                absorbed = False
                if absorbable:
                    assert(cur_node)
                    try:
                        absorbed = isinstance(cur_node.replace_on_room_clear[0], basestring)
                    except AttributeError:
                        absorbed = True
                if absorbed:
                    cur_node.replace_on_room_clear = [conn]
                    for node in conn.connections[:]:
                        conn.disconnect(node)
                        if node is not cur_node:
                            cur_node.connect(node)
                    nodes.extend(connnodes)
                elif conn.backtrackable:
                    nodes.append(conn)
                    nodes.extend(connnodes)
                elif connnodes:
                    nodes.append({conn: connnodes})
                else:
                    nodes.append(conn)
        return nodes
    
    def add_difficulty(self, node):
        for conn in node.connections:
            if not hasattr(conn, "difficulty"):
                conn.difficulty = node.difficulty + 1
                self.add_difficulty(conn)
                if hasattr(conn, "challenge"):
                    conn.difficulty *= conn.challenge
                try:
                    conn.difficulty *= conn.replace_on_room_clear[0].challenge
                except AttributeError:
                    pass
                conn.difficulty = int(conn.difficulty)
                
    def add_rewards(self):
        test_nodes = [node for node in self.flatten_nodes(self.nodes) if
                        node.__class__ is nodes.nodetypes["Test"]]
        random.shuffle(test_nodes)
        added_compass = False
        added_map = False
        start_difficulty = self.entrance.difficulty
        end_difficulty = self.exit.difficulty
        delta_difficulty = end_difficulty - start_difficulty
        map_difficulty_min = delta_difficulty*MAP_DIFFICULTY
        compass_difficulty_min = delta_difficulty*COMPASS_DIFFICULTY
        for node in test_nodes:
            if hasattr(node, "replace_on_room_clear"): continue
            node_delta = node.difficulty-start_difficulty
            addnode = None
            if node_delta >= compass_difficulty_min and not added_compass:
                added_compass = True
                addnode = nodes.nodetypes["Compass"]()
            elif node_delta >= map_difficulty_min and not added_map:
                added_map = True
                addnode = nodes.nodetypes["Map"]()
            if addnode is not None:
                node.difficulty *= addnode.challenge
                node.replace_on_room_clear = [addnode]

    def flatten_nodes(self, nodelist):
        nodes = []
        for node in nodelist:
            if isinstance(node, dict):
                nodes.append(node.keys()[0])
                nodes.extend(self.flatten_nodes(node.values()[0]))
            else:
                nodes.append(node)
        return nodes
    
    def add_map(self, cur_node, ignore = None):
        pref = ["N", "E", "S", "W"]
        random.shuffle(pref)
        dir = 0
        if len(cur_node.connections) > 4:
            addnode = nodes.nodetypes["Nothing"]()
            addnode.difficulty = cur_node
            cur_node.connect(addnode)
            while len(cur_node.connections) > 4:
                conn = cur_node.connections[-2]
                conn.disconnect(cur_node)
                conn.connect(addnode)
        #print "START NODE", cur_node
        for node in cur_node.connections:
            if node is not ignore:
                success = False
                while (not success):
                    if dir == 4:
                        self.remove_map(cur_node, ignore)
                        return False
                    success = True
                    try:
                        if self.map.append(cur_node, node, pref[dir]) is True:
                            if not self.add_map(node, cur_node):
                                self.map.remove_obj(node)
                                success = False
                        else:
                            success = False
                    except AssertionError:
                        success = False
                    dir+=1
        #print "END NODE", cur_node
        return True
        
    def remove_map(self, cur_node, ignore):
        self.map.remove_obj(cur_node)
        for node in cur_node.connections:
            if node is not ignore:
                self.remove_map(node, cur_node)

    def count_nodes(self, cur_node):
        count = 1
        cur_node.transversed = True
        for node in cur_node.connections:
            if not node.transversed:
                count += self.count_nodes(node)
        return count

if __name__ == '__main__':
    d = Nodes()
    d.create_dungeon()
    ta = tilearray.TileArray(d.map.map)
    print ta