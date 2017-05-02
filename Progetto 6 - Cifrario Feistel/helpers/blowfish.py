from helpers.key_gen import gen_16key32
from helpers.utils import get_chunks, xor_func


class Blowfish:

    encrypted = []
    decrypted = []


    def __init__(self, out_lck, chunks, key):

        self.chunks = chunks
        self.keys = []
        self.p_boxes = []
        chunk_len = 64

        # creo chiavi
        self.keys = gen_16key32(out_lck, key)
        self.p_boxes = self.keys

        # controllo lunghezza chunk, se è più corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(chunk_len)

    def encrypt(self):
        for chunk in self.chunks:
            chunk = self.cipher(chunk)
            self.encrypted.append(chunk)

    def decrypt(self):
        for chunk in self.encrypted:
            chunk = self.decipher(chunk)
            self.decrypted.append(chunk)

    def cipher(self, chunk):

        xl = chunk[:int(len(chunk) / 2)]
        xr = chunk[int(len(chunk) / 2):]
        for i in range(6):
            xl = xor_func(xl, self.p_boxes[i])
            xr = xor_func(self.__round_func(xl), xr)
            xl, xr = xr, xl
        xl, xr = xr, xl
        xr = xor_func(xr, self.p_boxes[6])
        xl = xor_func(xl, self.p_boxes[7])
        return xl, xr

    def decipher(self, chunk):

        xl = chunk[:int(len(chunk) / 2)]
        xr = chunk[int(len(chunk) / 2):]
        for i in range(7, 1, -1):
            xl = xor_func(xl, self.p_boxes[i])
            xr = xor_func(self.__round_func(xl), xr)
            xl, xr = xr, xl
        xl, xr = xr, xl
        xr = xor_func(xr, self.p_boxes[1])
        xl = xor_func(xl, self.p_boxes[0])
        return xl, xr

    def __round_func(self, xl):

        a = xl[24:]  # ultime 8
        b = xl[16:-8]  # penultime 8
        c = xl[8:-16]
        d = xl[:-24]  # prime 8

        ab = a + b
        abc = xor_func(ab, c)
        abcd = abc + d

        return abcd
