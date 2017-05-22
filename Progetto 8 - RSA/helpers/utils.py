import os, copy, pyprimes, math


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
    for piece in read_in_chunks(filename, 128):  # chunks da 128 bytes
        output(out_lck, "JUST DO IT")
    return chunks


def read_in_chunks(filename, chunk_size):
    file = open("files/" + filename, "rb")
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        if len(data) < chunk_size:      #TODO: controllare grandezza ultimo chunk
            fill(data, chunk_size)
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

