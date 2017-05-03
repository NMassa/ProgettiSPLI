import random
import hashlib
#from helpers.utils import *

def toBinary(n):
    return ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])
def toNum(b):
    dec =int(b,2)
    return dec

def gen_keys(out_lck, skeyb):
    print("\t\t KEY8 \t")
    i=0
    keys=[]
    Left = keyb[:len(keyb)//2]
    Right = keyb[len(keyb)//2:]
    Left1=Left
    Right1=Right
    #shift 1 Left and Right
    for i in range(0,4):
        if(i<4):
            Left1=Left1[(1 % len(Left1)):] + Left1[:(1 % len(Left1))]
            Right1=Right1[(1 % len(Right1)):] + Right1[:(1 % len(Right1))]
            keyret=Left1+Right1
            keys.append(keyret)
            #print("Left: "+Left +"\tLeft1: "+Left1)
            #print("Right: "+Right +"\tRight1: "+Right1)
            print("KEYRET:"+keyret)
            dec= toNum(keyret)
            print("DEC:"+str(dec))
    #invert left and right
    Left2=Right
    Right2=Left
    #print("\t \t Invert left and right")
    for i in range(0,4):
        if(i<4):
            Left2=Left2[(1 % len(Left2)):] + Left2[:(1 % len(Left2))]
            Right2=Right2[(1 % len(Right2)):] + Right2[:(1 % len(Right2))]
            keyret=Left2+Right2
            keys.append(keyret)
            #print("Left (Right): "+Right+"\tLeft1: "+Left2)
            #print("Right (Left): "+Left +"\tRight1: "+Right2)
            print("KEYRET:"+keyret)
            dec = toNum(keyret)
            print("DEC:" + str(dec))
    return keys

#prendo chiave da 8 e restituisco tot chiavi da 32 tutte diverse (una per round-->8)
#def gen_key32(out_lck, keyb):
def gen_8key32(out_lck, keyb):

    # output(out_lck, "Key base: %s" % keyb)
    # output(out_lck, "Generating subkeys...")
    print("\t\t 8 KEY32 \t")
    i = 0
    keys = []
    Left = keyb[:len(keyb) // 2]
    Right = keyb[len(keyb) // 2:]
    Left1 = Left
    Right1 = Right
    # shift 1 Left and Right
    for i in range(0, 4):
        Left1 = Left1[(1 % len(Left1)):] + Left1[:(1 % len(Left1))]
        Right1 = Right1[(1 % len(Right1)):] + Right1[:(1 % len(Right1))]

        keyret = Left1 + Right1
        key32 = keyret + keyret + keyret + keyret + keyret + keyret
        keys.append(key32)
        print("KEYRET:" + key32)
        dec = toNum(key32)
        print("DEC:" + str(dec))
        # output(out_lck, "Subkey %s: %s" % (i, key32))

    # invert left and right
    Left2 = Right
    Right2 = Left
    for i in range(0, 4):
        Left2 = Left2[(1 % len(Left2)):] + Left2[:(1 % len(Left2))]
        Right2 = Right2[(1 % len(Right2)):] + Right2[:(1 % len(Right2))]

        keyret = Left2 + Right2
        key32 = keyret + keyret + keyret + keyret + keyret + keyret
        keys.append(key32)
        print("KEYRET:" + key32)
        dec = toNum(key32)
        print("DEC:" + str(dec))
        # output(out_lck, "Subkey %s: %s" % (i + 4, key32))

    return keys

def gen_16key32(out_lck, keyb):
    #output(out_lck, "Key base: %s" % keyb)
    #output(out_lck, "Generating subkeys...")
    print("\t\t 16 KEY32 \t")
    i=0
    keys=[]
    Left = keyb[:len(keyb)//2]
    Right = keyb[len(keyb)//2:]
    Left1=Left
    Right1=Right

    # shift 1 Left and Right
    for i in range(0, 4):
        Left1 = Left1[(1 % len(Left1)):] + Left1[:(1 % len(Left1))]
        Right1 = Right1[(1 % len(Right1)):] + Right1[:(1 % len(Right1))]

        keyret = Left1 + Right1
        key32 = keyret + keyret + keyret +keyret +keyret + keyret
        keys.append(key32)
        print("KEYRET:" + key32)
        dec = toNum(key32)
        print("DEC:" + str(dec))
        #output(out_lck, "Subkey %s: %s" % (i, key32))

    # invert left and right
    Left2 = Right
    Right2 = Left
    for i in range(0, 4):
        Left2 = Left2[(1 % len(Left2)):] + Left2[:(1 % len(Left2))]
        Right2 = Right2[(1 % len(Right2)):] + Right2[:(1 % len(Right2))]

        keyret = Left2 + Right2
        key32 = keyret + keyret + keyret + keyret + keyret + keyret
        keys.append(key32)
        print("KEYRET:" + key32)
        dec = toNum(key32)
        print("DEC:" + str(dec))
        #output(out_lck, "Subkey %s: %s" % (i + 4, key32))

    #only left
    Left2 = Left
    Right2 = Left
    for i in range(0, 4):
        Left2 = Left2[(1 % len(Left2)):] + Left2[:(1 % len(Left2))]
        Right2 = Right2[(1 % len(Right2)):] + Right2[:(1 % len(Right2))]

        keyret = Left2 + Right2
        key32 = keyret + keyret + keyret + keyret + keyret + keyret
        keys.append(key32)
        print("KEYRET:" + key32)
        dec = toNum(key32)
        print("DEC:" + str(dec))
        # output(out_lck, "Subkey %s: %s" % (i + 4, key32))

    #only right
    Left2 = Right
    Right2 = Right
    for i in range(0, 4):
        Left2 = Left2[(1 % len(Left2)):] + Left2[:(1 % len(Left2))]
        Right2 = Right2[(1 % len(Right2)):] + Right2[:(1 % len(Right2))]

        keyret = Left2 + Right2
        key32 = keyret + keyret + keyret + keyret + keyret + keyret
        keys.append(key32)
        print("KEYRET:" + key32)
        dec = toNum(key32)
        print("DEC:" + str(dec))
        # output(out_lck, "Subkey %s: %s" % (i + 4, key32))

    return keys

def gen_md5_32(pwd):
    h_obj=hashlib.md5(str(pwd))
    #print(h_obj.hexdigest())
    return(h_obj.hexdigest())

if __name__ == "__main__":
    print ("Generate Key")
    key = str(random.randrange(0,256))
    print (key)
    keyb= toBinary(int(key))
    print (keyb)
    gen_keys(str(keyb))
    gen_8key32(str(keyb))
    gen_16key32(str(keyb))
    gen_md5_32('abcdehehheeh')