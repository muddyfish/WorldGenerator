#!/usr/bin/env python

import json
from collections import Counter

f = open("dungeon_tile_config.json")
values_dict = json.load(f)["tile_values"]
values = []
for i in range(len(values_dict)-1):
    values.append(tuple(map(tuple, values_dict[str(i)])))
f.close()

dupes = [k for k,v in Counter(values).items() if v>1]

d = {}
for i, v in enumerate(values):
    if v in dupes:
        if hash(v) not in d:
            d[hash(v)] = []
        else:
            d[hash(v)].append(i)
for_del = []
for i in d.values():
    for_del.extend(i)
for_del = sorted(for_del, reverse = True)
for i in for_del:
    del values[i]
new_values = dict(enumerate(values))
new_values[99] = values_dict["99"]
print json.dumps(new_values, sort_keys=True)
print for_del