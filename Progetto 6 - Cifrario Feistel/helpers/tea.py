#!/usr/bin/python
"""
Tiny Encryption Algorithm (TEA) implementation
----------------------------------------------
The encrypt/decrypt functions do just that for a single block (2
4-byte unsigned integers).
The encipher/decipher functions act on a string, breaking it into
blocks and encrypt-/decrypting.
All functions take a key parameter which is expected to be 4 unsigned
4-byte integers.
CAVEAT: Encipher right-pads with zero bytes which are stripped off in
decipher, so a message ending in zero bytes will become garbled.
Corollary: there's an assumption that these functions will be used to
encipher plain, readable text.
See http://en.wikipedia.org/wiki/Tiny_Encryption_Algorithm for reference
"""

import struct

DELTA = 0x9e3779b9  # key schedule constant


# Helper for unsigned long math
def ul(v):
    return v & 0xFFFFFFFF


def encrypt(v0, v1, key, rounds=32):
    assert len(key) == 4
    sum = 0
    for i in range(rounds):
        v0 = ul(v0 + ((v1 << 4 ^ v1 >> 5) + v1 ^ sum + key[sum & 3]))
        sum = ul(sum + DELTA)
        v1 = ul(v1 + ((v0 << 4 ^ v0 >> 5) + v0 ^ sum + key[sum >> 11 & 3]))
    return v0, v1


def decrypt(v0, v1, key, rounds=32):
    assert len(key) == 4
    sum = ul(DELTA * rounds)
    for i in range(rounds):
        v1 = ul(v1 - ((v0 << 4 ^ v0 >> 5) + v0 ^ sum + key[sum >> 11 & 3]))
        sum = ul(sum - DELTA)
        v0 = ul(v0 - ((v1 << 4 ^ v1 >> 5) + v1 ^ sum + key[sum & 3]))
    return v0, v1


def encipher(s, key):
    """TEA-encipher a string"""
    assert struct.calcsize('I') == 4
    s = s.ljust(8 * int((len(s) + 7) / 8), bytes('\x00'.encode('utf-8')))  # pad with 0's
    u = struct.unpack('%dI' % (len(s) / 4), s)
    e = [encrypt(u[i], u[i + 1], key) for i in range(len(u))[::2]]
    return ''.join([struct.pack('2I', ee, ef) for ee, ef in e])


def decipher_raw(s, key):
    """TEA-decipher a raw string"""
    assert struct.calcsize('I') == 4
    assert len(s) % 8 == 0, len(s)
    u = struct.unpack('%dI' % (len(s) / 4), s)
    e = [decrypt(u[i], u[i + 1], key) for i in range(len(u))[::2]]
    return ''.join([struct.pack('2I', ee, ef) for ee, ef in e])


def decipher(s, key):
    """TEA-decipher a readable string"""
    return decipher_raw(s, key).rstrip('\x00')


def main():
    """Usage: tea.py [OPTS] [KEY] [INFILE [OUTFILE]]
  OPTS:
    -d         Decipher (default is to encipher)
    -h         Ciphertext is expressed in hex format (default for tty or with -i)
    -t         Ciphertext is expressed as literal text (default otherwise)
    -i INPUT   Input specified is used instead of INFILE or stdin
    -P PROMPT  Specify text prompt for password request (e.g., a hint)
  KEY:
    -k KEY      A hexadecimal key string of length exactly 16
    -p PASSWORD Password is used to generate an md5 hash, which is used as key
    -f KEYFILE  A key file of length exactly 16
    If no key, keyfile or password is provided, a password is read from stdin.
    This requires that INFILE be specified or -i option is used.
  INFILE
    Path to file containing plain or cipher text
  OUTFILE
    Path to file to write
  If either FILE argument is omitted, stdin/stdout is used."""

    def usage(msg=None):
        if msg: print >> sys.stderr, 'Error:', msg
        print >> sys.stderr, main.__doc__
        sys.exit(-1)

    cipher = encipher
    hex = None
    key = None
    password = None
    message = None
    prompt = "Password: "
    import sys, getopt
    opts, args = getopt.getopt(sys.argv[1:], "dhi:p:P:tk:")
    for o, a in opts:
        if o == '-d':
            cipher = decipher
        elif o == '-h':
            hex = True
        elif o == '-t':
            hex = False
        elif o == '-p':
            password = a
        elif o == '-k':
            key = a
        elif o == '-f':
            key = open(a, 'rb').read()
        elif o == '-i':
            message = a
        elif o == '-P':
            prompt = a
        else:
            usage()
            if (len(args) < 1) or (len(args[0]) != 16):
                usage
    if not (key or password or args or message): usage()
    if not key:
        import getpass, hashlib
        if not password:
            password = getpass.getpass(prompt)
        key = hashlib.md5(password.encode('utf-8')).digest()[:16]
    if len(key) != 16:
        usage('key length must be 16')
    key = struct.unpack('4I', key)

    inputisatty = True
    if not message:
        input = args and open("piedpiper.jpg", 'rb') or sys.stdin
        message = input.read()
        inputisatty = input.isatty()
        input.close()

    output = args and open("asd.jpg", 'wb') or sys.stdout

    if (cipher == decipher) and ((hex == True) or
                                     ((hex == None) and inputisatty)):
        message = message.decode('hex')
    result = cipher(message, key)
    if (cipher == encipher) and ((hex == True) or
                                     ((hex == None) and output.isatty())):
        result = result.encode('hex')
    output.write(result)


