from helpers.utils import output, calculateEncryptionKey, egcd
import math, rsa, random

from helpers import utils
from helpers.utils import output, toBinary8

from helpers.utils import output
import math


class Cipher:
    file = None
    keys = None
    chunks = None
    encrypted = []
    decrypted = []

    def __init__(self, out_lck, chunks, key, chunklen):
        self.keys = []
        self.chunks = chunks
        self.intchunks = []
        self.chunk_len = chunklen

        self.keys = key

        self.p = 0
        self.q = 0
        self.n = 0
        self.fn = 0
        self.e = 0
        self.d = 0

        self.generate_keys()

        for index in range(0,len(self.chunks)):
            if len(self.chunks[index]) < self.chunk_len:
                self.chunks[index] = self.chunks[index].zfill(self.chunk_len)
        '''
        # controllo lunghezza chunk, se e piu corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < self.chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(self.chunk_len)
        '''
        # ottengo i chunk in intero
        for chunk in self.chunks:
            self.intchunks.append(int(chunk, 2))

    def signature_encrypt(self, prvkey, mod):
        cryptedchunks = []
        for chunk in self.intchunks:
            cryptedchunks.append(pow(chunk, prvkey, mod))
        return cryptedchunks

    def signature_decrypt(self, pubkey, mod):
        decryptedchunks = []
        for chunk in self.intchunks:
            decryptedchunks.append(pow(chunk, pubkey, mod))
        return decryptedchunks

    def generate_keys(self):
        list_Prime = [3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41]
        if self.chunk_len < 9:
            self.p = 17#random.choice(list_Prime)
            self.q = 29#random.choice(list_Prime)
            self.n = self.p * self.q
            self.fn = (self.p - 1) * (self.q - 1)
            self.e = calculateEncryptionKey(self.n, self.fn)
            gcd, x, y = egcd(self.e, self.fn)
            if gcd != 1:
                output(self.out_lck, "no d key exist")
            else:
                self.d = x % self.fn
            return self.p, self.q, self.n, self.d, self.e
        else:
            (pub_key, priv_key) = rsa.newkeys(self.chunk_len)
            self.p = priv_key['p']
            self.q = priv_key['q']
            self.n = priv_key['n']
            self.d = priv_key['d']
            self.e = pub_key['e']
            return self.p, self.q, self.n, self.d, self.e

            """
            self.n = self.p * self.q
            self.fn = (self.p - 1) * (self.q - 1)
            #self.e = calculateEncryptionKey(self.n, self.fn)
            #self.e = calculateEncryptionKey(self.n, self.fn)
            self.e = pub_key['e']
            gcd, x, y = egcd(self.e, self.fn)
            if gcd != 1:
                output(out_lck, "no d key exist")
            else:
                self.d = x % self.fn
            """


def bruteforce(out_lck, chunks, mod):
    stringa = ['89504e470d0a1a0a', 'ffd8ffe000104a46', '424df640000', '89504e47da1aa', '47496383961181', '474946',
               'FFFB']
    out = 0
    pippo = 0
    decryptedchunks = []

    for i in range(1, 256):
        if pippo == 0:
            new_chunks = ''
            # prendo primi 8 chunks da 8 bit
            for chunk in chunks[0:6]:
                # trasformo chunk in intero e applico modulo
                new = (toBinary8(pow(int(chunk, 2), i, int(mod))))
                new_chunks = new_chunks + new

            for a in stringa:
                check = bin(int(a, 16))[2:]
                if new_chunks.find(check) != -1:
                    #any(check in s for s in new_chunks) != -1:
                    # if chunks.find(check) != -1:
                    if a == '89504e470d0a1a0a':
                        output(out_lck, '\ndetect format file: PNG')
                        out = 1
                    elif a == 'ffd8ffe000104a46':
                        output(out_lck, '\ndetect format file: JPG')
                        out = 2
                    elif a == '424df640000':
                        output(out_lck, '\ndetect format file: BMP')
                        out = 3
                    elif a == '474946':
                        output(out_lck, '\ndetect format file: GIF')
                        out = 4
                    elif a == 'FFFB':
                        output(out_lck, '\ndetect format file: MP3')
                        out = 5
                    key = i
                    pippo = 1
                    break
        else:
            break


    for chunk in chunks:
        # trasformo chunk in intero e applico modulo
        decryptedchunks.append(toBinary8(pow(int(chunk, 2), key, int(mod))))

    return out, decryptedchunks
