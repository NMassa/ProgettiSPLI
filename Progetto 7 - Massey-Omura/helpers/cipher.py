import utils


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

        # controllo lunghezza chunk, se e piu corta metto "0"
        if len(self.chunks[len(self.chunks) - 1]) < chunk_len:
            self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(chunk_len)

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
        print new_chunks
        return new_chunks

    def algorithmShiftR(self):
        num_keys = len(self.keys)
        #keys = utils.gen_keys(self.key,num_keys)

        new_chunks =[]
        i=0
        print (self.chunks)
        while i < num_keys:
            #print (self.keys[i])
            rightS = utils.sR(self.chunks[i],int(self.keys[i]))
            print("rightS"+ str(int(rightS,2)))
            new_chunks.append(rightS)

            i +=1
        print new_chunks
        return new_chunks
