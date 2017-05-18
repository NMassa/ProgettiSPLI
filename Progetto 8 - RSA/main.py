import threading
from helpers import mysocket
from helpers.utils import loop_menu, loop_input, output, loop_int_input, get_dir_list
from helpers.netutils import arpoisoner, analyzer

_base = "192.168."
host = 0


if __name__ == "__main__":

    out_lck = threading.Lock()
    network = 0
    port = 60000
    fileExt = "mp3"

    #Get the network...
    while network == 0:
        network = loop_menu(out_lck, "Select network enviroment ('e' to exit): ", ["Local", "Network"])
        if network == 1:
            _base = "127.0.0."
            host = "1"
        elif network == 2:
            ip = loop_input(out_lck, "Insert your IP: ")
            my_ip = _base + ip
            output(out_lck, "Your IP: " + my_ip)

    while True:
        # Main Menu
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Send file",
                                                                                               "Receive file",
                                                                                               "ARP poisoner",
                                                                                               "Sniffer"])
        if main_menu == 1:
            if network == 2:
                host = loop_input(out_lck, "Insert destination IP:")

            #Inizializzo socket
            sock = mysocket.MySocket()

            # Get filenames
            filename = get_dir_list(out_lck, "files")


            #Il file deve essere nella cartella files
            sock.sendfile(out_lck, sock, _base + host, port, filename)
            output(out_lck, "File sent!\n")

        elif main_menu == 2:
            sock = mysocket.MySocket()

            #il file verrà salvato nella cartella received con l'estensione indicata
            sock.receivefile(out_lck, sock, port, "asd", fileExt)
            output(out_lck, "Done!\n")

        elif main_menu == 3:
            arpoisoner(out_lck, _base + host)

        elif main_menu == 4:
            analyzer(out_lck, port, fileExt)








