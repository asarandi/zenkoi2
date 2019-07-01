#!/usr/bin/env python3

import json

with open('data/PondData.json') as fp:
    data = fp.read().encode('utf-8')
    fp.close()

prey = json.loads(data)['prey']

for p in prey:
    print(p['id'], p['name'], p['xp'], p['edible'])

