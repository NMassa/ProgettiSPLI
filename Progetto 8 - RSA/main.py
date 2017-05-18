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

        # Main Menu
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Send file",
                                                                                               "Receive file"])
        if main_menu == 1:
            if network == 2:
                host = loop_input(out_lck, "Insert destination IP:")