if __name__ == "__main__":
    main()




#
# from bitarray import bitarray
# from bitstring import BitArray
#
# from helpers.key_gen import gen_16key32, toBinary
# from helpers.utils import get_chunks, toBinary32, xor_func
#
#
# class mybitarray(bitarray):
#     def __lshift__(self, count):
#         return self[count:] + type(self)('0') * count
#     def __rshift__(self, count):
#         return type(self)('0') * count + self[:-count]
#     def __repr__(self):
#         return "{}('{}')".format(type(self).__name__, self.to01())
#
#
# class teaCipher:
#     file = None
#     keys = None
#     chunks = None
#     encrypted = []
#     decrypted = []
#
#
#     def __init__(self, out_lck, file, key):
#         self.file = file
#         self.keys = []
#         chunk_len = 64
#
#         self.keys = gen_16key32(out_lck, key)
#
#         self.chunks = get_chunks("files/" + file, chunk_len)
#
#         if len(self.chunks[len(self.chunks) - 1]) < chunk_len:
#             self.chunks[len(self.chunks) - 1] = self.chunks[len(self.chunks) - 1].zfill(chunk_len)
#
#
#     def teaencrypt(self):
#         # encrypt
#         delta = 30
#         start = 0
#         stop = 4
#         for chunk in self.chunks:
#             if stop != len(self.keys):
#                 chunk = self.encrypt_chunk(chunk, self.keys[start:stop], delta)
#                 start += 4
#                 stop += 4
#
#                 self.encrypted.append(chunk)
#
#     def teadecrypt(self):
#         # encrypt
#         delta = 30
#         start = 0
#         stop = 4
#         for chunk in self.chunks:
#             if stop != len(self.keys):
#                 chunk = self.decrypt_chunk(chunk, self.keys[start:stop], delta)
#                 start += 4
#                 stop += 4
#
#                 self.decrypted.append(chunk)
#         file = open("received/tea.jpg", "wb")
#         for element in self.decrypted:
#             file.write(bytes(element.encode('utf-8')))
#         file.close()
#
#     def encrypt_chunk(self, chunk, keys, delta):
#         leftchunk = chunk[int(len(chunk) / 2):]
#         rightchunk = chunk[:int(len(chunk) / 2)]
#
#         sumation = 100
#
#         lba = mybitarray(leftchunk)
#         rba = mybitarray(rightchunk)
#
#         sum0 = toBinary32(BitArray(rba.__lshift__(4)).uint + BitArray(bitarray(keys[0])).uint)
#         sum1 = toBinary32(BitArray(rba.__rshift__(5)).uint + BitArray(bitarray(keys[1])).uint)
#         sum2 = toBinary32(BitArray(rba).uint + BitArray(bitarray(toBinary32(delta))).uint)
#
#         xor1 = xor_func(sum0, sum1)
#         xoresult = xor_func(xor1, sum2)
#
#         bitxoresult = bitarray(xoresult)
#         midsum = toBinary32(BitArray(bitxoresult).uint + BitArray(lba).uint)
#
#         sum3 = toBinary32(BitArray(mybitarray(midsum).__lshift__(4)).uint + BitArray(bitarray(keys[2])).uint)
#         sum4 = toBinary32(BitArray(mybitarray(midsum).__rshift__(5)).uint + BitArray(bitarray(keys[3])).uint)
#         sum5 = toBinary32(BitArray(mybitarray(midsum)).uint + BitArray(bitarray(toBinary32(delta))).uint)
#
#         xor2 = xor_func(sum3, sum4)
#         xoresult = xor_func(xor2, sum5)
#
#         finalsum = toBinary32(BitArray(xoresult).uint + BitArray(rba).uint)
#         return finalsum
#
#     def decrypt_chunk(self, leftchunk, rightchunk, keys, delta):
#         lol = 100
#         if len(keys) > 0:
#             lba = mybitarray(leftchunk)
#             rba = mybitarray(rightchunk)
#
#             lshift = rba.__lshift__(4)
#             rshift = rba.__rshift__(5)
#
#             bitkey0 = bitarray(keys[0])
#             bitkey1 = bitarray(keys[1])
#             bitsum = bitarray(toBinary32(delta))
#
#             sum0 = toBinary32(BitArray(lshift).uint - BitArray(bitkey0).uint)
#             sum1 = toBinary32(BitArray(rshift).uint - BitArray(bitkey1).uint)
#             sum2 = toBinary32(BitArray(rba).uint - BitArray(bitsum).uint)
#
#             xor1 = xor_func(sum0, sum1)
#             xoresult = xor_func(xor1, sum2)
#
#             bitxoresult = bitarray(xoresult)
#             sum = toBinary32(BitArray(bitxoresult).uint - BitArray(lba).uint)
#             keys.pop(0)
#             keys.pop(0)
#             self.decrypt_chunk(rightchunk, sum, keys, str(lol - int(delta)))
#         elif len(keys) == 0:
#             return True
#         return (leftchunk + rightchunk)
