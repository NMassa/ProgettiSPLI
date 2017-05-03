import hashlib

from bitarray import bitarray
from helpers.key_gen import *
from helpers.utils import *


class Cipher:
    file = None
    keys = None
    chunks = None
    encrypted = []
    decrypted = []

    def __init__(self, out_lck, chunks, key):
        self.keys = []
        self.chunks = chunks
        chunk_len = 64

        # creo chiavi
        self.keys = gen_8key32(out_lck, key)

        # controllo lunghezza chunk, se è più corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(chunk_len)

    def encrypt(self):

        for chunk in self.chunks:
            for k_i in self.keys: # il numero di chiavi è anache il numero di rounds dell'algoritmo
                chunk = self.round_encode(chunk, k_i)
            self.encrypted.append(chunk)

    def decrypt(self):

        for chunk in self.chunks:
            for k_i in reversed(self.keys): # il numero di chiavi è anache il numero di rounds dell'algoritmo
                chunk = self.round_decode(chunk, k_i)
            self.decrypted.append(chunk)

    def decrypt_brute_force(self):
        stringa = ['89504e470d0a1a0a', 'ffd8ffe000104a46', '424df640000', '89504e47da1aa', '47496383961181']
        pippo = True
        stop = True # variabile che con vero non mi esamina tutto il file
        index = 0
        out = 0

        for chunk in self.chunks:
            if pippo:
                for k_i in reversed(self.keys):  # il numero di chiavi è anache il numero di rounds dell'algoritmo
                    chunk = self.round_decode(chunk, k_i)

                if index == 0:
                    for i in stringa:
                        check = bin(int(i, 16))[2:]
                        if chunk == check:

                            if i == '89504e470d0a1a0a':
                                print('detect format file: PNG')
                                out = 1
                            elif i == 'ffd8ffe000104a46':
                                print('detect format file: JPG')
                                out = 2
                            elif i == '424df640000':
                                print('detect format file: BMP')
                                out = 3
                            pippo = True
                            # indico che posso andare avanti con il file
                            stop = False
                            break
                        else:
                            #print('non trovato')
                            pippo = False
                    index = 1

            if not stop:
                self.decrypted.append(chunk)
            else:

                break

        return out

    def round_encode(self, chunk, key_i):
        left = chunk[:int(len(chunk)/2)]
        right = chunk[int(len(chunk)/2):]

        new_left = right

        xor = xor_func(right, key_i)

        ba = bitarray(xor)  # obtain bitarray object from string message
        bytes = ba.tobytes()  # get bytes

        md5 = hashlib.md5()
        md5.update(bytes)
        dig = md5.digest()
        D = ''  # binary representation of dig
        for i in range(0, len(dig)):
            d = bin(dig[i])[2:]  # binary representation of dig[i]
            while (len(d) < 8):
                d = '0' + d
            D += d

        new_right = xor_func(D[:32], left)

        new_chunk = new_left + new_right

        return new_chunk

    def round_decode(self, chunk, key_i):
        left = chunk[:int(len(chunk)/2)]
        right = chunk[int(len(chunk)/2):]

        new_right = left

        xor = xor_func(left, key_i)

        ba = bitarray(xor)  # obtain bitarray object from string message
        bytes = ba.tobytes()  # get bytes

        md5 = hashlib.md5()
        md5.update(bytes)
        dig = md5.digest()
        D = ''  # binary representation of dig
        for i in range(0, len(dig)):
            d = bin(dig[i])[2:]  # binary representation of dig[i]
            while (len(d) < 8):
                d = '0' + d
            D += d

        new_left = xor_func(D[:32], right)

        new_chunk = new_left + new_right

        return new_chunk