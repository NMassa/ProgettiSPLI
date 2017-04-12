import socket
import os
import copy
import sys




def caesar(message, shift):
    key = shift
    translated = ''

    for symbol in message:
        if symbol.isalpha():
            num = ord(symbol)
            num += key

            if symbol.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26

            translated += chr(num)
        else:
           translated += symbol
    return translated


def decaesar(message,shift):
    key = -shift
    translated = ''

    for symbol in message:
        if symbol.isalpha():
            num = ord(symbol)
            num += key

            if symbol.isupper():
                if num > ord('Z'):
                    num -= 26
                elif num < ord('A'):
                    num += 26
            elif symbol.islower():
                if num > ord('z'):
                    num -= 26
                elif num < ord('a'):
                    num += 26

            translated += chr(num)
        else:
           translated += symbol
    return translated


def connect(Host, Port):
    # Socket TCP
    host = Host
    port = Port

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ListLib = []
    try:
        _socket.connect((host, port))

        print("Insert Shift")
        shift = input()

        i = 1
        for file in os.listdir("books"):
        #for file in os.listdir("/Users/Giacomo/Documents"):
            if file.endswith(".txt"):
                print(i, file)
                ListLib.append(str(file))
                i += 1
        print("Choose file ")
        nfile = input()
        nf = int(nfile) - 1
        filename = copy.copy(ListLib[nf])
        f = open("books/"+filename, 'r')
        l = f.read(1024)
        cs = caesar(str(l), int(shift))
        tr = cs.encode()
        while (l):
            _socket.send(tr)
            print('Sent ', repr(tr))
            l = f.read(1024)
            cs = caesar(str(l), int(shift))
            tr = cs.encode()
        f.close()

    except socket.error as msg:
        sys.exit(1)
    _socket.close()


def listen(Port):
    # Ascolto socket TCP
    port = Port
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    try:
        s.bind(('', port))  # inizializzazione della connessione
        s.listen(100)
        conn, addr = s.accept()
        f = open('received_file.txt', 'wb')
        size = 1024
        data = conn.recv(size)
        while len(data) > 0:
            print ("Received: %s" % data)
            f.write(data)
            data = conn.recv(size)
        f.close()
        print("Decifro file sapendo shift\n Inserisci shift \n")
        shift = input()
        f = open("received_file.txt", 'rb')
        l = f.read(1024)
        l = l.decode('utf8')
        # print("leggo %s" %l)
        dc = decaesar(str(l), int(shift))
        tr = dc  # .encode()
        while (l):
            print('decipherText ', repr(tr))
            l = f.read(1024)
            l = l.decode('utf8')
            dc = decaesar(str(l), int(shift))
            tr = dc  # .encode()

        f.close()
    except socket.error as msg:
        sys.exit(1)
        # helpers.output(self.out_lck, str(msg))


