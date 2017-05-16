from helpers import utils
import random

global DIM_BLOCK
DIM_BLOCK = 8

class Cipher:
    file = None
    keys = None
    chunks = None
    encrypted = []
    decrypted = []

    def __init__(self, out_lck, chunks, key):
        self.keys = []
        self.chunks = chunks

        # TODO da modificare
        self.chunk_len = 64

        self.keys = key
        #self.key = key

        # chiavi MOD
        self.encrypt_A = 0
        self.decrypt_A = 0
        self.p = 0
        self.fp = self.p - 1
        troia = self.chunks[len(self.chunks) - 1]
        # controllo lunghezza chunk, se e piu corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < self.chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(self.chunk_len)

    def encryptXOR(self):
        towrite = self.algorithmXOR()
        return towrite

    def decryptXOR(self):
        towrite = self.algorithmXOR()
        return towrite

    def encryptShift(self):
        towrite = self.algorithmShiftL()
        return towrite

    def decryptShift(self):
        towrite = self.algorithmShiftR()
        return towrite

    def encryptMul8(self):
        towrite = self.algorithmMultiply8_to_16()
        return towrite

    def encryptMul16(self):
        towrite = self.algorithmMultiply16_to_32()
        return towrite

    def decryptMul32(self):
        towrite = self.algorithmDiv32_to_16()
        return towrite

    def decryptMul16(self):
        towrite = self.algorithmDiv16_to_8()
        return towrite

    def algorithmXOR(self):

        new_chunks = []

        i = 0
        for c in self.chunks:  # for each chunk

            c = utils.xor_func(c, utils.toBinary64(self.keys[i]))  # primo chunk con prima chiave, secondo chunk con seconda chiave, ecc
            new_chunks.append(c)
            i = i + 1
        return new_chunks

    def algorithmMultiply8_to_16(self):

        new_chunks = []

        i = 0

        for m in self.chunks:
            m = utils.mul8_to_16(m, utils.toBinary64(self.keys[i]))
            new_chunks.append(m)
            i += 1

        return new_chunks

    def algorithmMultiply16_to_32(self):

        new_chunks = []

        i = 0

        for m in self.chunks:
            m = utils.mul16_to_32(m, utils.toBinary64(self.keys[i]))
            new_chunks.append(m)
            i += 1

        return new_chunks

    def algorithmDiv32_to_16(self):

        new_chunks = []

        i = 0

        for m in self.chunks:
            m = utils.div32_to_16(m, utils.toBinary64(self.keys[i]))
            new_chunks.append(m)
            i += 1

        return new_chunks

    def algorithmDiv16_to_8(self):

        new_chunks = []

        i = 0

        for m in self.chunks:
            m = utils.div16_to_8(m, utils.toBinary64(self.keys[i]))
            new_chunks.append(m)
            i += 1

        return new_chunks

    def algorithmAdd(self):

        new_chunks = []
        i = 0

        for m in self.chunks:
            m = utils.sum(int(utils.toBinary64(self.keys[i]), 2), int(m, 2))
            new_chunks.append(utils.toBinary64(m))
            i += 1

        return new_chunks

    def algorithmDiff(self):

        new_chunks = []
        i = 0

        for m in self.chunks:
            m = utils.diff(int(m, 2), int(utils.toBinary64(self.keys[i]), 2))
            new_chunks.append(utils.toBinary64(m))
            i += 1

        return new_chunks

    def algorithmShiftL(self):

        num_keys = len(self.keys)

        new_chunks =[]

        i=0
        while i < num_keys:
            leftS = utils.sL(self.chunks[i],int(self.keys[i]))
            new_chunks.append(leftS)
            i +=1
        return new_chunks

    def algorithmShiftR(self):
        num_keys = len(self.keys)

        new_chunks =[]
        i=0
        while i < num_keys:
            rightS = utils.sR(self.chunks[i], int(self.keys[i]))
            new_chunks.append(rightS)

            i += 1
        return new_chunks

    def encryptMOD(self, n, number):

        self.p = number
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

    def set_chunks(self, chunks):

        self.chunks = chunks

        # controllo lunghezza chunk, se e piu corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < self.chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(self.chunk_len)
