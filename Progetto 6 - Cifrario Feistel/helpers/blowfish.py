from helpers.key_gen import gen_key32, toBinary, toBinary32
from helpers.utils import xor_func


class Blowfish:
    encrypted = []
    decrypted = []

    def __init__(self, out_lck, chunks, key):

        self.chunks = chunks
        self.keys = []
        self.p_boxes = []
        chunk_len = 64

        # creo chiavi
        self.keys = gen_key32(out_lck, key)
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
        chunk1 = xr + xl
        return chunk1

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
        chunk1 = xr + xl
        return chunk1

    def __round_func(self, xl):

        a1 = xl[24:].zfill(32)  # ultime 8
        b1 = xl[16:-8].zfill(32)  # penultime 8
        c1 = xl[8:-16].zfill(32)
        d1 = xl[:-24].zfill(32) # prime 8
        a = int(a1,2)
        b = int(b1, 2)
        ab1 = a + b
        ab = toBinary32(ab1)
        abc1 = xor_func(ab, c1)
        abc = int(abc1,2)
        d = int(d1,2)
        abcd = abc + d
        num = toBinary32(abcd)

        return num
