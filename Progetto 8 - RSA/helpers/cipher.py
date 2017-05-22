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

        # chiavi MOD
        self.encrypt_A = 0
        self.decrypt_A = 0
        self.p = 0
        self.fp = self.p - 1

        # controllo lunghezza chunk, se e piu corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < self.chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(self.chunk_len)

        #ottengo i chunk in intero
        for chunk in self.chunks:
            self.intchunks.append(int(chunk, 2))

    def signature_encrypt(self, privkey, mod):
        cryptedchunks = []
        for chunk in self.intchunks:
            cryptedchunks.append(pow(chunk, privkey, mod))
        return cryptedchunks

    def signature_decrypt(self, pubkey, mod):
        decryptedchunks = []
        for chunk in self.intchunks:
            decryptedchunks.append(pow(chunk, pubkey, mod))
        return decryptedchunks