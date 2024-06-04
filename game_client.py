import time
import hashlib

ticklen = 30
var1 = 'c65371c08716b108'
var2 = 'Android'
var3 = hashlib.md5(int(time.time()).to_bytes(length=4, byteorder='little')).hexdigest()
var4 = 'Google Pixel 4a|Android OS 12 / API-32 (SQ3A.220705.003.A1/8672226) ^ en'
clientVersion = '2.7.2'


headers = {
    'Host':             'landshark-zenkoi.appspot.com',
    'User-Agent':       'UnityPlayer/2021.3.21f1 (UnityWebRequest/1.0, libcurl/7.84.0-DEV)',
    'Accept-Encoding':  'gzip, deflate',
    'Content-Type':     'application/x-www-form-urlencoded',
    'Accept-Language':  'en-us',
    'Accept':           '*/*',
    'Connection':       'keep-alive',
    'X-Unity-Version':  '2021.3.21f1'
}

initial_data = {
    'var1':           var1,
    'var2':           var2,
    'var3':           var3,
    'var4':           var4,
    'clientVersion':  clientVersion,
    'var5':          '-25200.425143',
    'var6':          'en',
    'var7':          'US',
    'checkSeq':      '0',
    'seq':           '0',
    'baseD':         '',
}
