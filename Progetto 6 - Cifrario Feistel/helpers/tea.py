import struct
import re

DELTA = 0x9e3779b9  # key schedule constant

def ul(v):
    return v & 0xFFFFFFFF


def encrypt(v0, v1, key, rounds=8):
    assert len(key) == 16
    sum = 0
    for i in range(rounds):
        v0 = ul(v0 + ((v1 << 4 ^ v1 >> 5) + v1 ^ sum + int(key[sum & 3])))
        sum = ul(sum + DELTA)
        v1 = ul(v1 + ((v0 << 4 ^ v0 >> 5) + v0 ^ sum + int(key[sum>>11 & 3])))
    return v0, v1


def decrypt(v0, v1, key, rounds=8):
    assert len(key) == 16
    sum = ul(DELTA * rounds)
    for i in range(rounds):
        v1 = ul(v1 - ((v0 << 4 ^ v0 >> 5) + v0 ^ sum + int(key[sum>>11 & 3])))
        sum = ul(sum - DELTA)
        v0 = ul(v0 - ((v1 << 4 ^ v1 >> 5) + v1 ^ sum + int(key[sum & 3])))
    return v0, v1


def encipher(s, key):
    """TEA-encipher a string"""
    assert struct.calcsize('I') == 4
    s = s.ljust(8 * int((len(s) + 7) / 8), bytes('\x00'.encode('utf-8')))  # pad with 0's
    u = struct.unpack('%dI' % (len(s) / 4), s)
    e = [encrypt(u[i], u[i + 1], key) for i in range(len(u))[::2]]
    return b''.join([struct.pack('2I', ee, ef) for ee, ef in e])


def decipher_raw(s, key):
    """TEA-decipher a raw string"""
    assert struct.calcsize('I') == 4
    assert len(s) % 8 == 0, len(s)
    u = struct.unpack('%dI' % (len(s) / 4), s)
    e = [decrypt(u[i], u[i + 1], key) for i in range(len(u))[::2]]
    return b''.join([struct.pack('2I', ee, ef) for ee, ef in e])


def decipher(s, key): # s = message
    """TEA-decipher a readable string"""
    return decipher_raw(s, key).rstrip(bytes('\x00'.encode('utf-8')))


def tea_encryptfile(file, key):
    message = None
    result = None
    #output_file = open('received/tea_encrypted', 'wb')

    if not message:
        input = open(file, 'rb')
        message = input.read()
        input.close()
        result = encipher(message, key)
        #output_file.write(result)
        #output_file.close()
    return result


def tea_decryptfile(filein, fileout, key):
    message = None
    tea_decrypted = open(fileout, 'wb')

    if not message:
        input = open(filein, 'rb')
        message = input.read()
        input.close()
        result = decipher(message, key)
        tea_decrypted.write(result)
        tea_decrypted.close()


def decrypt2(v0, v1, key, rounds=8):
    assert len(key) == 16
    sum = ul(DELTA * rounds)
    for i in range(8):
        v1 = ul(v1 - ((v0 << 4 ^ v0 >> 5) + v0 ^ sum + int(key[sum >> 11 & 3])))
        sum = ul(sum - DELTA)
        v0 = ul(v0 - ((v1 << 4 ^ v1 >> 5) + v1 ^ sum + int(key[sum & 3])))
    return v0, v1


def decipher_raw2(s, key):
    """TEA-decipher a raw string"""
    assert struct.calcsize('I') == 4
    assert len(s) % 8 == 0, len(s)
    u = struct.unpack('%dI' % (len(s) / 4), s)
    stringa = str(b'\xff\xd8\xff').replace('\'', '')
    for i in range(len(u))[::2]:
        e = [decrypt2(u[i], u[i + 1], key)]
        i = b''.join([struct.pack('2I', ee, ef) for ee, ef in e])

        prova = str(i).replace('\'', '')

        #lel = prova.find(stringa)

        if prova.find(stringa) != -1:
            print("detect format file: JPG")
            return 0
        else:
            return 1



def decipher2(s, key):  # s = message
    """TEA-decipher a readable string"""
    return decipher_raw2(s, key).rstrip(bytes('\x00'.encode('utf-8')))


def brute_force_tea(filein, fileout, key):
    message = None
    tea_decrypted = open(fileout, 'wb')

    if not message:
        input = open(filein, 'rb')
        message = input.read()
        input.close()
        result = decipher_raw2(message, key)
        if result == 0:
            tea_decryptfile(filein, fileout, key)
            return 0
        else:
            return 1
