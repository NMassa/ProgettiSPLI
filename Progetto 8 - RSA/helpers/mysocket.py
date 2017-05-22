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
        try:
            size = get_file_size(out_lck, filename)
            sock.send(fill(str(filename[-3:]).encode('utf-8'), 3))   #send the extension of the file 3 CHAR!!!
            sock.send(fill(str(size).encode('utf-8'), 128))
            with open("files/" + filename, 'rb') as f:
                output(out_lck, "Sending File...")
                sock.send(f.read(size))
            f.close()
            sock.close()
        except Exception as e:
            output(out_lck, e)
            exit(1)

    def receivefile(self, out_lck, myclient_sock, filename):
        try:

            #ATTENZIONE! l'extension è sott'intesa di 3 CHAR
            extension = bytes(myclient_sock.recv(3)).decode('utf-8')
            output(out_lck, "Receiving %s file.." % extension)

            with open("received/" + filename + "." + extension, 'wb') as f:
                size = int(myclient_sock.recv(128))
                output(out_lck, "Receiving file of %d KB..." % (size / 16))
                received = myclient_sock.recv(size)
                output(out_lck, "Received..Writing file...")
                f.write(received)
            f.close()
            myclient_sock.close()
        except Exception as e:
            output(out_lck, e)
            exit(2)

    def send_key(self, out_lck, sock, address, port, key, len):
        try:
            sock.connect(address, port)
            sock.send(fill(str(len).encode('utf-8'), 128))   #send the lenght of the key
            sock.send(fill(str(key).encode('utf-8'), len))
            output(out_lck, "Key sent.")
            sock.shutdown(0)
        except Exception as e:
            output(out_lck, "Error: " + str(e))
            exit(3)

    def recv_key(self, out_lck, sock, port):
        try:
            sock.bind('', port)
            sock.listen(5)
            output(out_lck, "Waiting for key...")
            (client_sock, address) = sock.accept()
            myclient_sock = MySocket(client_sock)
            output(out_lck, "Connection established.")

            key_lenght = int(myclient_sock.recv(128))
            key = myclient_sock.recv(key_lenght)
            output(out_lck, "Received Key: %s of length %d bits" % (bytes(key).decode('utf-8'), key_lenght))
            sock.shutdown(0)
            return key, key_lenght, myclient_sock
        except Exception as e:
            output(out_lck, "Error: " + str(e))
            exit(3)