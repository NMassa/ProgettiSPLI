from helpers.utils import toBinary8

from helpers.utils import output

class Cipher:
    file = None
    keys = None
    chunks = None
    encrypted = []
    decrypted = []

    def __init__(self, out_lck, chunks, chunklen):
        self.keys = []
        self.chunks = chunks
        self.intchunks = []
        self.chunk_len = chunklen

        self.p = 0
        self.q = 0
        self.n = 0
        self.fn = 0
        self.e = 0
        self.d = 0

        #paddo i chunk
        for index in range(0, len(self.chunks)):
            if len(self.chunks[index]) < self.chunk_len:
                self.chunks[index] = self.chunks[index].zfill(self.chunk_len)

        # ottengo i chunk in intero
        for chunk in self.chunks:
            self.intchunks.append(int(chunk, 2))

    def encrypt_and_decrypt(self, key, mod):
        chunks = []
        for chunk in self.intchunks:
            chunks.append(pow(chunk, key, mod))
        return chunks


def check_controller(e, d, n):
    # controllo che le chiavi generate a 8 bit funzionino
    m = 255
    c = pow(m, e, n)
    m1 = pow(c, d, n)
    if m == m1:
        return 1
    else:
        return 0

def bruteforce(out_lck, chunks, mod, d):
    stringa = ['89504e470d0a1a0a', 'ffd8ffe000104a46', '424df640000', '89504e47da1aa', '47496383961181', '474946',
               'FFFB']
    out = 0
    pippo = 0
    key = 0
    decryptedchunks = []


    for i in range(1, 1000):
        if pippo == 0:
            new_chunks = ''
            # prendo primi 8 chunks da 8 bit
            for chunk in chunks[0:8]:
                # trasformo chunk in intero e applico modulo
                new = (toBinary8(pow(int(chunk, 2), i, int(mod))))
                new_chunks = new_chunks + new

            for a in stringa:
                check = bin(int(a, 16))[2:]

                if new_chunks.find(check) != -1:

                    if a == '89504e470d0a1a0a':
                        output(out_lck, '\ndetect format file: PNG')
                        out = 1
                    elif a == 'ffd8ffe000104a46':
                        output(out_lck, '\ndetect format file: JPG')
                        out = 2
                    elif a == '424df640000':
                        output(out_lck, '\ndetect format file: BMP')
                        out = 3
                    elif a == '474946':
                        output(out_lck, '\ndetect format file: GIF')
                        out = 4
                    elif a == 'FFFB':
                        output(out_lck, '\ndetect format file: MP3')
                        out = 5
                    key = i
                    if i == d:
                        pippo = 1
                        print("\nKey found : \n", key)
                        break
        else:
            break

    for chunk in chunks:
        # trasformo chunk in intero e applico modulo
        decryptedchunks.append(toBinary8(pow(int(chunk, 2), key, int(mod))))

    return out, decryptedchunks
