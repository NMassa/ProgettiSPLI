from helpers.cipher import *

from bitarray import bitarray
import os
from helpers.connection import *


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
        if n == len // 8:  # controllore se voglio chunk più lunghi
            chunks.append(chunk)
            chunk = ''
            n = 0
    f.close()
    return chunks


def xor_func(xs, ys):
    return "".join(str(ord(x) ^ ord(y)) for x, y in zip(xs, ys))


def toBinary32(n):
    return ''.join(str(1 & int(n) >> i) for i in range(32)[::-1])


def send_file_crypt(out_lck, chunks, key, _base, host):
    c = Cipher(out_lck, chunks, key)
    output(out_lck, "Encrypting file...")
    c.encrypt()
    output(out_lck, "File encrypted")

    data = b''
    for chunk in chunks:
        data += bitarray(chunk).tobytes()

    output(out_lck, "Sending file...")
    UDPclient(out_lck, _base + host, 60000, data)
    output(out_lck, "File Crypted sent")


def send_file_decrypt(out_lck, chunks, key, _base, host):
    c = Cipher(out_lck, chunks, key)
    output(out_lck, "Decrypting file...")
    c.decrypt()
    output(out_lck, "File decrypted")

    data = b''
    for chunk in c.encrypted:
        data += bitarray(chunk).tobytes()

    output(out_lck, "Sending file...")
    UDPclient(out_lck, _base + host, 60000, data)
    output(out_lck, "File Decrypted sent")


# mi da problemi l'import e definendole qua va tutto

def UDPclient(out_lck, host, port, data):
    _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        # _socket.connect(("127.0.0.1", 60000))
        _socket.connect((host, port))

        idx = 0
        l = data[0:1024]
        while l:
            _socket.sendall(l)
            l = data[idx:idx + 1024]
            idx += 1024

        _socket.close()

    except socket.error as msg:
        output(out_lck, msg)
        exit(1)
    else:
        _socket.close()


def UDPserver(out_lck, port):
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    count = 0
    for file in os.listdir("received"):
        if "UDPReceived" in file:
            count += 1

    f = open('received/UDPReceived%s' % count, 'wb+')
    try:
        sock.bind(("", port))

        output(out_lck, "Listening on port %s..." % port)
        data, address = sock.recvfrom(1024)
        while len(data) == 1024:
            data, address = sock.recvfrom(1024)
            f.write(data)

        sock.close()
        f.close()

    except socket.error as msg:
        output(out_lck, msg)
        exit(3)
    else:
        sock.close()