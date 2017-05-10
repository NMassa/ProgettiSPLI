import os
import socket

import helpers


def UDPclient(out_lck, host, port, data):

    _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        _socket.connect((host, port))

        idx = 0
        l = data[0:1024]
        while l:
            _socket.sendall(l)
            l = data[idx:idx+1024]
            idx += 1024

        _socket.close()

    except socket.error as msg:
        helpers.utils.output(out_lck, msg)
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

        helpers.utils.output(out_lck, "Listening on port %s..." % port)
        data = sock.recv(1024)
        f.write(data)
        while len(data) == 1024:
            data = sock.recv(1024)
            f.write(data)

        sock.close()
        f.close()

    except socket.error as msg:
        helpers.utils.output(out_lck, msg)
        exit(3)
    else:
        sock.close()