'''
THIS IS RSA ATTACK SYSTEM THAT WORKS IF THE PLAINTEXT IS PADDED 
'''
import math
import binascii


# THIS IS THE MAIN METHOD YOUHAVE TO RUN IT TO RUN THE POROGRAM
def run():
    print('Welcome to RSA attack system')
    print('Please enter the number you want to factor')
    n = input("N: ")
    factor(n)
    
    
# THIS METHOD FINDS THE MODULO MULTIPLICATVE INVERS 
def inverse(x, p):
    inv1 = 1
    inv2 = 0
    while p != 1:
        inv1, inv2 = inv2, inv1 - inv2 * (x / p)
        x, p = p, x % p

    return inv2


# THIS METHOD FINDS THE INTERGER SUQAURE ROOT OF A NUMBER
def intsqrt(n):
    x = n
    y = (x + n // x) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


# THIS METHOD FACTORIZE THE NUMBER TO TO ITS RPRIME FACTORS BASED OF FERMAT FACORING METHOD
def factor(n):
    a = intsqrt(n) 
    b2 = a*a - n
    b = intsqrt(n) 
    count = 0
    while b*b != b2:
        a = a + 1
        b2 = a*a - n
        b = intsqrt(b2)
        count += 1
    p=a+b
    q=a-b
    assert n == p * q
    print('Factoraizing.........')
    print('p = ',p)
    print('q = ',q)
    mode = (p-1)*(q-1)
    print('(p-1)*(q-1)= ',mode)
    e = input("Now enter e: ")
    print('Finding d .........')
    d = inverse(e,mode)
    print('d = ',d)
    ct = input("Enter the cipher text: ")
    print('Decyption.........')
    p = pow(ct, d, n)
    print('The plain text: ',p)
# IN THIS PART OF THE CODE THE PADDED DIGITS WILL BE REMOVE AND THE PLAIN TEXT WILL BE EXPOSED
    myp_binary = bin(p)
    print('The binary representation of plain text: ',myp_binary)
    myp_padd = p % pow(2,200)
    print('The plain text after removing the paddings: ',myp_padd)
    myp_padd_bin = bin(myp_padd)
    print('The binary representation of real plain text: ',myp_padd_bin)
    n = int(myp_padd_bin, 2)
    str = binascii.unhexlify('%x' % n)
    print('The ASCII representation:',str)
    

    
    
    
    