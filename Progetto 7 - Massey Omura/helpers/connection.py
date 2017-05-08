import socket
from helpers.utils import output
import os


def recvall(socket, chunk_size):
    """
    Legge dalla socket un certo numero di byte, evitando letture inferiori alla dimensione specificata
    """

    data = socket.recv(chunk_size)  # Lettura di chunk_size byte dalla socket
    actual_length = len(data)

    # Se sono stati letti meno byte di chunk_size continua la lettura finchè non si raggiunge la dimensione specificata
    while actual_length < chunk_size:
        new_data = socket.recv(chunk_size - actual_length)
        actual_length += len(new_data)
        data += new_data

    return data


def UDPclient(out_lck, host, port, data):

    _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        #_socket.connect(("127.0.0.1", 60000))
        _socket.connect((host, port))

        idx = 0
        l = data[0:1024]
        while l:
            _socket.sendall(l)
            l = data[idx:idx+1024]
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


def TCPclient(out_lck, host, port, data):

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        _socket.connect((host, port))
        #_socket.connect(("127.0.0.1", 3000))
        while data:
            _socket.send(data)
    except socket.error as msg:
        output(out_lck, msg)
        exit(2)
    _socket.close()


def TCPserver(out_lck, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        output(out_lck, "Listening....\n")
        s.bind(('', port))  # inizializzazione della connessione
        s.listen(100)
        conn, addr = s.accept()
        f = open('files/output/TCPreceived', 'wb')
        size = 1024
        data = recvall(conn, size)

        while len(data) > 0:
            f.write(data)
            data = recvall(conn, size)

        f.close()
    except socket.error as msg:
        output(out_lck, msg)
        exit(4)
    s.close()