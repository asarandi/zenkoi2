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

    headers = {
                'Host'              : 'landshark-zenkoi.appspot.com',
                'Accept'            : '*/*',
                'Content-Type'      : 'application/x-www-form-urlencoded',
                'User-Agent'        : 'ios/8813 CFNetwork/894 Darwin/17.4.0',
                'Connection'        : 'keep-alive',
                'Secret'            : '123456789',
                'Accept-Language'   : 'en-us',
                'Accept-Encoding'   : 'br, gzip, deflate',
                'X-Unity-Version'   : '5.6.4p3'
                }


    data = {
                'var1'              : var1,
                'var2'              : var2,
                'var3'              : var3,
                'var4'              : 'iPhone7,1|iOS 11.2.6 ^ en',
                'clientVersion'     : clientVersion,
                'var5'              : '-25200.000016',
                'var6'              : 'en',
                'var7'              : 'US',
                'idfa'              : '00000000-0000-0000-0000-000000000000',
                'adTrackingOn'      : '0',
                'checkSeq'          : '0',
                'seq'               : '0'
                }

#    r = requests.post('http://127.0.0.1:4242/index.php', data=data, headers=headers)
    r = requests.post('https://landshark-zenkoi.appspot.com/ZK2/GetGameStartData.php', data=data, headers=headers)
    if r.status_code != 200: return None
    return parse_qs(r.content.decode('utf-8'))


t_start = time.time()
r = GetGameStartData()
if not r: sys.exit('error')

print(r)

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

while True:
    if (level < 1) or (level > 8):
        break

    if level > 1:
        mv = v['maxVelocity'].split('^');       mv[2] = mv[1];     v['maxVelocity'] = '^'.join(mv)
        mv = v['agilityBonus'].split('^');       mv[2] = mv[1];     v['agilityBonus'] = '^'.join(mv)
        mv = v['intelligence'].split('^');       mv[2] = mv[1];     v['intelligence'] = '^'.join(mv)

    print('level', level)
    print()

    time.sleep(100)
    t_end = time.time()
    t_delta = (int)((t_end - t_start) * 1000)
    end = start + t_delta
    seq += 1
    fish = f"{v['fid']}~{v['skin']}~{v['colour']}~{v['spot']}~{v['maxVelocity']}~{v['agilityBonus']}~{v['boosts']}~{v['intelligence']}~{v['xp']}~{v['energy']}~{v['giftCount']}~{v['lastUpdate']}~{v['gems']}~{v['ascended']}"

    headers = {
                    'Host'                    : 'landshark-zenkoi.appspot.com',
                    'Accept'                  : '*/*',
                    'Content-Type'            : 'application/x-www-form-urlencoded',
                    'User-Agent'              : 'ios/8813 CFNetwork/894 Darwin/17.4.0',
                    'Connection'              : 'keep-alive',
                    'Secret'                  : '123456789',
                    'Accept-Language'         : 'en-us',
                    'Accept-Encoding'         : 'br, gzip, deflate',
                    'X-Unity-Version'         : '5.6.4p3'
            }

    food = []
    next_xp = 0

    if actions == []:
        for f in levels[level]['food']:
            ft = f['Type']
            fc = random.randrange(f['Count'], f['Count'] * 2)            
            for k in prey:
                if k['id'] == ft:
                    next_xp += (fc * k['xp'])
                    break
            food.append({'Count': fc, 'Type': ft})
        actions += levels[level]['actions']

    else:
        for k in prey:
            count = random.randrange(100, 200)
            prey_id = k['id']
            next_xp += (count * k['xp'])
            food.append({'Count': count, 'Type': prey_id})

    v['xp'] += next_xp

    if (p) and ('partner' in p):
        partner_number = p['partner'][0].split('|')[-1]
        actions.append('MATE|' + partner_number)
    if (p) and ('treasure' in p):
        s = p['treasure'][0].replace('|', '^')
        s += '^' + str(int(time.time() - random.randrange(100)))
        actions.append('OPEN_TREASURE|' + s)



    var4dict = {
                'class PondSessionClass'      : {
                        'clientStart'         : t,
                        'start'               : start,
                        'end'                 : end,
                        'food'                : food,
                        'actions'             : actions,
                        'fish'                : fish,
                        'countTowardsPortal'  : True,
                        'aBoost'              : 0,
                        'sBoost'              : 0
                    }
                }


    data = {
            'var1': var1,
            'var2': var2,
            'var3': var3,
            'var4': json.dumps([var4dict]),
            'var5': 'live',
            'clientVersion': clientVersion,
            'checkSeq': seq,
            'seq': seq
            }



    print('CLIENT:', data)
    print()

#    r = requests.post('http://127.0.0.1:4242/index.php', data=data, headers=headers)
    r = requests.post('https://landshark-zenkoi.appspot.com/ZK2/CommunicationsTick.php', data=data, headers=headers)
    start = end
    t_start = time.time()

    actions = []
    if r.status_code != 200:
        print(r.status_code)
        break
    p = parse_qs(r.content.decode('utf-8').strip())
    print('SERVER:', p)
    print()

    if p['result'][0][:2] != 'ok':
        break
    if 'seq' in p:
        seq = int(p['seq'][0])

    if level == 8:
        break
    if 'GEMS' in p:
        gems = p['GEMS'][0].split('|')[1]
        v['gems'] = gems
        level = int(v['gems'].split('-')[0])





