import os, copy, pyprimes, math
import random

import rsa


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


def get_chunks(out_lck, filename, len):
    chunks = []
    for piece in read_in_chunks(filename, len):  # chunks da 128 bytes
        chunks.append(toBinary128(int.from_bytes(piece, byteorder='big')))
    return chunks

def get_chunks_8bit(out_lck, filename, len):
    chunks = []
    for piece in read_in_chunks(filename, len):  # chunks da 1 bytes
        chunks.append(toBinary8(int.from_bytes(piece, byteorder='big')))
    return chunks

def get_chunks_16bit(out_lck, filename, len):
    chunks = []
    for piece in read_in_chunks(filename, len):  # chunks da 2 bytes
        chunks.append(toBinary16(int.from_bytes(piece, byteorder='big')))
    return chunks


def read_in_chunks(filename, chunk_size):
    file = open(filename, "rb")
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data
    return data


def get_dir_list(out_lck, dir_name):
    i = 1
    fileList = []
    for file in os.listdir(dir_name):
        output(out_lck, "%s %s" % (i, file))
        fileList.append(str(file))
        i += 1

    nfile = loop_int_input(out_lck, "Choose file")
    nf = int(nfile) - 1
    filename = copy.copy(fileList[nf])
    return filename


def write_encrypted_from_chunks(int_chunks, filename, len):
    bytes_chunks = []
    for int_chunk in int_chunks:
        bytes_chunks.append(int_chunk.to_bytes(len, byteorder='big'))
    f = open('files/encrypted/' + filename, 'wb')
    for chunk in bytes_chunks:
        f.write(chunk)
    f.close()
    return 'encrypted/' + filename

def recon_file_and_write(out_lck, chunks, lunghezza, isFermat):
    stringa = ['89504e470d0a1a0a', 'ffd8ffe000104a46', '424df640000', '89504e47da1aa', '47496383961181', '474946',
               'FFFB']
    new_chunks = ''
    if lunghezza == 1:
        for chunk in chunks[0:8]:
            new = toBinary8(chunk)
            new_chunks = new_chunks + new
    elif lunghezza == 8:
        for chunk in chunks[0:1]:
            new = toBinary128(chunk)
            new_chunks = new_chunks + new

    for a in stringa:
        check = bin(int(a, 16))[2:]

        if new_chunks.find(check) != -1:

            if a == '89504e470d0a1a0a':
                output(out_lck, '\nDetect format file: PNG')
                if isFermat == 1:
                    write_decrypted_from_chunks(chunks, "decrypted_fermat.png", lunghezza)
                else:
                    write_decrypted_from_chunks(chunks, "decrypted.png", lunghezza)
            elif a == 'ffd8ffe000104a46':
                output(out_lck, '\nDetect format file: JPG')
                if isFermat == 1:
                    write_decrypted_from_chunks(chunks, "decrypted_fermat.jpg", lunghezza)
                else:
                    write_decrypted_from_chunks(chunks, "decrypted.jpg", lunghezza)
            elif a == '424df640000':
                output(out_lck, '\nDetect format file: BMP')
                if isFermat == 1:
                    write_decrypted_from_chunks(chunks, "decrypted_fermat.bmp", lunghezza)
                else:
                    write_decrypted_from_chunks(chunks, "decrypted.bmp", lunghezza)
            elif a == '474946':
                output(out_lck, '\nDetect format file: GIF')
                if isFermat == 1:
                    write_decrypted_from_chunks(chunks, "decrypted_fermat.gif", lunghezza)
                else:
                    write_decrypted_from_chunks(chunks, "decrypted.gif", lunghezza)
            elif a == 'FFFB':
                output(out_lck, '\nDetect format file: MP3')
                if isFermat == 1:
                    write_decrypted_from_chunks(chunks, "decrypted_fermat.mp3", lunghezza)
                else:
                    write_decrypted_from_chunks(chunks, "decrypted.mp3", lunghezza)
            break


def write_decrypted_from_chunks(byte_chunks, filename, lenght):
    f = open('received/' + filename, 'wb')
    for element in byte_chunks:
        asd = element.to_bytes(lenght, byteorder='big')
        f.write(asd)
    f.close()


def write_decrypted_from_chunks_fermat(byte_chunks, lenght):
    f = open('received/decrypted_fermat.jpg', 'wb')
    for element in byte_chunks:
        asd = element.to_bytes(lenght, byteorder='big')
        f.write(asd)
    f.close()

def fill(n, len):
    if bytes(n):
        return n.zfill(len)
    else:
        return n.zfill(len).encode('ascii')


def get_file_size(out_lck, file):
    return os.path.getsize("files/" + file)

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

def toBinary128(n):
    return ''.join(str(1 & int(n) >> i) for i in range(128)[::-1])


def toBinary2048(n):
    return ''.join(str(1 & int(n) >> i) for i in range(2048)[::-1])


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


def check_controller(e, d, n):
    # controllo che le chiavi generate a 8 bit funzionino
    m = 255
    c = pow(m, e, n)
    m1 = pow(c, d, n)
    if m == m1:
        return 1
    else:
        return 0


def generate_keys(out_lck, chunk_len):
    list_Prime = [2,3,5,7,11,13,17,19,23,29,31,37,41,43,47,53,59,61,67,71,73,79,83,89,97]
    controller = 0

    if chunk_len < 68:

        d = 1000
        p = 0
        q = 0
        n = 0
        e = 0
        fn = 0
        phi = 0

        while d > 255:  # and controller == 0 and phi == 0:

            p = random.choice(list_Prime)
            q = random.choice(list_Prime)
            n = p * q
            while n < 256 or p == q:
                p = random.choice(list_Prime)
                q = random.choice(list_Prime)
                n = p * q
            fn = (p - 1) * (q - 1)
            e = calculateEncryptionKey(n, fn)
            # d = math.pow((1/e), fn)
            gcd, x, y = egcd(e, fn)
            if gcd != 1:
                y = 0  # modular inverse does not exist
            else:
                d = x % fn
            phi = pow(1, d * e, n)
            controller = check_controller(e, d, n)

        if controller == 0 and phi == 0:
            print("errore")
        return n, d, e
    else:
        (pub_key, priv_key) = rsa.newkeys(chunk_len)
        p = priv_key['p']
        q = priv_key['q']
        n = priv_key['n']
        d = priv_key['d']
        e = pub_key['e']
        return n, d, e


def intsqrt(n):
    x = n
    y = (x + n // x) // 2
    while y < x:
        x = y
        y = (x + n // x) // 2
    return x


def factoring(out_lck, n, e):
    output(out_lck, 'Factoring %s ...' % n)
    a = intsqrt(n)
    b2 = a*a - n
    b = intsqrt(n)
    count = 0
    while b*b != b2:
        a = a + 1
        b2 = a*a - n
        b = intsqrt(b2)
        count += 1
    p=a+b
    q=a-b
    assert n == p * q
    output(out_lck, 'p = %s' % p)
    output(out_lck, 'q = %s' % q)
    mode = (p-1)*(q-1)
    #print('(p-1)*(q-1)= ', mode)
    output(out_lck, 'Finding d ...')
    for d in range(0, n):
        if e*d % mode == 1:
            output(out_lck, 'd = %s' % d)
            break

    return d