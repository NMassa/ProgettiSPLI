import threading
import sys
from helpers.utils import *
from helpers.netutils import arpoisoner
from helpers.netutils import analyzer

_base = "192.168."

if __name__ == "__main__":

    out_lck = threading.Lock()

    ip = loop_input(out_lck, "Insert your IP: ")
    my_ip = _base + ip

    output(out_lck, "Your IP: " + my_ip)
    while True:
        # Main Menu

        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", [  "Send file",
                                                                                                 "Receive file",
                                                                                                 "Execute Order 66" ])
        if main_menu == 1:
            print("invio file cifrato")
        elif main_menu == 2:
            decipher = loop_menu(out_lck, "Select deciphering method ('e' to exit): ", [ "Decipher with key",
                                                                                         "Brute Force",
                                                                                         "Frequency"])
            if decipher == 1:
                key = loop_int_input(out_lck, "Insert decription key:")
            elif decipher == 2:
                print("pwned")
            elif decipher == 3:
                print("chissà")
        elif main_menu == 3:
            option = loop_menu(out_lck, "Select one option ('e' to exit): ", ["Arp Poisoner",
                                                                                        "Analyzer"])
            if option == 1:
                arpoisoner(out_lck)
            elif option == 2:
                analyzer(out_lck)
