import threading, os, copy

from bitarray import *
from helpers.utils import loop_menu, loop_input, output, loop_int_input, get_chunks, gen_keys, get_chunks, DIM_BLOCK, \
    gen_keys2
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
    #dim_blocco = 8

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

            if algorithm == 4:
                prime_number = loop_input(out_lck, "Insert prime number: ")
            else:
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
            chunks = get_chunks("files/" + filename, DIM_BLOCK)

            if algorithm != 4 and algorithm != 5:
                keysA = gen_keys(keyA, len(chunks))
                output(out_lck, "Encrypting with Alice's key %s..." % keyA)
                # cifro e salvo di nuovo
                c = Cipher(out_lck, chunks, keysA)

            #algoritmo di cifratura
            if algorithm == 1: #XOR
                encrypted = c.encryptXOR()
                encA = "files/encrypted/encA_XOR"
                encAB = "files/encrypted/encAB_XOR"
                output(out_lck, "Encrypted with key Alice: '%s'" % keyA)
            elif algorithm == 2: #Somma
                encrypted = c.algorithmAdd()
                encA = "files/encrypted/encA_SUM"
                encAB = "files/encrypted/encAB_SUM"
                output(out_lck, "Encrypted with key Alice: '%s'" % keyA)
            elif algorithm == 3: #Shift
                encrypted = c.encryptShift()
                output(out_lck, "Shift!")
                encA = "files/encrypted/encA_SHIFT"
                encAB = "files/encrypted/encAB_SHIFT"
                output(out_lck, "Encrypted with key Alice: '%s'" % keyA)
            elif algorithm == 4: #Mul
                keysA = gen_keys(keyA, len(chunks))
                output(out_lck, "Encrypting with Alice's key %s..." % keyA)
                # cifro e salvo di nuovo
                c = Cipher(out_lck, chunks, keysA)
                encrypted = c.encryptMul()
                encA = "files/encrypted/encA_MUL"
                encAB = "files/encrypted/encAB_MUL"
                output(out_lck, "Encrypted with key Alice: '%s'" % keyA)
            elif algorithm == 5: #Exponential
                c = Cipher(out_lck, chunks, 0)
                encrypted = c.encryptMOD(10, int(prime_number))
                encA = "files/encrypted/encA_MOD"
                encAB = "files/encrypted/encAB_MOD"
                output(out_lck, "Encrypted with key Alice: '%s'" % c.encrypt_A)

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

            if algorithm != 5:
                output(out_lck, "Decrypting with Alice's key '%s'..." % keyA)
                # decifro con la keyA
                chunks = get_chunks(encAB, DIM_BLOCK)
                c = Cipher(out_lck, chunks, keysA)

            # algoritmo di decifratura
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
            elif algorithm == 4:
                c.decryptMul32()
                decA = "received/encB_MUL"
            elif algorithm == 5: #Exponential
                #TODO richiamo algoritmo di decrifratura
                #c.set_chunks(chunks)
                chunks = get_chunks(encAB, DIM_BLOCK)
                c.chunks = chunks
                #c = Cipher(out_lck, chunks, 0)
                decrypted = c.decryptMOD()
                output(out_lck, "Decrypting with Alice's key '%s'..." % c.decrypt_A)
                decA = "received/encB_MOD"

            output(out_lck, "Decrypted with Alice's key %s." % keyA)

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

            if algorithm != 4:
                keyB = loop_input(out_lck, "Insert key: ")  # key Bob
            else:
                prime_number = loop_input(out_lck, "Insert prime number: ")

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', port))
            sock.listen(1)
            output(out_lck, 'Waiting for Alice...')

            (client_sock, address) = sock.accept()

            # ricevo file cifrato con keyA e cifro di nuovo con la keyB
            recv_file(client_sock, "received/encA")

            output(out_lck, "Doing some magic tricks...Getting chunks :D")
            chunks = get_chunks("received/encA", DIM_BLOCK)

            if algorithm == 5:
                output(out_lck, "Encrypting with Bob's key '%s'..." % keyB)
                keysB = gen_keys(keyB, len(chunks))
                c = Cipher(out_lck, chunks, keysB)
            elif algorithm == 4:
                output(out_lck, "Encrypting with Bob's key '%s'..." % keyB)
                keysB = gen_keys2(keyB, len(chunks))
                c = Cipher(out_lck, chunks, keysB)
            else:
                output(out_lck, "Encrypting with Bob's key...")
                keysB = gen_keys(keyB, len(chunks))
                c = Cipher(out_lck, chunks, prime_number)

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
            elif algorithm == 4:
                encrypted = c.encryptMul()
                encAB = "received/encAB_MUL"
                encB = "received/encB_MUL"
            elif algorithm == 5: #Exponential
                c = Cipher(out_lck, chunks, 0)
                encrypted = c.encryptMOD(7, int(prime_number))
                encAB = "received/encAB_MOD"
                encB = "received/encB_MOD"
                output(out_lck, "Encrypted with Bob's key '%s'." % c.encrypt_A)

            if algorithm != 5:
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

            chunks = get_chunks(encB, DIM_BLOCK)

            output(out_lck, "Decrypting with Bob's key...")

            #algoritmo di decifratura
            if algorithm == 1: #XOR
                c = Cipher(out_lck, chunks, keysB)
                decrypted = c.decryptXOR()
                fname = "received/decrypted_XOR.mp4"
            elif algorithm == 2: #Somma
                c = Cipher(out_lck, chunks, keysB)
                decrypted = c.algorithmDiff()
                fname = "received/decrypted_SUM.jpg"
            elif algorithm == 3: #Shift
                c = Cipher(out_lck, chunks, keysB)
                decrypted =c.decryptShift()
                output(out_lck, "Shift!")
                fname = "received/decrypted_Shift.jpg"
            elif algorithm == 4: #Mul
                c = Cipher(out_lck, chunks, keysB)
                decrypted = c.decryptMul16()
                fname = "received/decrypted_MUL.jpg"
            elif algorithm == 5: #Exponential
                c.chunks = chunks
                decrypted = c.decryptMOD()
                fname = "received/decrypted_MOD.jpg"
                output(out_lck, "Decrypted with Bob's key '%s'." % c.decrypt_A)

            if algorithm != 5:
                output(out_lck, "Decrypted with Bob's key '%s'." % keyB)

            fout = open(fname, "wb+")

            for chunk in decrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()
            sock.close()
            output(out_lck, "\n\nDone!\n\n")










