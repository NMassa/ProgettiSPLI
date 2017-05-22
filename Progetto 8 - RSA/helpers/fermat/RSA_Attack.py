'''
THIS IS RSA ATTACK SYSTEM THAT WORKS IF N HAS A RELATIVE SMALL NUMBER OF DIGITS AND THE PLAINT TEXT IS NOT PADDED
'''
import math


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
    print('p = ', p)
    print('q = ', q)
    mode = (p-1)*(q-1)
    print('(p-1)*(q-1)= ', mode)
    e = int(input("Now enter e: "))
    print('Finding d .........')
    for d in range(0, n):
        if e*d % mode == 1:
            print('d = ', d)
            break
    ct = int(input("Enter the cipher text: "))
    print('Decyption.........')
    p = pow(ct, d, n)
    print('The plain text: ', p)


# THIS IS THE MAIN METHOD YOU HAVE TO RUN IT TO RUN THE POROGRAM
if __name__ == "__main__":
    print('Welcome to RSA attack system')
    print('Please enter the number you want to factor')
    n = int(input("N: "))
    factor(n)