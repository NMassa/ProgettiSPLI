import socket
import os
import copy
import sys
from helpers import ccypher
from helpers.utils import *


def connect(out_lck, host, port):
    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ListLib = []

    try:
        #_socket.connect(("127.0.0.1", port))
        _socket.connect((host, port))

        shift = loop_int_input(out_lck, "Insert shift")
        i = 1
        for file in os.listdir("books"):
            if file.endswith(".txt"):
                print(i, file)
                ListLib.append(str(file))
                i += 1

        nfile = loop_int_input(out_lck, "Choose file")
        nf = int(nfile) - 1
        filename = copy.copy(ListLib[nf])
        f = open("books/"+filename, 'r')

        let = loop_menu(out_lck, "Select cyphering method: ", ["Full cypher", "Letter cypher"])
        if let == 2:
            l = f.read(1024)
            cs = ccypher.caesar(str(l), int(shift))
            tr = cs.encode()
            while (l):
                _socket.send(tr)

                l = f.read(1024)
                cs = ccypher.caesar(str(l), int(shift))
                tr = cs.encode()
            f.close()
        elif let == 1:
            l = f.read(1024)
            cs = ccypher.full_caesar(str(l), int(shift))
            tr = cs.encode()
            while l:
                _socket.send(tr)

                l = f.read(1024)
                cs = ccypher.full_caesar(str(l), int(shift))
                tr = cs.encode()
            f.close()
    except socket.error as msg:
        output(out_lck, str(msg))
        sys.exit(1)
    _socket.close()


def listen(out_lck, port):
    # Ascolto socket TCP
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

    try:
        s.bind(('', port))  # inizializzazione della connessione
        s.listen(100)
        conn, addr = s.accept()
        f = open('received/cifrato.txt', 'wb')
        size = 1024
        data = conn.recv(size)

        while len(data) > 0:
            f.write(data)
            data = conn.recv(size)
        f.close()

        shift = loop_int_input(out_lck, "Inserisci shift to decypher")
        f = open("received/cifrato.txt", 'rb')
        fout = open("received/decifrato.txt", 'w')

        l = f.read()
        let = loop_menu(out_lck, "Select decyphering method: ", ["Full cypher", "Letter cypher"])

        if let == 2:
            dc = ccypher.decaesar(l, int(shift))
            fout.write(dc)
        elif let == 1:
            dc = ccypher.full_decaesar(l, int(shift))
            fout.write(dc)

        f.close()


    except socket.error as msg:
        output(out_lck, str(msg))
        sys.exit(1)


