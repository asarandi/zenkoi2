#!/usr/bin/env python3

import sys
import json
import time
import random
import requests
from urllib.parse import parse_qs
from gemsdata import levels
from game_client import ticklen, var1, var2, var3, var4, clientVersion

with open('data/PondData.json') as fp:
    prey = json.load(fp)['prey']
    fp.close()

headers = {
    'Host':             'landshark-zenkoi.appspot.com',
    'User-Agent':       'Zen%20Koi%202/9144 CFNetwork/811.5.4 Darwin/16.7.0',
    'Accept-Encoding':  'gzip, deflate',
    'Content-Type':     'application/x-www-form-urlencoded',
    'Accept-Language':  'en-us',
    'Accept':           '*/*',
    'Connection':       'keep-alive',
    'X-Unity-Version':  '2018.3.11f1'
}

data = {
    'var1':           var1,
    'var2':           var2,
    'var3':           var3,
    'var4':           var4,
    'clientVersion':  clientVersion,
    'var5':          '-25200.000077',
    'var6':          'en',
    'var7':          'US',
    'idfa':          '00000000-0000-0000-0000-000000000000',
    'adTrackingOn':  '0',
    'checkSeq':      '0',
    'seq':           '0'
}

print("CLIENT HELLO:", data, "\n")

req = requests.post('https://landshark-zenkoi.appspot.com/ZK2/GetGameStartData.php', headers=headers, data=data)
if req.status_code != 200:
    sys.exit('error')

def make_fish_string(f):     # expecting f to be a dictionary from fishList
    return f"{f['fid']}~{f['skin']}~{f['colour']}~{f['spot']}~{f['maxVelocity']}~{f['agilityBonus']}~{f['boosts']}~{f['intelligence']}~{f['xp']}~{f['energy']}~{f['giftCount']}~{f['lastUpdate']}~{f['gems']}~{f['ascended']}"

resp = parse_qs(req.content.decode('utf-8').strip())

print("SERVER HELLO:", resp, "\n")

if ('result' not in resp) or (resp['result'][0] != 'ok'):
    sys.exit('error')

clientStart = int(resp['t'][0])
fishList = json.loads(resp['fishList'][0])
sequence = int(resp['seqReset'][0]) + 1
fid, fdata = fishList.popitem()

t_start = int((time.time() * 1000) - (clientStart * 1000))

done = False
while not done:

    t_delta = time.time()
    time.sleep(ticklen)
    t_end = int((time.time() - t_delta) * 1000) + t_start

    food = []
    actions = []
    actions.append('SPURN|' + str(fid))

    if 'GEMS' in resp:
        gems = resp['GEMS'][0].split('|')[1]
        fdata['gems'] = gems
    level = int(fdata['gems'].split('-')[0])

    if 'treasure' in resp:
        treasure = resp['treasure'][0].replace('|', '^')
        treasure += '^' + str(int(time.time() - random.randrange(ticklen)))
        actions.append('OPEN_TREASURE|' + treasure)

    next_xp = 0

    for food_item in levels[level]['food']:
        food_type = food_item['Type']
        food_count = random.randrange(food_item['Count'], food_item['Count'] * 2)
        for prey_item in prey:
            if prey_item['id'] == food_type:
                next_xp += (food_count * prey_item['xp'])
                break
        food.append({'Count': food_count, 'Type': food_type})

    actions += levels[level]['actions']

    session = {
            "class PondSessionClass": {
                "clientStart": clientStart,
                "start":str(t_start),
                "end":str(t_end),
                "food": food,
                "actions": actions,
                "fish": make_fish_string(fdata),
                "countTowardsPortal": True,
                "aBoost":0,
                "sBoost":0
                }
            }

    fdata['xp'] = int(fdata['xp']) + next_xp

    data = {
        'var1':           var1,
        'var2':           var2,
        'var3':           var3,
        'var4':           json.dumps([session]),
        'var5':           'live',
        'clientVersion':  clientVersion,
        'ctc':            '0',
        'checkSeq':       sequence,
        'seq':            sequence
    }

    t_start = t_end

    print("CLIENT:", data, "\n")

    req = requests.post('https://landshark-zenkoi.appspot.com/ZK2/CommunicationsTick.php', headers=headers, data=data)
    
    if req.status_code != 200:
        sys.exit('error, status code: %d' % (req.status_code,))
        
    resp = parse_qs(req.content.decode('utf-8').strip())

    print("SERVER:", resp, "\n")

    if ('result' not in resp) or (resp['result'][0] != 'ok'):
        done = True

    if 'seq' in resp:
        sequence = int(resp['seq'][0]) + 1
    else:
        sequence += 1

    if level >= 8:
        done = True

