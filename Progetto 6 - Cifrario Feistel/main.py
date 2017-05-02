import os
import re
import threading

from bitarray import bitarray

from helpers.cipher import Cipher
from helpers.feistel import *
from helpers.utils import *
from helpers.connection import *


_base = "192.168."

if __name__ == "__main__":

    out_lck = threading.Lock()

    ip = loop_input(out_lck, "Insert your IP: ")
    my_ip = _base + ip

    output(out_lck, "Your IP: " + my_ip)
    while True:
        # Main Menu
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Send file",
                                                                                               "Receive file",
                                                                                               "Feistel cipher"])

        if main_menu == 1:

            host = loop_input(out_lck, "Insert destination ip:")

            UDPclient(out_lck, _base + host, 60000)

        elif main_menu == 2:

            port = 60000
            output(out_lck, "Listening on port %s..." % port)
            received = UDPserver(out_lck, port, "jpg")

        elif main_menu == 3:

            key = str(random.randrange(0, 256))
            keyb = toBinary(int(key))

            c = Cipher(out_lck, "piedpiper.jpg", keyb)

            c.encrypt()

            print("encrypted")

            c.decrypt()

            print("decrypted")

            fout = open("received/decrypted.jpg", "wb")

            for chunk in c.decrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())

            fout.close()

            print("done")