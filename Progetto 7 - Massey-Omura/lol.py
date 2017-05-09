import threading, os, copy

from bitarray import *
from helpers.utils import loop_menu, loop_input, output, loop_int_input, get_chunks, gen_keys
from helpers.connection import UDPserver, UDPclient
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

            chunks = get_chunks("files/" + filename, 64)
            keysA = gen_keys(keyA, len(chunks))

            output(out_lck, "Cifro con key Alice %s..." % keyA)

            # cifro e salvo di nuovo
            c = Cipher(out_lck, chunks, keysA)
            encrypted = c.encryptXOR()
            output(out_lck, "Cifrato con key Alice: %s" % keyA)

            fout = open("files/encrypted/encA", "wb+")

            for chunk in encrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()

            # invio file cifrato con keyA
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((_base + host, port))

            output(out_lck, "Invio file cifrato con key Alice...")
            send_file(sock, "files/encrypted/encA")

            output(out_lck, "Aspetto Bob...")
            # ricevo file cifrato con keyB
            recv_file(sock, "received/encAB")

            output(out_lck, "Decifro con key Alice %s..." % keyA)
            # decifro con la keyA
            chunks = get_chunks("received/encAB", 64)
            c = Cipher(out_lck, chunks, keysA)
            decrypted = c.decryptXOR()
            output(out_lck, "Decifrato con key Alice.")

            fout = open("received/encB", "wb+")

            for chunk in decrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()

            output(out_lck, "Invio cifrato con key Bob...")
            send_file(sock, "received/encB")
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

            output(out_lck, "Ricevo cifrato di Alice...")

            # ricevo file cifrato con keyA e cifro di nuovo con la keyB
            recv_file(client_sock, "received/encA")

            chunks = get_chunks("received/encA", 64)

            output(out_lck, "Cifro con key Bob %s..." % keyB)

            keysB = gen_keys(keyB, len(chunks))
            c = Cipher(out_lck, chunks, keysB)

            encrypted = c.encryptXOR()
            output(out_lck, "Cifrato con key Bob %s." % keyB)

            fout = open("received/encAB", "wb+")

            for chunk in encrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()

            output(out_lck, "invio cifrato con keyA e keyB")
            send_file(client_sock, "received/encAB")

            output(out_lck, "ricevo cifrato con keyB")
            # ricevo file cifrato con keyB
            recv_file(client_sock, "received/encB")

            chunks = get_chunks("received/encB", 64)

            output(out_lck, "decifro con keyB")
            c = Cipher(out_lck, chunks, keysB)
            decrypted = c.decryptXOR()
            output(out_lck, "decifrato con keyB")

            fout = open("received/decrypted.jpg", "wb+")

            for chunk in decrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()
        sock.close()










