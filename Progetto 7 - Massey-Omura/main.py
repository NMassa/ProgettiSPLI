import threading, os, copy

from bitarray import *
from helpers.utils import loop_menu, loop_input, output, loop_int_input, gen_keys, get_chunks, \
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
            sock.sendall(data)
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
    return data
if __name__ == "__main__":

    out_lck = threading.Lock()
    network = 0
    port = 60000

    #Get the network...
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

        algorithm = loop_menu(out_lck, "Select encryption algorithm ('e' to exit)", ["XOR", "Sum", "Shift", "Multiply", "Exponential"])
        # Main Menu
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Send file",
                                                                                               "Receive file"])
        if main_menu == 1:
            if network == 2:
                host = loop_input(out_lck, "Insert destination IP:")

            output(out_lck, "destination IP:" + _base + host)

            if algorithm != 5:
                keyA = loop_input(out_lck, "Insert Key: ")

            #Get filenames
            i = 1
            fileList = []
            for file in os.listdir("files"):
                output(out_lck, "%s %s" % (i, file))
                fileList.append(str(file))
                i += 1

            nfile = loop_int_input(out_lck, "Choose file")
            nf = int(nfile) - 1
            filename = copy.copy(fileList[nf])

            #sender chunks first time

            #Zotti e Massa prendono i primi chunk da 8
            if algorithm != 4 and algorithm != 5:
                output(out_lck, "Getting 64 bit file chunks..")
                chunks = get_chunks("files/" + filename, 64)
                keysA = gen_keys(keyA, len(chunks))
                output(out_lck, "Encrypting with Alice's key %s..." % keyA)
                # cifro e salvo di nuovo
                c = Cipher(out_lck, chunks, keysA)
            else:
                output(out_lck, "Getting 8 bit file chunks..")
                chunks = get_chunks("files/" + filename, 8)

            #algoritmo di cifratura
            if algorithm == 1: #XOR
                encrypted = c.encryptXOR()
                encA = "files/encrypted/encA_XOR"
                encAB = "files/encrypted/encAB_XOR"
                output(out_lck, "Encrypted.")
            elif algorithm == 2: #Somma
                encrypted = c.algorithmAdd()
                encA = "files/encrypted/encA_SUM"
                encAB = "files/encrypted/encAB_SUM"
                output(out_lck, "Encrypted.")
            elif algorithm == 3: #Shift
                encrypted = c.encryptShift()
                output(out_lck, "Shift!")
                encA = "files/encrypted/encA_SHIFT"
                encAB = "files/encrypted/encAB_SHIFT"
                output(out_lck, "Encrypted.")
            elif algorithm == 4: #Mul
                keysA = gen_keys2(keyA, len(chunks))
                output(out_lck, "Encrypted.")
                # cifro e salvo di nuovo
                c = Cipher(out_lck, chunks, keysA)
                encrypted = c.encryptMul8()
                encA = "files/encrypted/encA_MUL"
                encAB = "files/encrypted/encAB_MUL"
                output(out_lck, "Encrypted.")


            #Zotti
            elif algorithm == 5: #Exponential
                c = Cipher(out_lck, chunks, 0)
                encrypted = c.encryptMOD(10, 257)
                encA = "files/encrypted/encA_MOD"
                encAB = "files/encrypted/encAB_MOD"
                output(out_lck, "Encrypted.")
            #-Zotti


            #Scrivo il file criptato con keyA
            fout = open(encA, "wb+")

            for chunk in encrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()

            # invio file cifrato con keyA
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((_base + host, port))


            send_file(sock, encA)
            output(out_lck, "Sent to Bob.\n")
            # ricevo file cifrato con keyB

            output(out_lck, "Waiting for Bob...")
            recv_file(sock, encAB)

            if algorithm != 5:
                output(out_lck, "\nDecrypting with Alice's key '%s'..." % keyA)
            else:
                output(out_lck, "\nDecrypting..")

            if algorithm != 4 and algorithm != 5:
                # decifro con la keyA
                chunks = get_chunks(encAB, 64)
                c = Cipher(out_lck, chunks, keysA)

            elif algorithm == 4:
                chunks = get_chunks(encAB, 32)
                c = Cipher(out_lck, chunks, keysA)


            #Zotti
            elif algorithm == 5:
                chunks = get_chunks(encAB, 8)
            #-Zotti


            # algoritmo di decifratura con keyA
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
            elif algorithm == 4: #Mul
                decrypted = c.decryptMul32()
                decA = "received/encB_MUL"

            #Zotti
            elif algorithm == 5: #Exponential
                c.chunks = chunks
                decrypted = c.decryptMOD()
                decA = "received/encB_MOD"
            #-Zotti

            fout = open(decA, "wb+")
            for chunk in decrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()

            send_file(sock, decA)

            output(out_lck, "Sent encrypted file with Bob's key...")
            output(out_lck, "\n\nDone!\n\n")
            sock.close()

        #BOB

        elif main_menu == 2:
            if network == 2:
                host = loop_input(out_lck, "Insert destination IP:")

            if algorithm != 5:
                keyB = loop_input(out_lck, "Insert key: ")  # key Bob

            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock.bind(('', port))
            sock.listen(100)
            output(out_lck, 'Waiting for Alice...')

            (client_sock, address) = sock.accept()

            # ricevo file cifrato con keyA e cifro di nuovo con la keyB
            result = recv_file(client_sock, "received/encA")



            if algorithm == 4:
                output(out_lck, "Getting 16 bit chunks...")
                chunks = get_chunks("received/encA", 16)
                output(out_lck, "Encrypting with Bob's key '%s'..." % keyB)
                keysB = gen_keys2(keyB, len(chunks))
                c = Cipher(out_lck, chunks, keysB)

            #Zotti
            elif algorithm == 5:
                output(out_lck, "Getting 8 bit chunks...")
                chunks = get_chunks("received/encA", 8)
                c = Cipher(out_lck, chunks, 0)
            #-Zotti

            else:
                output(out_lck, "Getting 64 bit chunks...")
                chunks = get_chunks("received/encA", 64)
                output(out_lck, "Encrypting with Bob's key...")
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
                encAB = "received/encAB_Shift"
                encB = "received/encB_Shift"
            elif algorithm == 4:
                encrypted = c.encryptMul16()
                encAB = "received/encAB_MUL"
                encB = "received/encB_MUL"

            #Zotti
            elif algorithm == 5: #Exponential
                encrypted = c.encryptMOD(11, 257)
                encAB = "received/encAB_MOD"
                encB = "received/encB_MOD"
            #-Zotti

            output(out_lck, "Encrypted.")

            fout = open(encAB, "wb+")

            for chunk in encrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()

            output(out_lck, "Sending encrypted file with Bob and Alice's key...")
            send_file(client_sock, encAB)

            output(out_lck, "Waiting for Bob...")

            # ricevo file cifrato con keyB
            recv_file(client_sock, encB)

            if algorithm != 4 and algorithm != 5:
                chunks = get_chunks(encB, 64)
                c = Cipher(out_lck, chunks, keysB)
            elif algorithm == 4:
                chunks = get_chunks(encB, 16)
                c = Cipher(out_lck, chunks, keysB)

            #Zotti
            elif algorithm == 5:
                chunks = get_chunks(encB, 8)
            #-Zotti

            output(out_lck, "Decrypting with Bob's key...")

            #algoritmo di decifratura
            if algorithm == 1: #XOR
                decrypted = c.decryptXOR()
                fname = "received/decrypted_XOR.gif"
            elif algorithm == 2: #Somma
                decrypted = c.algorithmDiff()
                fname = "received/decrypted_SUM.png"
            elif algorithm == 3: #Shift
                decrypted =c.decryptShift()
                fname = "received/decrypted_Shift.jpg"
            elif algorithm == 4: #Mul
                decrypted = c.decryptMul16()
                fname = "received/decrypted_MUL.mp3"

            #Zotti
            elif algorithm == 5: #Exponential
                c.chunks = chunks
                decrypted = c.decryptMOD()
                fname = "received/decrypted_MOD.mp4"
            #-Zotti

            output(out_lck, "Decrypted.")


            fout = open(fname, "wb+")

            for chunk in decrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())

            fout.close()
            sock.close()
            output(out_lck, "\n\nDone!\n\n")










