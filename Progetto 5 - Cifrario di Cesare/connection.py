import socket
import os
import copy


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


def server():
    # ip local
    host = socket.gethostname()  # Get local machine name
    port = 60000  # Reserve a port for your service.
    s = socket.socket()  # Create a socket object
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))  # Bind to the port
    s.listen(1)  # Now wait for client connection.

    print('Server listening....')
    ListLib = []

    conn, addr = s.accept()
    print("Insert Shift")
    shift = input()

    i = 1
    for file in os.listdir("/Users/Giacomo/Documents"):  # da modificare path
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
        conn.send(tr)
        print('Sent ', repr(tr))
        l = f.read(1024)
        cs = caesar(str(l), int(shift))
        tr = cs.encode()
    f.close()
    print("Done Sending")
    conn.close()


def client():
    c_s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Create a socket object
    host = socket.gethostname()  # Get local machine name
    port = 60000  # Reserve a port for your service.

    c_s.connect((host, port))

    with open('received_file.txt', 'wb') as f:
        print('file opened')
        while True:
            print('receiving data...')
            data = c_s.recv(1024)
            print('data ', (data))
            if not data:
                break
            # write data to a file
            f.write(data)

    f.close()
    print('Successfully get the file')
    c_s.close()
    print('connection closed')


def menu():
    print('---1--- Send message    --')
    print('---2--- Receive message --')
    print('---3--- List of file    --')
    print('---0--- Exit            --')


if __name__ == '__main__':
    menu()
    print("Choose an option:")
    scelta = input()
    if (scelta == '1'):
        server()
    if (scelta == '2'):
        client()
    if (scelta == '3'):
        for file in os.listdir("/Users/Giacomo/Documents"):
            if file.endswith(".txt"):
                print(os.path.join("/Users/Giacomo/Documents", file))
