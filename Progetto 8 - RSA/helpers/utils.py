from helpers.cipher import *
from helpers.connection import UDPclient
from bitarray import bitarray
from random import randint
import pyprimes
import math
import random


def recvall(socket, chunk_size):
    data = socket.recvfrom(chunk_size)  # Lettura di chunk_size byte dalla socket
    actual_length = len(data)

    # Se sono stati letti meno byte di chunk_size continua la lettura finche non si raggiunge la dimensione specificata
    while actual_length < chunk_size:
        new_data = socket.recvfrom(chunk_size - actual_length)
        actual_length += len(new_data)
        data += new_data

    return data


def output(lock, message):
    lock.acquire()
    print(message)
    lock.release()


def loop_menu(lock, header, options):
    action = None
    while action is None:
        output(lock, header)

        for idx, o in enumerate(options, start=1):
            output(lock, str(idx) + ": " + o + "")

        try:
            action = input()
        except SyntaxError:
            action = None

        if not action:
            output(lock, "Please select an option")
            action = None
        elif action == 'e':
            return None
        else:
            try:
                selected = int(action)
            except ValueError:
                output(lock, "A number is required")
                continue
            else:
                if selected > len(options):
                    output(lock, "Option " + str(selected) + " not available")
                    action = None
                    continue
                else:
                    return selected


def loop_input(lock, header):
    var = None
    while var is None:
        output(lock, header)

        try:
            var = input()
        except ValueError:
            var = None

        if not var:
            output(lock, "Type something!")
            var = None
        elif var == 'e':
            return None
        else:
            return var


def loop_int_input(lock, header):
    var = None
    while var is None:
        output(lock, header)

        try:
            var = input()
        except ValueError:
            var = None

        if not var:
            output(lock, "Type something!")
            var = None
        elif var == 'e':
            return None
        else:
            try:
                selected = int(var)
            except ValueError:
                output(lock, "A number is required")
                continue
            else:
                return selected


def get_chunks(file, len):
    f = open(file, "rb")
    chunks = []
    chunk = ''
    n = 0
    while (1):
        byte = f.read(1)
        if not byte:
            if chunk != '':
                chunks.append(chunk)
            break
        chunk = chunk + format(ord(byte), 'b').zfill(8)
        n = n + 1
        if n == len // 8:  # controllore se voglio chunk piu lunghi
            chunks.append(chunk)
            chunk = ''
            n = 0
    f.close()
    return chunks


def gen_keys(K, num_keys):

    key0 = random.sample(range(0, num_keys), num_keys)
    for element in key0:
        element += int(K)
    keys = []
    for element in key0:
        keys.append(str(element))

    return keys


def gen_keys2(K, num_keys):
    keys = []
    random.seed(int(K))
    for i in range(0, num_keys):
        key = int(K) + random.randint(0, 256)
        if key > 255:
            key = key % 255
        if key == 0:
            key += 1
        keys.append(key)

    return keys


def xor_func(xs, ys):
    return "".join(str(ord(x) ^ ord(y)) for x, y in zip(xs, ys))


def toBinary4(n):
    return ''.join(str(1 & int(n) >> i) for i in range(4)[::-1])


def toBinary8(n):
    return ''.join(str(1 & int(n) >> i) for i in range(8)[::-1])


def toBinary16(n):
    return ''.join(str(1 & int(n) >> i) for i in range(16)[::-1])


def toBinary32(n):
    return ''.join(str(1 & int(n) >> i) for i in range(32)[::-1])


def toBinary64(n):
    return ''.join(str(1 & int(n) >> i) for i in range(64)[::-1])


def toBinary2048(n):
    return ''.join(str(1 & int(n) >> i) for i in range(2048)[::-1])



def send_file_crypt(out_lck, chunks, key, _base, host):
    c = Cipher(out_lck, chunks, key)
    output(out_lck, "Encrypting file...")
    c.encryptXOR(key)
    output(out_lck, "File files")

    data = b''
    for chunk in chunks:
        data += bitarray(chunk).tobytes()

    output(out_lck, "Sending file...")
    UDPclient(out_lck, _base + host, 60000, data)
    output(out_lck, "File Crypted sent")


def send_file_decrypt(out_lck, chunks, key, _base, host):
    c = Cipher(out_lck, chunks, key)
    output(out_lck, "Decrypting file...")
    chunkstowrite = c.decryptXOR(key)
    output(out_lck, "File decrypted.jpg")
    filetowrite = open("received/prova.jpg", "wb+")

    for element in chunkstowrite:
        filetowrite.write(bitarray(element).tobytes())
    filetowrite.close()

    data = b''
    for chunk in c.encrypted:
        data += bitarray(chunk).tobytes()

    output(out_lck, "Sending file...")
    UDPclient(out_lck, _base + host, 60000, data)
    output(out_lck, "File Decrypted sent")


def calculateP(n):
    """
    Prende in ingresso un numero 'n'
    restituisce il numero primo successivo a 'n'
    """
    return pyprimes.next_prime(n)


def calculateEncryptionKey(nthprime, p):
    """
    Prende in ingresso la posizione del numero primo che si vuole calcolare (se passo 10, prendo il decimo numero primo) e 'p'
    restituisce 'e' ovvero un numero primo diverso da p-1 e che sia primo con quest'ultimo
    """
    e = pyprimes.nth_prime(nthprime)
    fp = p-1
    while e == fp or math.gcd(e, fp) != 1:
        nthprime += 2
        e = pyprimes.nth_prime(nthprime)
    return e


def egcd(a, b):
    # https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    x,y, u,v = 0,1, 1,0
    while a != 0:
        q, r = b//a, b % a
        m, n = x-u*q, y-v*q
        b,a, x,y, u,v = a,r, u,v, m,n
    gcd = b
    return gcd, x, y


def mod(M, a, p):
    msg = pow(M, a, p)
    return msg


def modinv(a, m):
    # https://en.wikibooks.org/wiki/Algorithm_Implementation/Mathematics/Extended_Euclidean_algorithm
    gcd, x, y = egcd(a, m)
    if gcd != 1:
        return None  # modular inverse does not exist
    else:
        return x % m

