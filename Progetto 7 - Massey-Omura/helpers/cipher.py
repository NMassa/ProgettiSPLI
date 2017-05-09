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
        chunk_len = 64

        self.keys = key
        #self.key = key

        # controllo lunghezza chunk, se è più corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(chunk_len)

    def encryptXOR(self):
        towrite = self.algorithmXOR()
        return towrite

    def decryptXOR(self):
        towrite = self.algorithmXOR()
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

        keys = utils.gen_keys(self.key, num_keys)  # generate keys from K

        new_chunks = []

        i = 0

        for m in self.chunks:

            m = utils.multiply(int(m, 2), int(utils.toBinary64(keys[i]), 2))
            new_chunks.append(utils.toBinary64(m))
            i += 1

        return new_chunks

    def algorithmDiv(self):

        num_keys = len(self.chunks)  # una chiave per ogni chunk

        keys = utils.gen_keys(self.key, num_keys)  # generate keys from K

        new_chunks = []

        i = 0

        for m in self.chunks:
            m = utils.div(int(m, 2),int(utils.toBinary64(keys[i]), 2))
            new_chunks.append(utils.toBinary64(m))
            i += 1

        return new_chunks

    def algorithmAdd(self):

        num_keys = len(self.chunks)  # una chiave per ogni chunk

        keys = utils.gen_keys(self.key, num_keys)  # generate keys from K

        new_chunks = []

        i = 0

        for m in self.chunks:
            m = utils.sum(int(utils.toBinary64(keys[i]), 2), int(m, 2))
            new_chunks.append(utils.toBinary64(m))
            i += 1

        return new_chunks

    def algorithmDiff(self):

        num_keys = len(self.chunks)  # una chiave per ogni chunk

        keys = utils.gen_keys(self.key, num_keys)  # generate keys from K

        new_chunks = []

        i = 0

        for m in self.chunks:
            m = utils.diff(int(m, 2), int(utils.toBinary64(keys[i]), 2))
            new_chunks.append(utils.toBinary64(m))
            i += 1

        return new_chunks