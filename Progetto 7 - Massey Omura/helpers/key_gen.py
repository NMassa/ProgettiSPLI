from helpers.utils import *

def toBinary(n):
    return ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])
def toNum(b):
    dec =int(b,2)
    return dec
def fromHEx_tobin(h):
    h_size = len(h) *8
    h = (bin(int(h, 32))[2:]).zfill(h_size)
    return h

#def gen_keys(out_lck, keyb):
def gen_keys(out_lck, keyb):
    output(out_lck, "keys....")