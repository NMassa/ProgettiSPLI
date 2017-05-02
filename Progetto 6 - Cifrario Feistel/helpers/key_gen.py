import random

def toBinary(n):
    return ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])

def gen_keys(keyb):
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
    #invert left and right
    Left2=Right
    Right2=Left
    print("\t \t Invert left and right")
    for i in range(0,4):
        if(i<4):
            Left2=Left2[(1 % len(Left2)):] + Left2[:(1 % len(Left2))]
            Right2=Right2[(1 % len(Right2)):] + Right2[:(1 % len(Right2))]
            keyret=Left2+Right2
            keys.append(keyret)
            #print("Left (Right): "+Right+"\tLeft1: "+Left2)
            #print("Right (Left): "+Left +"\tRight1: "+Right2)
            print("KEYRET:"+keyret)
    return keys
#prendo chiave da 56 e restituisco tot chiavi da 48 tutte diverse (una per round-->8)
def gen_key32(keyb):
    print("\t\t KEY32 \t")
    i=0
    keys=[]
    Left = keyb[:len(keyb)//2]
    Right = keyb[len(keyb)//2:]
    Left1=Left
    Right1=Right
    # shift 1 Left and Right
    for i in range(0, 4):
        if (i < 4):
            Left1 = Left1[(1 % len(Left1)):] + Left1[:(1 % len(Left1))]
            Right1 = Right1[(1 % len(Right1)):] + Right1[:(1 % len(Right1))]
            keyret = Left1 + Right1
            key32 = keyret + keyret + keyret +keyret
            keys.append(key32)
            #print("Left: " + Left + "\tLeft1: " + Left1)
            #print("Right: " + Right + "\tRight1: " + Right1)
            print("KEY32:" + key32)
    # invert left and right
    Left2 = Right
    Right2 = Left
    print("\t \t Invert left and right")
    for i in range(0, 4):
        if (i < 4):
            Left2 = Left2[(1 % len(Left2)):] + Left2[:(1 % len(Left2))]
            Right2 = Right2[(1 % len(Right2)):] + Right2[:(1 % len(Right2))]
            keyret = Left2 + Right2
            key32 = keyret + keyret + keyret + keyret
            keys.append(key32)
            #print("Left (Right): " + Right + "\tLeft1: " + Left2)
            #print("Right (Left): " + Left + "\tRight1: " + Right2)
            print("KEY32:" + key32)
    return keys

if __name__ == "__main__":
    print ("Generate Key")
    key = str(random.randrange(0,256))
    print (key)
    keyb= toBinary(int(key))
    print (keyb)
    gen_keys(str(keyb))
    gen_key32(str(keyb))