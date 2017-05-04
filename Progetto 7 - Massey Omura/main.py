import os
import re
import threading
import time

from bitarray import bitarray

from helpers import netutils
from helpers.blowfish import Blowfish
from helpers.cipher import Cipher
from helpers.key_gen import *
from helpers.tea import *
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
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Generate keys",
                                                                                               "Send file",
                                                                                               "Receive file",
                                                                                               "Brute Force"])
