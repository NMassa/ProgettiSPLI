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


        self.keys = key

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




