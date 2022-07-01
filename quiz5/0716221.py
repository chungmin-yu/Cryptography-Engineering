# -*- coding: utf-8 -*-
import hashlib
import random

m = hashlib.md5()
hexstring = input()
#hexstring = "c606196ea460a3a53ac3e81c614b990b"
data = bytes.fromhex(hexstring)
m.update(data)
h = m.hexdigest()
msb=h[0:4]
print(msb, end=' ')
while(True):
    new_m = hashlib.md5()
    new_hexstring = ''.join(random.choice("0123456789abcdef") for _ in range(32))
    new_data = bytes.fromhex(new_hexstring) 
    new_m.update(new_data)
    new_h = new_m.hexdigest()
    new_msb=new_h[0:4]
    if(msb==new_msb):
        print(new_hexstring)
        #print(new_h)
        break
