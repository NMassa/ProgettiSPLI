import socket
from helpers import config
from helpers import helpers
import threading

out_lck = threading.Lock()

class Connection:
        socket = None
        host = None
        protocol = None
        port = None

        def __init__(self, host, protocol, port):
                self.host = "%s%s" % (config._base,host)
                self.protocol = protocol
                self. port = int(port)

        #Lato client
        def connect(self):
            #Socket TCP
            if str(self.protocol) == "TCP":
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                try:
                    self.socket.connect((self.host, self.port))
                    #qui devo fare un ciclo o un timer per mandare le richieste
                    message = "I like Bananas"
                    self.socket.sendall(message)

                except socket.error as msg:
                    helpers.output(out_lck, str(msg))

                helpers.output(out_lck, "Done!")
                self.socket.close()

            #Socket Datagram
            elif str(self.protocol) == "UDP":
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                try:
                    self.socket.connect((self.host, self.port))
                    # qui devo fare un ciclo o un timer per mandare le richieste
                    message = "I like Bananas"
                    for i in range(0, 40):
                        self.socket.sendall(message)

                except socket.error as msg:
                    helpers.output(out_lck, str(msg))
                helpers.output(out_lck, "Done!")
                self.socket.close()
            else:
                #errori
                exit()

        #Lato server
        def listen(self):

            if str(self.protocol) == "TCP":

                #Ascolto socket TCP
                self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    self.socket.bind(('localhost', self.port))  # inizializzazione della connessione
                    self.socket.listen(10)
                    helpers.output(out_lck, "Listening on port %s" % (self.port))
                    while True:
                        conn, addr = self.socket.accept()
                        data = conn.recv(40)
                        helpers.output(out_lck, "Received: %s" % data)
                except socket.error as msg:
                    helpers.output(out_lck, str(msg))

            #Ascolto socket UDP
            elif str(self.protocol) == "UDP":

                self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

                try:
                    self.socket.bind(('localhost', self.port))  # inizializzazione della connessione
                    helpers.output(out_lck, "Listening on port %s" % (self.port))
                    while True:
                        data, address = self.socket.recvfrom(40)
                        helpers.output(out_lck, "Received: %s" % data)

                except socket.error as msg:
                    helpers.output(out_lck, str(msg))
            else:
                #errori
                exit()