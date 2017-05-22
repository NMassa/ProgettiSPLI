'''
THIS IS RSA SYSTEM
'''
import math

if __name__ == "__main__":
    print('Welcome to RSA system')
    print('Please enter p & q ,where p & q are two large prime numbers')
    p = int(input("p: "))
    q = int(input("q: "))
    n = p*q
    print('N:', n)
    print('Now enter e')
    e = int(input("e: "))
    print('The public key is (%s,%s)' % (n, e))
    mode = (p-1)*(q-1)
    for d in range(0, n):
        if e*d % mode == 1:
            break
    print('The private key is ', d)
    print('Enter The plain text ')
    plain = float(input("plaintext: "))
    ct = (math.pow(plain, e)) % n
    print('encyption.........')
    print('The ciphertext ', ct)
    
    

    
