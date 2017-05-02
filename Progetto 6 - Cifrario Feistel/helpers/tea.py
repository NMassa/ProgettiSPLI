from bitarray import bitarray
from bitstring import BitArray

from helpers.key_gen import gen_16key32, toBinary
from helpers.utils import get_chunks, toBinary32, xor_func


class mybitarray(bitarray):
    def __lshift__(self, count):
        return self[count:] + type(self)('0') * count
    def __rshift__(self, count):
        return type(self)('0') * count + self[:-count]
    def __repr__(self):
        return "{}('{}')".format(type(self).__name__, self.to01())


class teaCipher:
    file = None
    keys = None
    chunks = None
    encrypted = []
    decrypted = []


    def __init__(self, out_lck, file, key):
        self.file = file
        self.keys = []
        chunk_len = 64

        self.keys = gen_16key32(out_lck, key)

        self.chunks = get_chunks("files/" + file, chunk_len)

        if len(self.chunks[len(self.chunks) - 1]) < chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(chunk_len)


    def teaencrypt(self):
        # encrypt
        delta = 30
        start = 0
        stop = 4
        for chunk in self.chunks:
            if stop != len(self.keys):
                chunk = self.encrypt_chunk(chunk[:int(len(chunk) / 2)], chunk[int(len(chunk) / 2):],
                                           self.keys[start:stop], delta)
                start += 4
                stop += 4

                self.encrypted.append(chunk)

    def teadecrypt(self):
        # encrypt
        delta = 30
        start = 0
        stop = 4
        for chunk in self.chunks:
            if stop != len(self.keys):
                chunk = self.decrypt_chunk(chunk[int(len(chunk) / 2):], chunk[:int(len(chunk) / 2)],
                                           self.keys[start:stop], delta)
                start += 4
                stop += 4

                self.decrypted.append(chunk)
        file = open("received/tea.jpg", "wb")
        for element in self.decrypted:
            file.write(bytes(element.encode('utf-8')))
        file.close()

    def encrypt_chunk(self, leftchunk, rightchunk, keys, delta):
        lol = 100
        if len(keys) > 0:
            lba = mybitarray(leftchunk)
            rba = mybitarray(rightchunk)

            lshift = rba.__lshift__(4)
            rshift = rba.__rshift__(5)

            bitkey0 = bitarray(keys[0])
            bitkey1 = bitarray(keys[1])
            bitsum = bitarray(toBinary32(delta))

            sum0 = toBinary32(BitArray(lshift).uint + BitArray(bitkey0).uint)
            sum1 = toBinary32(BitArray(rshift).uint + BitArray(bitkey1).uint)
            sum2 = toBinary32(BitArray(rba).uint + BitArray(bitsum).uint)

            xor1 = xor_func(sum0, sum1)
            xoresult = xor_func(xor1, sum2)

            bitxoresult = bitarray(xoresult)
            sum = toBinary32(BitArray(bitxoresult).uint + BitArray(lba).uint)
            keys.pop(0)
            keys.pop(0)
            self.encrypt_chunk(rightchunk, sum, keys, str(lol+int(delta)))
        elif len(keys) == 0:
            return True
        return (leftchunk + rightchunk)

    def decrypt_chunk(self, leftchunk, rightchunk, keys, delta):
        lol = 100
        if len(keys) > 0:
            lba = mybitarray(leftchunk)
            rba = mybitarray(rightchunk)

            lshift = rba.__lshift__(4)
            rshift = rba.__rshift__(5)

            bitkey0 = bitarray(keys[0])
            bitkey1 = bitarray(keys[1])
            bitsum = bitarray(toBinary32(delta))

            sum0 = toBinary32(BitArray(lshift).uint - BitArray(bitkey0).uint)
            sum1 = toBinary32(BitArray(rshift).uint - BitArray(bitkey1).uint)
            sum2 = toBinary32(BitArray(rba).uint - BitArray(bitsum).uint)

            xor1 = xor_func(sum0, sum1)
            xoresult = xor_func(xor1, sum2)

            bitxoresult = bitarray(xoresult)
            sum = toBinary32(BitArray(bitxoresult).uint - BitArray(lba).uint)
            keys.pop(0)
            keys.pop(0)
            self.decrypt_chunk(rightchunk, sum, keys, str(lol - int(delta)))
        elif len(keys) == 0:
            return True
        return (leftchunk + rightchunk)