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

    def sendfile(self, out_lck, sock, filename):
        try:
            size = get_file_size(out_lck, filename)
            #sock.send(fill(str(filename[-3:]).encode('utf-8'), 3))   #send the extension of the file 3 CHAR!!!
            sock.send(fill(str(size).encode('utf-8'), 8))
            with open("files/" + filename, 'rb') as f:
                output(out_lck, "Sending File...")
                sock.send(f.read(size))
            f.close()
        except Exception as e:
            output(out_lck, e)
            exit(1)

    def receivefile(self, out_lck, sock, filename):
        try:
            output(out_lck, "Waiting for connection...")
            (client_sock, address) = sock.accept()
            myclient_sock = MySocket(client_sock)
            output(out_lck, "Connection established.")
            output(out_lck, "Receiving file..")
            with open("received/" + filename, 'wb') as f:
                size = int(myclient_sock.recv(8))
                received = myclient_sock.recv(size)
                output(out_lck, "Received!\nWriting file...")
                f.write(received)
            f.close()
            return 'received/' + filename, address[0]
        except Exception as e:
            output(out_lck, e)
            exit(2)

    def send_key(self, out_lck, sock, key, len):
        try:
            sock.send(fill(str(len).encode('utf-8'), 128))   #send the lenght of the key
            sock.send(fill(str(key).encode('utf-8'), len))
        except Exception as e:
            output(out_lck, "Error: " + str(e))
            exit(3)

    def recv_key(self, out_lck, sock, port):
        try:
            sock.bind('', port)
            sock.listen(5)
            (client_sock, address) = sock.accept()
            myclient_sock = MySocket(client_sock)
            output(out_lck, "Connection established.")

            key_lenght = int(myclient_sock.recv(128))
            mod, pkey, len_key = bytes(myclient_sock.recv(key_lenght)).decode('utf-8').split('@')
            pkey = int(pkey, 2)
            mod = int(mod, 2)
            len_key = int(len_key, 2)
            output(out_lck, "Received Key: %s\nReceived module: %s" % (pkey, mod))
            return pkey, mod, len_key, address
        except Exception as e:
            output(out_lck, "Error: " + str(e))
            exit(4)