#
#   e1z1r1p6% ./test1.py
#   {'\nresult': ['ok'], 'login': ['0^1^6^5^6^6^6^7^10^6^31^'], 'chal': ['C-32-0-5-0-E1,P-8-0-25-0-E2,E-0-0-30-0-E3,F-0-0-3-0-E4'], 'slitd': ['20095'], 't': ['1561785905'], 'seqReset': ['837'], 'dp': ['6'], 'pc': ['21'], 'ec': ['210'], 'aw': ['21'], 'asc': ['6'], 'boostA': ['2'], 'boostS': ['2'], 'fishSlots': ['5'], 'travc': ['0'], 'flags': ['3'], 'achievements': ['AIAAAAAAAA'], 'created': ['1545072344'], 'fishList': ['{"13":{"fid":"13","skin":"1","colour":"1","spot":"3","xp":"53156","energy":"100","giftCount":"0","lastUpdate":"1561785834","alt_name":"","ascended":0,"model":"GeneticsClass","maxVelocity":"2^8^8","agilityBonus":"0^8^8","boosts":"0^0^0","intelligence":"3^7^3","gems":"2-0^0-584^0-590^1-597^0-9^0-7"}}'], 'collection': ['{"0":"0~50c0908","1":"1~c00","70":"70~c"}'], 'dragons': ['{"0":"0~80800","70":"70~c","1":"1~400"}'], 'AppleGameCenterUid': ['G:12107361000'], 'zenPondVersion': ['1'], 'zenPondData': ['AAP.tACxAAB..wAAAAkAjP81AAF..wAA'], 'decoOwned': ['3*1|9*1|8*1']}
#
#   result ['ok']
#   login ['0^1^6^5^6^6^6^7^10^6^31^']
#   chal ['C-32-0-5-0-E1,P-8-0-25-0-E2,E-0-0-30-0-E3,F-0-0-3-0-E4']
#   slitd ['20095']
#   t ['1561785905']
#   seqReset ['837']
#   dp ['6']
#   pc ['21']
#   ec ['210']
#   aw ['21']
#   asc ['6']
#   boostA ['2']
#   boostS ['2']
#   fishSlots ['5']
#   travc ['0']
#   flags ['3']
#   achievements ['AIAAAAAAAA']
#   created ['1545072344']
#   fishList ['{"13":{"fid":"13","skin":"1","colour":"1","spot":"3","xp":"53156","energy":"100","giftCount":"0","lastUpdate":"1561785834","alt_name":"","ascended":0,"model":"GeneticsClass","maxVelocity":"2^8^8","agilityBonus":"0^8^8","boosts":"0^0^0","intelligence":"3^7^3","gems":"2-0^0-584^0-590^1-597^0-9^0-7"}}']
#   collection ['{"0":"0~50c0908","1":"1~c00","70":"70~c"}']
#   dragons ['{"0":"0~80800","70":"70~c","1":"1~400"}']
#   AppleGameCenterUid ['G:12107361000']
#   zenPondVersion ['1']
#   zenPondData ['AAP.tACxAAB..wAAAAkAjP81AAF..wAA']
#   decoOwned ['3*1|9*1|8*1']
#
#
#

#
#{
#-        "fid":"13",
#-        "skin":"1",
#-        "colour":"1",
#-        "spot":"3",
#-        "xp":"53156",
#-        "energy":"100",
#-        "giftCount":"0",
#-        "lastUpdate":"1561785834",
#        "alt_name":"",
#-        "ascended":0,
#        "model":"GeneticsClass",
#-        "maxVelocity":"2^8^8",
#-        "agilityBonus":"0^8^8",
#-        "boosts":"0^0^0",
#-        "intelligence":"3^7^3",
#-        "gems":"2-0^0-584^0-590^1-597^0-9^0-7"}
#
#
#fid ~ skin ~ colour ~ spot ~ maxVelocity ~ agilityBonus ~ boosts ~ intelligence ~ xp ~ energy ~ giftCount ~ lastUpdate ~ gems ~ ascended
#
#

#
#   {'var1': ['oX3u.56fFk6xSflr.qZRz6'], 'var2': ['iOS'], 'var3': ['a3c33c65edaa63d7db3e2baf34d882f7'], 'var4': ['[{"class PondSessionClass":{"clientStart":1561783433,"start":1270,"end":101318,"food":[],"actions":[],"fish":"13~1~1~3~2^8^8~0^8^8~0^0^0~3^7^3~53156~100~0~1561781852~2-0^0-584^0-590^1-597^0-9^0-7~0","countTowardsPortal":true,"aBoost":0,"sBoost":0}}]'], 'var5': ['live'], 'clientVersion': ['2.1.13'], 'checkSeq': ['814'], 'seq': ['814\n']}
#
#




