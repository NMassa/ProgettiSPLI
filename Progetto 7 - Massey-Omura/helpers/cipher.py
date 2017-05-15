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
        self.chunk_len = DIM_BLOCK

        self.keys = key
        #self.key = key

        # chiavi MOD
        self.encrypt_A = 0
        self.decrypt_A = 0
        self.p = 0
        self.fp = self.p - 1

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

    def algorithmXOR(self):

        new_chunks = []

        i = 0
        for c in self.chunks:  # for each chunk

            c = utils.xor_func(c, utils.toBinary64(self.keys[i]))  # primo chunk con prima chiave, secondo chunk con seconda chiave, ecc
            new_chunks.append(c)
            i = i + 1
        return new_chunks

    def algorithmMultiply(self):

        num_keys = len(self.chunks)  # una chiave per ogni chunk

        keys = utils.gen_keys2(self.key, num_keys)  # generate keys from K

        new_chunks = []

        i = 0

        for m in self.chunks:
            m = utils.mul(int(m, 2), int(utils.toBinary8(keys[i]), 2))
            new_chunks.append(utils.toBinary32(m))
            i += 1

        return new_chunks

    def algorithmDiv32_to_16(self):

        num_keys = len(self.chunks)  # una chiave per ogni chunk

        keys = utils.gen_keys2(self.key, num_keys)  # generate keys from K

        new_chunks = []

        i = 0

        for m in self.chunks:
            m = utils.div32_to_16(int(m, 2), int(utils.toBinary64(keys[i]), 2))
            new_chunks.append(utils.toBinary32(m))
            i += 1

        return new_chunks

    def algorithmDiv16_to_8(self):

        num_keys = len(self.chunks)  # una chiave per ogni chunk

        keys = utils.gen_keys2(self.key, num_keys)  # generate keys from K

        new_chunks = []

        i = 0

        for m in self.chunks:
            m = utils.div16_to_8(int(m, 2), int(utils.toBinary64(keys[i]), 2))
            new_chunks.append(utils.toBinary32(m))
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

        #keys = utils.gen_keys(self.keys , num_keys)

        new_chunks =[]

        i=0
        #print (self.chunks)
        while i < num_keys:
            #print (self.keys[i])
            leftS = utils.sL(self.chunks[i],int(self.keys[i]))
            print("lefts"+ str(int(leftS,2)))
            new_chunks.append(leftS)

            i +=1

        return new_chunks

    def algorithmShiftR(self):
        num_keys = len(self.keys)
        #keys = utils.gen_keys(self.key,num_keys)

        new_chunks =[]
        i=0
        while i < num_keys:
            #print (self.keys[i])
            rightS = utils.sR(self.chunks[i],int(self.keys[i]))
            print("rightS"+ str(int(rightS,2)))
            new_chunks.append(rightS)

            i += 1
        return new_chunks

    def encryptMOD(self, n, number):

        self.p = 0

        #self.p = utils.calculateP(number)
        self.p = number
        self.encrypt_A = utils.calculateEncryptionKey(n, self.p)
        #print("eA: " + str(self.encrypt_A))
        towrite = self.algorithmMOD(self.encrypt_A)

        return towrite

    def decryptMOD(self):

        fp = self.p - 1
        self.decrypt_A = utils.modinv(self.encrypt_A, fp)
        #print("dA: " + str(self.decrypt_A))
        towrite = self.algorithmMOD(self.decrypt_A)

        return towrite

    def algorithmMOD(self, key):

        new_chunks = []

        for c in self.chunks:  # for each chunk
            c_int = int(c, 2)
            c = utils.mod(c_int, key, self.p)
            new_chunks.append(utils.toBinary8(c))
            #print(utils.toBinary8(c))

        return new_chunks

    def set_chunks(self, chunks):

        self.chunks = chunks

        # controllo lunghezza chunk, se e piu corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < self.chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(self.chunk_len)
