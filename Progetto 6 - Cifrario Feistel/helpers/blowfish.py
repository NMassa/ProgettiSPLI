from helpers.key_gen import *
from helpers.utils import *


class Blowfish:
    encrypted = []
    decrypted = []

    def __init__(self, out_lck, chunks, key):

        self.chunks = chunks
        self.keys = []
        self.p_boxes = []
        self.p_boxes_reversed = []
        chunk_len = 64

        # creo chiavi
        #self.keys = gen_8key32(out_lck, key)
        #self.p_boxes = self.keys
        self.p_boxes = key
        self.p_boxes_reversed = self.p_boxes[::-1]

        # controllo lunghezza chunk, se è più corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(chunk_len)

    def encrypt(self):
        for chunk in self.chunks:
            chunk = self.cipher(chunk)
            self.encrypted.append(chunk)

    def decrypt(self):
        for chunk in self.chunks:
            chunk = self.decipher(chunk)
            self.decrypted.append(chunk)

    def decrypt_brute_force(self):
        stringa = ['89504e470d0a1a0a', 'ffd8ffe000104a46', '424df640000', '89504e47da1aa', '47496381',
                   '474946']
        pippo = True
        stop = True  # variabile che con vero non mi esamina tutto il file
        index = 0
        out = 0

        for chunk in self.chunks:
            if pippo:
                chunk = self.decipher(chunk)
                if index == 0:
                    for i in stringa:
                        check = bin(int(i, 16))[2:]
                        if chunk.find(check) != -1:
                            if i == '89504e470d0a1a0a':
                                print('detect format file: PNG')
                                out = 1
                            elif i == 'ffd8ffe000104a46':
                                print('detect format file: JPG')
                                out = 2
                            elif i == '424df640000':
                                print('detect format file: BMP')
                                out = 3
                            elif i == '474946':
                                print('detect format file: GIF')
                                out = 4
                            pippo = True
                            # indico che posso andare avanti con il file
                            stop = False
                            break
                        else:
                            # print('non trovato')
                            pippo = False
                    index = 1

            if not stop:
                self.decrypted.append(chunk)
            else:
                break

        return out


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
        chunk1 = xl + xr
        return chunk1

    def decipher(self, chunk):

        xl = chunk[:int(len(chunk) / 2)]
        xr = chunk[int(len(chunk) / 2):]
        for i in range(6):
            xl = xor_func(xl, self.p_boxes_reversed[i])
            xr = xor_func(self.__round_func(xl), xr)
            xl, xr = xr, xl
        xl, xr = xr, xl
        xr = xor_func(xr, self.p_boxes_reversed[6])
        xl = xor_func(xl, self.p_boxes_reversed[7])
        chunk1 = xl + xr
        return chunk1

    def __round_func(self, xl):
        a = xl[0:8].zfill(32)
        b = xl[8:16].zfill(32)
        c = xl[16:24].zfill(32)
        d = xl[24:32].zfill(32)

        int_a = int(a,2)
        int_b = int(b,2)
        ab = toBinary32(int_a + int_b)
        abc = xor_func(ab, c)
        int_abc = int(abc, 2)
        abcd = toBinary32(int_abc + int(d, 2))

        return abcd