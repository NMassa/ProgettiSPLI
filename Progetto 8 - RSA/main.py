import threading
from helpers import mysocket
from helpers.utils import loop_menu, loop_input, output, loop_int_input, get_dir_list, read_in_chunks
from helpers.netutils import arpoisoner, analyzer

_base = "192.168."
host = 0


if __name__ == "__main__":

    out_lck = threading.Lock()
    network = 0
    port = 3000

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

            #Send the key
            key_input = loop_input(out_lck, "Please insert a Key..")
            sock.connect(_base + host, port)
            sock.send_key(out_lck, sock, key_input, len(key_input))

            #Cipher
            #for piece in read_in_chunks(filename, 128):                #chunks da 128 bytes
                #output(out_lck, "JUST DO IT")       #TODO: encryption

            #Il file deve essere nella cartella files
            sock.sendfile(out_lck, sock, filename)
            output(out_lck, "File sent!\n")

        elif main_menu == 2:
            sock = mysocket.MySocket()
            sock.bind('', port)
            sock.listen(5)
            key, lenght_key, new_sock = sock.recv_key(out_lck, sock)           # la key è in bytes: per avere una stringa bytes(key).decode('utf-8')

            #il file verrà salvato nella cartella received con l'estensione indicata
            new_sock.receivefile(out_lck, new_sock, "asd")
            output(out_lck, "Done!\n")
        elif main_menu == 3:
            arpoisoner(out_lck)

        elif main_menu == 4:
            analyzer(out_lck, port)








