import os
import re
import threading

from bitarray import bitarray

from helpers import tea
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
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Send file",
                                                                                               "Receive file",
                                                                                               "Feistel cipher"])

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

                print("blowfish")
                chunks = get_chunks("files/" + filename, 64)
                b = Blowfish(out_lck, chunks, keyb)

                output(out_lck, "Encrypting file...")
                b.encrypt()
                output(out_lck, "File encrypted")
                data = b''
                for chunk in b.encrypted:
                    data += bitarray(chunk).tobytes()

                print(data)
                output(out_lck, "Sending file...")
                UDPclient(out_lck, _base + host, 60000, data)
                output(out_lck, "File sent")

            elif method == 3:

                print("tea")

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

                print("blowfish")

                fout = open("received/decrypted_blowfish.jpg", "wb")


            elif method == 3:

                print("tea")

                fout = open("received/decrypted_tea.jpg", "wb")


        elif main_menu == 3:

            key = str(random.randrange(0, 256))
            keyb = toBinary(int(key))

            #chunks = get_chunks("piedpiper.jpg", 64)
            #key = get_key('Random Text or Something')
            c = teaCipher(out_lck, "piedpiper.jpg",keyb)
            c.teaencrypt()

"""
            #c.encrypt()

            #print("encrypted")

            #c.chunks = c.encrypted

            #c.decrypt()

            #print("decrypted")

            fout = open("received/decrypted.jpg", "wb")

            for chunk in c.decrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())

            fout.close()

            print("done")
"""