from socket import *
from helpers.utils import output

class MySocket:

    def __init__(self, sock=None):
        if sock is None:
            self.__sock = socket(AF_INET, SOCK_STREAM)
            self.__sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
        else:
            self.__sock = sock

    def send(self, msg):
        msglen = len(msg)
        totalsent = 0
        while totalsent < msglen:
            sent = self.__sock.send(msg[totalsent:])
            if sent == 0:
                raise RuntimeError("Connection interrupted.")
            totalsent = totalsent + sent

    def receive(self, msglen):
        msg = b''
        while len(msg) < msglen:
            chunk = self.__sock.recv(msglen - len(msg))
            if chunk == b'':
                raise RuntimeError("Connection interrupted")
            msg += chunk
        return msg

    def connect(self, host, port):
        self.__sock.connect((host, port))

    def bind(self, host, port):
        self.__sock.bind((host, port))

    def listen(self, value):
        self.__sock.listen(value)

    def accept(self):
        return self.__sock.accept()

    def shutdown(self, arg):
        return self.__sock.shutdown(arg)

    def close(self):
        return self.__sock.close()

    def sendfile(self, sock, address, port, filename):
        sock.connect(address, port)
        with open("files/" + filename, 'rb') as f:
            data = f.read(1024)
            while data:
                sock.send(data)
                data = f.read(1024)
        f.close()
        sock.close()

    def receivefile(self, out_lck, sock, port, filename, extension):
        sock.bind('', port)
        sock.listen(5)
        output(out_lck, "Waiting for connection...")
        (client_sock, address) = sock.accept()
        output(out_lck, "Connection established.")

        with open("received/" + filename + "." + extension, 'wb') as f:
            data = client_sock.recv(1024)
            while len(data) == 1024:
                f.write(data)
                data = client_sock.recv(1024)
            f.write(data)
        f.close()
        sock.close()
