import time
import hashlib

ticklen = 30
var1 = 'c65371c08716b108'
var2 = 'Android'
var3 = hashlib.md5(int(time.time()).to_bytes(length=4, byteorder='little')).hexdigest()
var4 = 'iPhone5,1|iOS 10.3.3 ^ en'
clientVersion = '2.7.1'
