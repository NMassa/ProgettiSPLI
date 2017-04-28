from helpers.key_gen import *
from helpers.utils import *


class cipher:
    def __int__(self, file, key):

        self.file = file
        self.key = key
        kes = []
        chunk_len = 8

        # creo chiavi
        keys = gen_keys(key)
        # prendo chunks di lunghezza chunk_len
        self.chunks = get_chunks("../files/Periodic-Table.png", chunk_len)
        print(self.chunks)

        # controllo lunghezza chunk, se è più corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(32)

    def encode(self):

        chunks_encode = []
        for chunk in self.chunks:
            # for i in range (0,2):
            # TODO: applico funzione al chunk con keys[i]
            # inverto chunk dx con sx
            chunks_encode.append(chunk[4:8] + chunk[0:4])
