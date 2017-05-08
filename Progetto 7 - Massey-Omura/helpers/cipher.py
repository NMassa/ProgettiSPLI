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
        lol = len(self.chunks[len(self.chunks) - 1])
        # controllo lunghezza chunk, se è più corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(chunk_len)

    def encryptXOR(self, key):
        self.algorithmXOR(self.chunks, key)

    def decryptXOR(self, key):
        towrite = self.algorithmXOR(self.chunks, key)
        return towrite

    def algorithmXOR(self, chunks, key):

        num_keys = len(chunks)  # una chiave per ogni chunk

        keys = utils.gen_keys(key, num_keys)  # generate keys from K

        new_chunks = []

        i = 0
        for c in chunks:  # for each chunk
            c = utils.xor_func(c, utils.toBinary64(keys[i]))  # primo chunk con prima chiave, secondo chunk con seconda chiave, ecc
            new_chunks.append(c)
            i = i + 1

        return new_chunks


