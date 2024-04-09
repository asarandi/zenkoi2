#!/usr/bin/env python3

import sys
import json
import time
import requests
from urllib.parse import parse_qs
from game_client import ticklen, var1, var2, var3, var4, clientVersion

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

t_delta = time.time()
time.sleep(ticklen)
t_end = int((time.time() - t_delta) * 1000) + t_start

actions = ["FRAMERATE|29"]
challenges = resp['chal'][0].split(',')
for i in range(20000):
    for chal in challenges:
        actions.append("CLAIMTASK|" + chal)

session = {
        "class PondSessionClass": {
            "clientStart": clientStart,
            "start":str(t_start),
            "end":str(t_end),
            "food":[],
            "actions":actions,
            "fish": make_fish_string(fdata),
            "countTowardsPortal": True,
            "aBoost":0,
            "sBoost":0
            }
        }

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
