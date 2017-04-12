import socket
import os
import copy
import sys


def caesar(plainText, shift):
    cipherText = ""
    for ch in plainText:
        if ch.isalpha():
            stayInAlphabet = ord(ch) + shift
            if stayInAlphabet > ord('z'):
                stayInAlphabet -= 26
            finalLetter = chr(stayInAlphabet)
            cipherText += finalLetter
    # print "Your ciphertext is: ", cipherText
    return cipherText


def connect(Host, Port):
    # Socket TCP
    host = Host
    port = Port

    _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    ListLib = []
    try:
        _socket.connect((host, port))
        # qui devo fare un ciclo o un timer per mandare le richieste
        print("Insert Shift")
        shift = input()

        i = 1
        # for file in os.listdir("~/PycharmProjects/SPLI/Progetto 5 - Cifrario di Cesare/books"):
        for file in os.listdir("/Users/Giacomo/Documents"):
            if file.endswith(".txt"):
                print(i, file)
                ListLib.append(str(file))
                i += 1
        print("Choose file ")
        nfile = input()
        nf = int(nfile) - 1
        filename = copy.copy(ListLib[nf])
        f = open(filename, 'rb')
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
        size = 1024
        data = conn.recv(size)
        while len(data) > 0:
            print ("Received: %s" % data)
            data = conn.recv(size)
    except socket.error as msg:
        sys.exit(1)
        # helpers.output(self.out_lck, str(msg))


  #  def menu():
   #     print('---1--- Send message    --')
    #    print('---2--- Receive message --')
     #   print('---3--- List of file    --')
      #  print('---0--- Exit            --')


  #  if __name__ == '__main__':
  #     menu()
  #      print("choose an option:")
  #      sc = input()
  #      scelta = int(sc)
  #      print("scelta", scelta)
  #      if (scelta == 1):
   #         connect()
   #     if (scelta == 2):
   #         listen()
   #     if (scelta == 3):
   #           for file in os.listdir("~/pycharmprojects/spli/progetto 5 - cifrario di cesare/books"):
   #             if file.endswith(".txt"):
    #                print(os.path.join("~/pycharmprojects/spli/progetto 5 - cifrario di cesare/books", file))
