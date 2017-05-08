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

        #self.keys = key
        self.key = key

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

        num_keys = len(self.chunks)  # una chiave per ogni chunk

        keys = utils.gen_keys(self.key, num_keys)  # generate keys from K

        new_chunks = []

        i = 0
        for c in self.chunks:  # for each chunk
            c = utils.xor_func(c, utils.toBinary64(keys[i]))  # primo chunk con prima chiave, secondo chunk con seconda chiave, ecc
            new_chunks.append(c)
            i = i + 1

        return new_chunks


