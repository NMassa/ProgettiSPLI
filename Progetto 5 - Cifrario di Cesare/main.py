import threading
import sys
from helpers.utils import *
from helpers.connection import *
from helpers.netutils import arpoisoner
from helpers.netutils import analyzer
import frequency

_base = "192.168."

if __name__ == "__main__":

    out_lck = threading.Lock()

    ip = loop_input(out_lck, "Insert your IP: ")
    my_ip = _base + ip

    output(out_lck, "Your IP: " + my_ip)
    while True:
        # Main Menu
        logo()
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Send file",
                                                                                               "Receive file",
                                                                                               "Arp poisoninig",
                                                                                               "Sniff & Decypher"])
        if main_menu == 1:
            print("invio file cifrato")
            connect(my_ip, 60000)

        elif main_menu == 2:
            print("ricevo file cifrato")
            #TODO: ricevo file cifrato
            received = listen(60000)



            #TODO: decifro file con la chiave

        elif main_menu == 3:
            arpoisoner(out_lck)
        elif main_menu == 4:
            # Analizzo il traffico
            #analyzer(out_lck)

            # TODO: Terminata l'analisi deve restituire un file con il testo cifrato

            # DEBUG
            received = open("received/cifrato.txt", "rb")
            # -DEBUG


            # Seleziono metodo di decifratura
            decipher = loop_menu(out_lck, "Select deciphering method ('e' to exit): ", ["Decipher with key",
                                                                                        "Brute Force",
                                                                                        "Frequency"])
            if decipher == 1:
                key = loop_int_input(out_lck, "Insert decription key:")
            elif decipher == 2:
                # TODO: creo dizionario dai file (tutti tranne quello appena ricevuto!)
                # file dict.txt nella cartella helpers

                file = open("helpers/words.txt", "r")
                dict = set()

                for l in file.readlines():
                    dict.add(l.lower().strip())

                output(out_lck, "Created dictionary of %s words" % len(dict))

                output(out_lck, "Starting brute force")

                cyphered = received.read()

                for i in range(1, 26):
                    text = caesar(cyphered, i)

                    fout = open("bruteforce/file" + str(i) + ".txt", "wt")
                    fout.write(text)
                    fout.close()

            elif decipher == 3:
                decipher = loop_menu(out_lck, "Select one option ('e' to exit): ", ["Generate letter frequency",
                                                                                    "Decipher"])
                f = frequency.Frequency(file)
                if decipher == 1:
                    f.letter_frequency()
                elif decipher == 2:
                    f.frequency_compare()