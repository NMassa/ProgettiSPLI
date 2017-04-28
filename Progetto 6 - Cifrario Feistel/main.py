import os
import re
import threading
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
                                                                                               "Receive file",])
        if main_menu == 1:

            output(out_lck, "Insert destination ip:")
            host = input()

            connect(out_lck, _base + host, 60000)

        elif main_menu == 2:

            port = 60000
            output(out_lck, "Listening on port %s..." % port)
            received = listen(out_lck, port)


