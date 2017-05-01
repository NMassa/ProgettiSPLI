import hashlib

from bitarray import bitarray

from helpers.key_gen import *
from helpers.utils import *


class Cipher:
    def __int__(self, file, key):

        self.file = file
        self.key = key
        kes = []
        chunk_len = 8

        # creo chiavi
        keys = gen_keys(key)
        # prendo chunks di lunghezza chunk_len
        self.chunks = get_chunks("../files/" + file, chunk_len)
        print(self.chunks)

        # controllo lunghezza chunk, se è più corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(chunk_len)

    def encode(self):

        chunks_encoded = []
        for chunk in self.chunks:
            for k_i in self.keys: # il numero di chiavi è anache il numero di rounds dell'algoritmo
                # TODO: applico funzione al chunk con keys[i]
                chunk = self.round_encode(chunk, k_i)
            chunks_encoded.append(chunk)

    def decode(self):

        chunks_decoded = []
        for chunk in self.chunks:
            for k_i in reversed(self.keys):  # il numero di chiavi è anache il numero di rounds dell'algoritmo
                # TODO: applico funzione al chunk con keys[i]
                chunk = self.round_encode(chunk, k_i)
            chunks_decoded.append(chunk)

    def round_encode(self, chunk, key_i):
        left = chunk[:len(chunk) / 2]
        right = chunk[len(chunk) / 2:]

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

        new_right = xor_func(D[:8], left)

        new_chunk = new_left + new_right

        return new_chunk

    def round_decode(self, chunk, key_i):
        left = chunk[:len(chunk) / 2]
        right = chunk[len(chunk) / 2:]

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

        new_left = xor_func(D[:8], right)

        new_chunk = new_left + new_right

        return new_chunk