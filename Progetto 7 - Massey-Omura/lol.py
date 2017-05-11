import threading, os, copy

from bitarray import *
from helpers.utils import loop_menu, loop_input, output, loop_int_input, get_chunks, gen_keys, get_chunks
from helpers.cipher import Cipher
import socket

_base = "192.168."
host = 0

## metodo per inviare un file attraverso una socket
def send_file (sock, file_path):
    ## legge il file e lo invia un po' per volta
    with open(file_path, 'rb') as f:
        data = f.read(1024)
        while data:
            sock.send(data)
            data = f.read(1024)

## metodo per ricevere le informazioni da una socket
## e le scrive in un file
def recv_file(sock, file_path):
    ## scrive sul file indicato
    with open(file_path, 'wb') as f:
        data = sock.recv(1024)
        while len(data) == 1024:
            f.write(data)
            data = sock.recv(1024)
        f.write(data)

if __name__ == "__main__":

    out_lck = threading.Lock()
    network = 0
    port = 60000

    while network == 0:
        network = loop_menu(out_lck, "Select network enviroment ('e' to exit): ", ["Local", "Network"])
        if network == 1:
            _base = "127.0.0."
            host = "1"
        elif network == 2:
            ip = loop_input(out_lck, "Insert your IP: ")
            my_ip = _base + ip
            output(out_lck, "Your IP: " + my_ip)

    while True:

        algorithm = loop_menu(out_lck, "Select encryption algorithm ('e' to exit)", ["XOR", "Sum", "Shift", "Exponential"])
        # Main Menu
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Send file",
                                                                                               "Receive file"])
        if main_menu == 1:
            if network == 2:
                host = loop_input(out_lck, "Insert destination IP:")

            output(out_lck, "destination IP:" + _base + host)
            keyA = loop_input(out_lck, "Insert Key: ")

            i = 1
            fileList = []
            for file in os.listdir("files"):
                output(out_lck, "%s %s" % (i, file))
                fileList.append(str(file))
                i += 1

            nfile = loop_int_input(out_lck, "Choose file")
            nf = int(nfile) - 1
            filename = copy.copy(fileList[nf])

            output(out_lck, "Doing some magic tricks..... :D")
            chunks = get_chunks("files/" + filename, 64)
            keysA = gen_keys(keyA, len(chunks))

            output(out_lck, "Cifro con key Alice %s..." % keyA)

            # cifro e salvo di nuovo
            c = Cipher(out_lck, chunks, keysA)

            #algoritmo di cifratura
            if algorithm == 1: #XOR
                encrypted = c.encryptXOR()
                encA = "files/encrypted/encA_XOR"
                encAB = "files/encrypted/encAB_XOR"
            elif algorithm == 2: #Somma
                encrypted = c.algorithmAdd()
                encA = "files/encrypted/encA_SUM"
                encAB = "files/encrypted/encAB_SUM"
            elif algorithm == 3: #Shift
                encrypted = c.encryptShift()
                output(out_lck, "Shift!")
                encA = "files/encrypted/encA_SHIFT"
                encAB = "files/encrypted/encAB_SHIFT"
            elif algorithm == 4: #Exponential
                output(out_lck, "Zomi Mona")

            output(out_lck, "Encrypted with key Alice: '%s'" % keyA)

            fout = open(encA, "wb+")

            for chunk in encrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()

            # invio file cifrato con keyA
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((_base + host, port))

            output(out_lck, "Sending encrypted file with Alice's key...")
            send_file(sock, encA)

            output(out_lck, "Waiting for Bob...")
            # ricevo file cifrato con keyB
            recv_file(sock, encAB)

            output(out_lck, "Decrypting with Alice's key '%s'..." % keyA)

            # decifro con la keyA
            chunks = get_chunks(encAB, 64)
            c = Cipher(out_lck, chunks, keysA)

            #algoritmo di decifratura
            if algorithm == 1: #XOR
                decrypted = c.decryptXOR()
                decA = "received/encB_XOR"
            elif algorithm == 2: #Somma
                decrypted = c.algorithmDiff()
                decA = "received/encB_SUM"
            elif algorithm == 3: #Shift
                decrypted = c.decryptShift()
                output(out_lck, "Shift!")
                decA = "received/encB_Shift"
            elif algorithm == 4: #Exponential
                output(out_lck, "Zomi Mona")


            output(out_lck, "Decrypted with Alice's key.")

            fout = open(decA, "wb+")

            for chunk in decrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()

            output(out_lck, "Sending encrypted file with Bob's key...")
            send_file(sock, decA)
            output(out_lck, "\n\nDone!\n\n")
            sock.close()

        elif main_menu == 2:
            if network == 2:
                host = loop_input(out_lck, "Insert destination IP:")

            keyB = loop_input(out_lck, "Insert key: ")  # key Bob

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', port))
            sock.listen(1)
            output(out_lck, 'Waiting for Alice...')

            (client_sock, address) = sock.accept()

            # ricevo file cifrato con keyA e cifro di nuovo con la keyB
            recv_file(client_sock, "received/encA")

            output(out_lck, "Doing some magic tricks...Getting chunks :D")
            chunks = get_chunks("received/encA", 64)

            output(out_lck, "Encrypting with Bob's key '%s'..." % keyB)

            keysB = gen_keys(keyB, len(chunks))
            c = Cipher(out_lck, chunks, keysB)

            #algoritmo di cifratura
            if algorithm == 1: #XOR
                encrypted = c.encryptXOR()
                encAB = "received/encAB_XOR"
                encB = "received/encB_XOR"
            elif algorithm == 2: #Somma
                encrypted = c.algorithmAdd()
                encAB = "received/encAB_SUM"
                encB = "received/encB_SUM"
            elif algorithm == 3: #Shift
                encrypted= c.encryptShift()
                output(out_lck, "Shift!")
                encAB = "received/encAB_Shift"
                encB = "received/encB_Shift"
            elif algorithm == 4: #Exponential
                output(out_lck, "Zomi Mona")

            output(out_lck, "Encrypted with Bob's key '%s'." % keyB)

            fout = open(encAB, "wb+")

            for chunk in encrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()

            output(out_lck, "Sending encrypted file with Bob and Alice's key...")
            send_file(client_sock, encAB)

            output(out_lck, "Waiting for encrypted file with Bob's key...")
            # ricevo file cifrato con keyB
            recv_file(client_sock, encB)

            chunks = get_chunks(encB, 64)

            output(out_lck, "Decrypting with Bob's key...")
            c = Cipher(out_lck, chunks, keysB)

            #algoritmo di decifratura
            if algorithm == 1: #XOR
                decrypted = c.decryptXOR()
                fname = "received/decrypted_XOR.mp4"
            elif algorithm == 2: #Somma
                decrypted = c.algorithmDiff()
                fname = "received/decrypted_SUM.jpg"
            elif algorithm == 3: #Shift
                decrypted =c.decryptShift()
                output(out_lck, "Shift!")
                fname = "received/decrypted_Shift.jpg"
            elif algorithm == 4: #Exponential
                output(out_lck, "Zomi Mona")


            output(out_lck, "Decrypted with Bob's key '%s'." % keyB)

            fout = open(fname, "wb+")

            for chunk in decrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()
            sock.close()
            output(out_lck, "\n\nDone!\n\n")










