from helpers.utils import output, calculateEncryptionKey, egcd
import math, rsa

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

    def generate_keys(self):
        (pub_key, priv_key) = rsa.newkeys(self.chunk_len)
        self.p = priv_key['p']
        self.q = priv_key['q']

        self.n = self.p * self.q
        self.fn = (self.p - 1) * (self.q - 1)
        self.e = calculateEncryptionKey(self.n, self.fn)
        gcd, x, y = egcd(self.e, self.fn)
        if gcd != 1:
            output("no d key exist")
        else:
            self.d = x % self.fn
