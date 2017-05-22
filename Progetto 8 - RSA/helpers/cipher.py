from helpers import utils

class Cipher:
    file = None
    keys = None
    chunks = None
    encrypted = []
    decrypted = []

    def __init__(self, out_lck, chunks, key):
        self.keys = []
        self.chunks = chunks

        self.chunk_len = 128

        self.keys = key

        # chiavi MOD
        self.encrypt_A = 0
        self.decrypt_A = 0
        self.p = 0
        self.fp = self.p - 1
        # controllo lunghezza chunk, se e piu corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < self.chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(self.chunk_len)


    def encryptMOD(self, n, number):
        self.p = 0
        #self.p = utils.calculateP(number)
        self.p = 257
        self.encrypt_A = utils.calculateEncryptionKey(n, self.p)
        towrite = self.algorithmMOD(self.encrypt_A)

        return towrite

    def decryptMOD(self):

        fp = self.p - 1
        self.decrypt_A = utils.modinv(self.encrypt_A, fp)
        towrite = self.algorithmMOD(self.decrypt_A)

        return towrite

    def algorithmMOD(self, key):

        new_chunks = []

        for c in self.chunks:  # for each chunk
            c_int = int(c, 2)
            c = utils.mod(c_int, key, self.p)
            new_chunks.append(utils.toBinary8(c))

        return new_chunks
