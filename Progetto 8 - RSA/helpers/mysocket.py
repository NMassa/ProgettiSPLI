from socket import *
from helpers.utils import output, get_file_size, fill

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

    def recv(self, msglen):
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

    def sendfile(self, out_lck, sock, address, port, filename):
        sock.connect(address, port)
        size = get_file_size(out_lck, filename)
        sock.send(fill(str(size), 128))
        with open("files/" + filename, 'rb') as f:
            output(out_lck, "Sending File...")
            sock.send(f.read(size * 8))
        f.close()
        sock.close()

    def receivefile(self, out_lck, sock, port, filename, extension):
        sock.bind('', port)
        sock.listen(5)
        output(out_lck, "Waiting for connection...")
        (client_sock, address) = sock.accept()
        myclient_sock = MySocket(client_sock)
        output(out_lck, "Connection established.")

        with open("received/" + filename + "." + extension, 'wb') as f:
            size = int(myclient_sock.recv(128))
            output(out_lck, "Receiving file of %d KB..." % (size / 8))
            received = myclient_sock.recv(size)
            output(out_lck, "Received..Writing file...")
            f.write(received)
        f.close()
        sock.close()
