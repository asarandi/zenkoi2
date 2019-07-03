#!/usr/bin/env python3

import sys
import json
import time
import random
import hashlib
import requests
from gemsdata import levels
from urllib.parse import parse_qs

with open('data/PondData.json') as fp:
    data = fp.read().encode('utf-8')
    fp.close()

prey = json.loads(data)['prey']

var1 = 'oX3u.56fFk6xSflr.qZRz6'
var2 = 'iOS'
var3 = hashlib.md5(int(time.time()).to_bytes(4, byteorder='little')).hexdigest()
clientVersion = '2.1.14'

def GetGameStartData():

    headers = {'Host': 'landshark-zenkoi.appspot.com', 'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'ios/8813 CFNetwork/894 Darwin/17.4.0', 'Connection': 'keep-alive', 'Secret': '123456789', 'Accept-Language': 'en-us', 'Accept-Encoding': 'br, gzip, deflate', 'X-Unity-Version': '5.6.4p3'}

    data = {'var1': var1, 'var2': var2, 'var3': var3, 'var4': 'iPhone7,1|iOS 11.2.6 ^ en', 'clientVersion': clientVersion, 'var5': '-25200.000016', 'var6': 'en', 'var7': 'US', 'idfa': '00000000-0000-0000-0000-000000000000', 'adTrackingOn': '0', 'checkSeq': '0', 'seq': '0'}

    r = requests.post('https://landshark-zenkoi.appspot.com/ZK2/GetGameStartData.php', data=data, headers=headers)
    if r.status_code != 200: return None
    return parse_qs(r.content.strip().decode('utf-8'))


t_start = time.time()
r = GetGameStartData()
if not r: sys.exit('error')

print(r)

collection = [int(k) for k in json.loads(r['collection'][0])]
t = int(r['t'][0]);
seq = int(r['seqReset'][0])
fl = json.loads(r['fishList'][0])
k, v = fl.popitem()
v['xp'] = int(v['xp'])


start = (int)(time.time() - t_start)*1000
food = []
actions = ["FRAMERATE|30"]
p = None
level = int(v['gems'][0][0])
flag = True

while True:
    time.sleep(100)
    t_end = time.time()
    t_delta = (int)((t_end - t_start) * 1000)
    end = start + t_delta
    seq += 1
    fish = f"{v['fid']}~{v['skin']}~{v['colour']}~{v['spot']}~{v['maxVelocity']}~{v['agilityBonus']}~{v['boosts']}~{v['intelligence']}~{v['xp']}~{v['energy']}~{v['giftCount']}~{v['lastUpdate']}~{v['gems']}~{v['ascended']}"

    headers = {'Host': 'landshark-zenkoi.appspot.com', 'Accept': '*/*', 'Content-Type': 'application/x-www-form-urlencoded', 'User-Agent': 'ios/8813 CFNetwork/894 Darwin/17.4.0', 'Connection': 'keep-alive', 'Secret': '123456789', 'Accept-Language': 'en-us', 'Accept-Encoding': 'br, gzip, deflate', 'X-Unity-Version': '5.6.4p3'}

    food = []
    next_xp = 0


    food_list = levels[level]['food']
    k = random.randrange(0, len(food_list))
    count = random.randrange(30, 50)
    prey_id = food_list[k]['Type']
    next_xp += (count * prey[prey_id - 1]['xp'])
    food.append({'Count': count, 'Type': prey_id})

    v['xp'] += next_xp

    if (p) and ('partner' in p):
        my_fid = p['partner'][0].split('|')[-1]
        partner_data = p['partner'][0].split('~')
        partner_action = 'SPURN|' + my_fid
        if len(partner_data) > 1:
            if int(partner_data[1]) not in collection:
                partner_action = 'MATE|' + my_fid

        print(partner_action, partner_data, "\n")
        actions.append(partner_action)

    if (p) and ('treasure' in p):
        s = p['treasure'][0].replace('|', '^')
        s += '^' + str(int(time.time() - random.randrange(100)))
        actions.append('OPEN_TREASURE|' + s)

    var4dict = {'class PondSessionClass': {'clientStart': t, 'start': start, 'end': end, 'food': food, 'actions': actions, 'fish': fish, 'countTowardsPortal': True, 'aBoost': 0, 'sBoost': 0}}
    data = {'var1': var1, 'var2': var2, 'var3': var3, 'var4': json.dumps([var4dict]), 'var5': 'live', 'clientVersion': clientVersion, 'checkSeq': seq, 'seq': seq}

    print('CLIENT:', data, "\n")

    r = requests.post('https://landshark-zenkoi.appspot.com/ZK2/CommunicationsTick.php', data=data, headers=headers)
    start = end
    t_start = time.time()

    actions = []
    if r.status_code != 200:
        print(r.status_code)
        break
    p = parse_qs(r.content.decode('utf-8').strip())
    print('SERVER:', p, "\n")

    if p['result'][0][:2] != 'ok':
        break
    if 'seq' in p:
        seq = int(p['seq'][0])
        
    if flag:
        flag = False        
        mv = v['maxVelocity'].split('^');       mv[2] = mv[1];     v['maxVelocity'] = '^'.join(mv)
        mv = v['agilityBonus'].split('^');       mv[2] = mv[1];     v['agilityBonus'] = '^'.join(mv)
        mv = v['intelligence'].split('^');       mv[2] = mv[1];     v['intelligence'] = '^'.join(mv)

