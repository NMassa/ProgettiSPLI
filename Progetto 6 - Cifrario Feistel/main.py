import os
import re
import threading
import time

from bitarray import bitarray
from helpers.blowfish import Blowfish
from helpers.blowfish_2 import Blowfish2
from helpers.cipher import Cipher
from helpers.key_gen import *
from helpers.tea import teaCipher
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
                                                                                               "Feistel cipher",
                                                                                               "Blowfish method",
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

        elif main_menu == 4:

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

            with open('files/' + filename, 'rb') as content_file:
                content = content_file.read()

            a = Blowfish2.encrypt(keyb, content)
            output(out_lck, "Encrypting file...")
            out_file1 = open("received/blowfish_crypted.jpg", "wb")
            out_file1.write(a)
            out_file1.close()
            output(out_lck, "\nFile encripted ...")

            method = loop_menu(out_lck, "Select dencryption method:", ["Key", "Bruteforce"])

            if method == 1:

                key = loop_int_input(out_lck, "Insert base key:")
                keyb = toBinary(int(key))
                b = Blowfish2.decrypt(keyb, a)
                output(out_lck, "\nStart decryptation...")
                out_file2 = open("received/blowfish_decrypted.jpg", "wb")
                out_file2.write(b)
                out_file2.close()

                output(out_lck, "\nFinish decryptation. Check files received.\n")
                '''check
                out_file2 = open("received/blowfish_decrypted.jpg", "rb")
                ciao = out_file2.read(5)
                print(ciao)'''
                output(out_lck, "Press enter to continue")
                input()

            elif method == 2:
                for i in range(1, 10000):
                    keya = toBinary(int(i))
                    b = Blowfish2.decrypt(keya, a)
                    data = b[:3]
                    print("Try key : ", i)
                    if data == b'\xff\xd8\xff':
                        print("Found key : ", i)
                        keya = toBinary(int(i))
                        b = Blowfish2.decrypt(keya, a)
                        output(out_lck, "\nStart decryptation...")
                        out_file2 = open("received/blowfish_decrypted.jpg", "wb")
                        out_file2.write(b)
                        out_file2.close()
                        output(out_lck, "\nFinish decryptation. Check files received.\n")
                    else:
                        i += 1


        elif main_menu == 3:

            key = str(random.randrange(0, 256))
            keyb = toBinary(int(key))

            # chunks = get_chunks("piedpiper.jpg", 64)

            c = teaCipher(out_lck, "piedpiper.jpg", keyb)
            c.teaencrypt()
            c.teadecrypt()
            '''
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
            '''
        elif main_menu == 5:

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
                    print("not valide key ", i_key, "\n")

            if n == 0:
                print("not found valide key")
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
