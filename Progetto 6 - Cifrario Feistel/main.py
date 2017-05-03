import os
import re
import threading
import time

from bitarray import bitarray

from helpers import netutils
from helpers.blowfish import Blowfish
from helpers.cipher import Cipher
from helpers.key_gen import *
from helpers.tea import tea_encryptfile, tea_decryptfile
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
                                                                                               "Brute Forse"])

        if main_menu == 1:

            host = loop_input(out_lck, "Insert destination ip:")

            key = loop_int_input(out_lck, "Insert base key:")
            keyb = toBinary(int(key))

            i = 1
            fileList = []
            for file in os.listdir("files"):
                output(out_lck, "%s %s" % (i, file))
                fileList.append(str(file))
                i += 1

            nfile = loop_int_input(out_lck, "Choose file")
            nf = int(nfile) - 1
            filename = copy.copy(fileList[nf])

            method = loop_menu(out_lck, "Select encryption method:", ["DES", "Blowfish", "TEA"])

            if method == 1:
                # prendo chunks di lunghezza chunk_len
                chunks = get_chunks("files/" + filename, 64)
                c = Cipher(out_lck, chunks, keyb)

                output(out_lck, "Encrypting file...")
                c.encrypt()
                output(out_lck, "File encrypted")

                data = b''
                for chunk in c.encrypted:
                    data += bitarray(chunk).tobytes()

                output(out_lck, "Sending file...")
                UDPclient(out_lck, _base + host, 60000, data)
                output(out_lck, "File sent")

            elif method == 2:

                chunks = get_chunks("files/" + filename, 64)
                b = Blowfish(out_lck, chunks, keyb)

                output(out_lck, "Encrypting file...")
                b.encrypt()
                output(out_lck, "File encrypted")
                data = b''
                for chunk in b.encrypted:
                    data += bitarray(chunk).tobytes()

                output(out_lck, "Sending file...")
                UDPclient(out_lck, _base + host, 60000, data)
                output(out_lck, "File sent")

            elif method == 3:

                keys = gen_16key32(out_lck, keyb)
                output(out_lck, "Encrypting file with TEA...")
                c = tea_encryptfile("files/" + filename, keys)
                output(out_lck, "Sending file...")
                UDPclient(out_lck, '', '', c)
                output(out_lck, "TEA file sent.")

        elif main_menu == 2:

            port = 60000

            UDPserver(out_lck, port)

            chunks = get_chunks("received/" + "UDPReceived", 64)

            key = loop_int_input(out_lck, "Insert key to decrypt:")
            keyb = toBinary(int(key))

            method = loop_menu(out_lck, "Select encryption method:", ["DES", "Blowfish", "TEA"])

            if method == 1:

                c = Cipher(out_lck, chunks, keyb)

                output(out_lck, "Decrypting file...")
                c.decrypt()
                output(out_lck, "File decrypted")

                fout = open("received/decrypted_des.jpg", "wb")

                for chunk in c.decrypted:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())

                fout.close()

                output(out_lck, "File saved")

            elif method == 2:

                b = Blowfish(out_lck, chunks, keyb)

                output(out_lck, "Decrypting file...")
                b.decrypt()
                output(out_lck, "File decrypted")

                fout = open("received/decrypted_blowfish", "wb")

                for chunk in b.decrypted:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())

                fout.close()

                output(out_lck, "File saved")

            elif method == 3:

                keys = gen_16key32(out_lck, keyb)
                output(out_lck, "Starting to decrypt with TEA...")
                tea_decryptfile('received/decrypted_tea', keys)
                output(out_lck, "Decrypted!")

        #bruteforce
        elif main_menu == 3:

            start = time.time()

            chunks = get_chunks("received/" + "UDPReceived", 64)

            #chunks = get_chunks("files/" + "800px-Periodic_table_simple_it_bw_(LCC_0).png", 64)

            for i_key in range(0, 256, 1):
                #print('chiave provata: ', i_key)
                c = Cipher(out_lck, chunks, toBinary(int(i_key)))
                n = c.decrypt_brute_force()
                if n != 0:
                    # trovato il formato del file, smetto di provare nuove chiavi
                    break
                else:
                    print("not valid key ", i_key, "\n")

            if n == 0:
                print("not found valid key")
            elif n == 1:
                fout = open("received/decrypted2.png", "wb")
                print("decrypted with key: ", i_key)

                for chunk in c.decrypted:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())

            elif n == 2:
                fout = open("received/decrypted2.jpg", "wb")
                print("decrypted with key: ", i_key)

                for chunk in c.decrypted:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())

            elif n == 3:
                fout = open("received/decrypted2.bmp", "wb")
                print("decrypted with key: ", i_key)

                for chunk in c.decrypted:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())

            stop = time.time() - start

            print("done, decode timer: ", stop, " seconds")

        #Arp Poisoner
        elif main_menu == 4:
            netutils.arpoisoner(out_lck, 'enx9cebe811a79a')

        #Sniffer
        elif main_menu == 5:

            encr = loop_input(out_lck, "Insert name for file Ex. 'tea' will output 'sniff_tea'")

            timeout = loop_input(out_lck, "Insert a timeout for the sniffer.")

            netutils.sniffer(out_lck, timeout, '60000', 'enx9cebe811a79a ', encr)

            i = 1
            fileList = []
            for file in os.listdir("sniffed"):
                output(out_lck, "%s %s" % (i, file))
                fileList.append(str(file))
                i += 1

            nfile = loop_int_input(out_lck, "Choose file")
            nf = int(nfile) - 1
            filename = "sniffed/" + copy.copy(fileList[nf])

            chunks = get_chunks(filename, 64)

            key = loop_int_input(out_lck, "Insert key to decrypt:")
            keyb = toBinary(int(key))

            method = loop_menu(out_lck, "Select encryption method:", ["DES", "Blowfish", "TEA"])

            #des
            if method == 1:

                c = Cipher(out_lck, chunks, keyb)

                output(out_lck, "Decrypting file...")
                c.decrypt()
                output(out_lck, "File decrypted")

                fout = open("sniffed/decrypted/decrypted_des.jpg", "wb")

                for chunk in c.decrypted:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())

                fout.close()

                output(out_lck, "File saved")

            #blowfish
            elif method == 2:

                b = Blowfish(out_lck, chunks, keyb)

                output(out_lck, "Decrypting file...")
                b.decrypt()
                output(out_lck, "File decrypted")

                fout = open("sniffed/decrypted/decrypted_blowfish.jpg", "wb")

                for chunk in b.decrypted:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())

                fout.close()

                output(out_lck, "File saved")

            #TEA
            elif method == 3:

                keys = gen_16key32(out_lck, keyb)
                output(out_lck, "Starting to decrypt with TEA...")
                tea_decryptfile(filename, "sniffed/decrypted/decrypted_TEA.jpg", keys)
                output(out_lck, "Decrypted!")
