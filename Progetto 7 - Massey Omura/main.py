import threading
from bitarray import bitarray
from helpers.cipher import Cipher
from helpers.connection import *
from helpers.utils import *

_base = "192.168."

if __name__ == "__main__":

    out_lck = threading.Lock()

    ip = loop_input(out_lck, "Insert your IP: ")
    my_ip = _base + ip

    output(out_lck, "Your IP: " + my_ip)
    while True:
        # Main Menu
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Send file",
                                                                                               "Receive file"])
        if main_menu == 1:

            host = loop_input(out_lck, "Insert destination ip:")

            output(out_lck, "Insert Key : ")
            keyA = input()  # key Alice

            i = 1
            fileList = []
            for file in os.listdir("files"):
                output(out_lck, "%s %s" % (i, file))
                fileList.append(str(file))
                i += 1

            nfile = loop_int_input(out_lck, "Choose file")
            nf = int(nfile) - 1
            filename = copy.copy(fileList[nf])
            chunks = get_chunks("files/" + filename, 64)

            # manda file cripatato con chiave keya e si rimette in ascolto
            send_file_crypt(chunks, keyA, _base, host)

            # si rimette in ascolto per ricevere file criptato con seconda chiave e decriptarlo con la propria
            port = 60000
            UDPserver(out_lck, port)
            chunks = get_chunks("received/UDPReceived", 64)

            # lo re-invia nuovamente decriptato con la propria chiave
            send_file_decrypt(chunks, keyA, _base, host)

        elif main_menu == 2:

            host = loop_input(out_lck, "Insert destination ip:")
            output(out_lck, "Insert Key : ")
            keyB = input()  # key Bob

            port = 60000
            UDPserver(out_lck, port)
            chunks = get_chunks("received/UDPReceived", 64)

            # manda il file nuovamente con la nuova chiave applicata
            send_file_crypt(chunks, keyB, _base, host)

            # ascolta, riceve file, decripta con propria chiave e taaaaakkkk
            UDPserver(out_lck, port)
            chunks = get_chunks("received/UDPReceived1", 64)

            # decripta il file che dovrebbe avere applicata solamente la chiave di Bob
            c = Cipher(out_lck, chunks, keyB)
            output(out_lck, "Decrypting file...")
            c.decrypt()
            output(out_lck, "File decrypted")

            fout = open("received/decrypted.jpg", "wb+")
            for chunk in c.decrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())
            fout.close()
            output(out_lck, "File saved")
