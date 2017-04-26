import os
import re
import threading
import queue

from helpers import bruteforce, ccypher
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

            output(out_lck, "Insert destination ip:")
            host = input()

            connect(host, 60000)

        elif main_menu == 2:

            port = 60000
            output(out_lck, "Listening on port %s..." % port)
            received = listen(port)

        elif main_menu == 3:
            arpoisoner(out_lck)
        elif main_menu == 4:
            # Analizzo il traffico
            analyzer(out_lck)

            # DEBUG
            received = open("received/pwndcifrato.txt", "rb")
            # -DEBUG

            # Seleziono metodo di decifratura
            decipher = loop_menu(out_lck, "Select deciphering method ('e' to exit): ", ["Decipher with key",
                                                                                        "Brute Force",
                                                                                        "Frequency"])
            if decipher == 1:
                key = loop_int_input(out_lck, "Insert decription key:")
                cyphered = received.read()

                deciphred = ccypher.full_decaesar(cyphered, key)

                fout = open("received/pwndecifrato.txt", "w")
                fout.write(deciphred)
                fout.close()

            elif decipher == 2:
                list = None

                # Ci mette una vita la facciamo prima e bona
                # Creazione dizionario
                # dictionary = open("helpers/dict.txt", "w")
                #
                # for filename in os.listdir("books"):
                #
                #     fop = open("books/%s" % filename, "r")
                #     for line in fop.readlines():
                #         lst = re.findall(r"[\w']+", line)
                #         for sublst in lst:
                #             if sublst:
                #                 if len(sublst) > 1:             #qui ho eliminato le "parole" di un solo carattere che venivano splittati dalle regular
                #                     dictionary.write("%s\n" % sublst)
                #     fop.close()
                #
                # dictionary.close()

                file = open("helpers/dict.txt", "rt")
                dict = set()

                for l in file.readlines():
                    dict.add(l.strip())

                output(out_lck, "Loaded dictionary of %s words" % len(dict))

                output(out_lck, "Starting brute force")

                cyphered = received.read()

                threads = []
                results = []
                queue = queue.Queue()
                max_res = None

                for i in range(1, 27):
                    t = threading.Thread(target=bruteforce.bruteforce, args=(out_lck, cyphered, dict, i, queue))
                    t.start()
                    threads.append(t)
                    results.append(queue.get())
                    # bf = bruteforce.Bruteforce(out_lck, cyphered, dict, i, results)
                    # bf.start()
                    # threads.append(bf)

                for t in threads:  # Aspetta la terminazione dei thread in esecuzione
                    t.join()

                for r in results:
                    output(out_lck, "Shift %s accuracy: %s" % (r['shift'], r['accuracy']))
                    if max_res is None:
                        max_res = r
                    else:
                        if max_res['accuracy'] < r['accuracy']:
                            max_res = r

                output(out_lck, "Maximum accuracy %s with shift %s" % (max_res['accuracy'], max_res['shift']))
                output(out_lck, "%s is the most probable deciphering key" % max_res['shift'])

            elif decipher == 3:
                decipher = loop_menu(out_lck, "Select one option ('e' to exit): ", ["Generate letter frequency",
                                                                                    "Decipher"])
                received = open("received/cifrato.txt","rb")
                f = frequency.Frequency(received)
                if decipher == 1:
                    f.letter_frequency()
                    f.crypt_file_frequency(received)

                elif decipher == 2:
                    key = f.frequency_compare()
                    #if key == None:
                     #   print ('Sorry but unacceptable rate, try bruteforce to decode the file \n')
                    #else:
                    cyph = received.read()
                    key1 = int(key)
                    deciphred_freq = ccypher.decaesar(cyph,key1)
                    fout = open("received/decifrato_freq.txt", "w")
                    fout.write(deciphred_freq)
                    fout.close()