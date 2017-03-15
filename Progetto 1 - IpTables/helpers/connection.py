import socket
from helpers import config
from helpers import helpers
import os
import time
import threading


class Connection:
        socket = None
        host = None
        protocol = None
        port = None
        out_lck = None

        def __init__(self, host, protocol, port, out_lock):
                self.host = host
                self.protocol = protocol
                self. port = int(port)
                self.out_lck = out_lock

        #Lato client
        def connect(self):
            #Socket TCP
            if str(self.protocol) == "TCP":
                for i in range(0, 10):
                    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    try:
                        _socket.connect((self.host, self.port))
                        #qui devo fare un ciclo o un timer per mandare le richieste
                        message = bytes("Sicurezza, Progettazione e Laboratorio Internet", encoding="utf8")
                        _socket.sendall(message)

                    except socket.error as msg:
                        helpers.output(self.out_lck, str(msg))

                    _socket.close()

                helpers.output(self.out_lck, "Done!")

            #Socket Datagram
            elif str(self.protocol) == "UDP":
                for i in range(0, 10):
                    self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                    #self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                    try:
                        self.socket.connect((self.host, self.port))
                        # qui devo fare un ciclo o un timer per mandare le richieste
                        message = bytes("Sicurezza, Progettazione e Laboratorio Internet", encoding="utf8")

                        self.socket.sendall(message)

                        helpers.output(self.out_lck, "%d" % i)
                        self.socket.close()

                    except socket.error as msg:
                        helpers.output(self.out_lck, str(msg))

            else:
                #errori
                exit()

        #Lato server
        def listen(self):

            if str(self.protocol) == "TCP":

                #Ascolto socket TCP
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    self.socket.bind(('', self.port))  # inizializzazione della connessione
                    self.socket.listen(100)
                    helpers.output(self.out_lck, "Listening on port %s" % (self.port))
                    conn, addr = self.socket.accept()
                    size = 1024
                    data = conn.recv(size)
                    while len(data) > 0:
                        helpers.output(self.out_lck, "Received: %s" % data)
                        data = conn.recv(size)
                except socket.error as msg:
                    helpers.output(self.out_lck, str(msg))

            #Ascolto socket UDP
            elif str(self.protocol) == "UDP":

                _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
                _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
                try:
                    _socket.bind(("", self.port))  # inizializzazione della connessione
                    helpers.output(self.out_lck, "Listening on port %s" % (self.port))
                    while True:
                        data, address = _socket.recvfrom(1024)
                        helpers.output(self.out_lck, "Received: %s" % data)

                except socket.error as msg:
                    helpers.output(self.out_lck, str(msg))
            else:
                #errori
                exit()

        # #server client per mangle -NON SERVE-
        # def client_server(self):
        #     _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #     _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        #
        #     try:
        #         _socket.bind(("", self.port))  # inizializzazione della connessione
        #         helpers.output(self.out_lck, "CS: Listening on port %s" % (self.port))
        #         while True:
        #             data, address = _socket.recvfrom(1024)
        #             helpers.output(self.out_lck, "CS: Received: %s" % data)
        #             _socket.close()
        #             break
        #
        #     except socket.error as msg:
        #         helpers.output(self.out_lck, str(msg))
        #
        #     self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        #
        #     try:
        #         self.socket.connect((self.host, self.port))
        #
        #         # qui devo fare un ciclo o un timer per mandare le richieste
        #         #message = bytes(data, encoding="utf8")
        #
        #         self.socket.sendall(data)
        #         #helpers.output(self.out_lck, data)
        #         self.socket.close()
        #
        #     except socket.error as msg:
        #         helpers.output(self.out_lck, str(msg))


        def send_udp(n, msg, addr, port):
            for i in range(0, n):
                cmd = "echo \"" + msg + "\" | nc -4u -w1 " + addr + " " + str(port)
                os.system(cmd)
