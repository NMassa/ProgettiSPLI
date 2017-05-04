import threading
from bitarray import bitarray
from helpers.key_gen import *
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

            output(out_lck,"Insert Key : ")
            keya = input() #key Alice

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

            output(out_lck, "Encrypting file...")
            # TODO: encrypt function

            data = b''
            for chunk in encrypted:
                data += bitarray(chunk).tobytes()

            output(out_lck, "Sending file...")
            UDPclient(out_lck, _base + host, 60000, data)
            output(out_lck, "File sent")

            # TODO: si rimette in ascolto per ricevere file criptato con seconda chiave e decriptarlo con la propria
            # TODO: lo re-invia nuovamente


        elif main_menu == 2:

            output(out_lck, "Insert Key : ")
            keyb = input() #key Bob

            port = 60000

            UDPserver(out_lck, port)

            chunks = get_chunks("received/UDPReceived", 64)

            # TODO: encrypt function
            output(out_lck, "Decrypting file...")

            fout = open("...", "wb+")

            for chunk in encrypted:
                ba = bitarray(chunk)
                fout.write(ba.tobytes())

            fout.close()
            output(out_lck, "File saved")

            # TODO: manda il file nuovamente con la nuova chiave applicata
            # TODO: ascolta, riceve file, decripta con propria chiave e taaaaakkkk
