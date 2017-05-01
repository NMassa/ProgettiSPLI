import os
import re
import threading

from helpers.feistel import *
from helpers.utils import *
from helpers.connection import *
from helpers.cipher import Cipher


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

            connect(out_lck, _base + host, 60000)

        elif main_menu == 2:

            port = 60000
            output(out_lck, "Listening on port %s..." % port)
            received = listen(out_lck, port)

        elif main_menu == 3:

            output(out_lck, "Feistel")

            key = str(random.randrange(0, 256))
            keyb = toBinary(int(key))

            cipher = Cipher("piedpiper.jpg", key)

            cipher.encode()


