import threading

from bitarray import bitarray

from helpers import mysocket, cipher, utils
from helpers.utils import loop_menu, loop_input, output, loop_int_input, get_dir_list, get_chunks, \
    write_decrypted_from_chunks, write_encrypted_from_chunks, get_chunks_8bit, factoring
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
                                                                                               "Fermat",
                                                                                               "Bruteforce"])
        if main_menu == 1:
            if network == 2:
                host = loop_input(out_lck, "Insert destination IP:")

            #Inizializzo socket
            sock = mysocket.MySocket()

            # Get filenames
            filename = get_dir_list(out_lck, "files")

            # Generate keys
            bits_keys = loop_menu(out_lck, "Select one of the following algorithm ('e' to exit): ", ["8 bits",
                                                                                                   "128 bits"])
            if bits_keys == 1:
                # Get Chunks
                chunks = get_chunks_8bit(out_lck, 'files/' + filename, 1)  # qui va in bytes
                c = cipher.Cipher(out_lck, chunks, 0, 16)
                key_input = utils.toBinary16(c.d) + '@' + utils.toBinary16(c.n)
                leng = 2

            else:
                # Get Chunks
                chunks = get_chunks(out_lck, 'files/' + filename, 8)  # qui va in bytes
                c = cipher.Cipher(out_lck, chunks, 0, 128)
                key_input = utils.toBinary128(c.d) + '@' + utils.toBinary128(c.n)
                leng = 16

            #Send the key
            #key_input = loop_input(out_lck, "Please insert a Key..")
            sock.connect(_base + host, port)

            #key_input = utils.toBinary128(c.d) + '@' + utils.toBinary128(c.n)
            sock.send_key(out_lck, sock, key_input, len(key_input))
            output(out_lck, "Key Sent.\nEncrypting file with %d key.." % c.e)

            encrypted_chunks = c.signature_encrypt(c.e, c.n)
            enc_file = write_encrypted_from_chunks(encrypted_chunks, "RSA", leng)

            #Il file deve essere nella cartella files
            sock.sendfile(out_lck, sock, enc_file)
            output(out_lck, "File sent!\n")
            sock.close()

        elif main_menu == 2:
            sock = mysocket.MySocket()
            sock.bind('', port)
            sock.listen(5)

            pkey, mod, lenght_key, new_sock = sock.recv_key(out_lck, sock)           # la key è in bytes: per avere una stringa bytes(key).decode('utf-8')

            bits_keys = loop_menu(out_lck, "Select one of the following algorithm ('e' to exit): ", ["8 bits",
                                                                                                     "128 bits"])

            enc_filename = new_sock.receivefile(out_lck, new_sock, "enc")

            if bits_keys == 1:
                # Get Chunks
                chunks = get_chunks_16bit(out_lck, enc_filename, 2)  # qui va in bytes
                c = cipher.Cipher(out_lck, chunks, 0, 16)
                lenght = 1

            elif bits_keys == 2:
                # Get Chunks
                chunks = get_chunks(out_lck, enc_filename, 16)  # qui va in bytes
                c = cipher.Cipher(out_lck, chunks, 0, 128)
                lenght = 8

            #il file verrà salvato nella cartella received con l'estensione indicata

            decrypted_chunks = c.signature_decrypt(pkey, mod)

            write_decrypted_from_chunks(decrypted_chunks, lenght)

            output(out_lck, "Done!\n")
            sock.close()
            new_sock.close()

        elif main_menu == 3:
            arpoisoner(out_lck)

        elif main_menu == 4:
            output(out_lck, "Fermat Factorization Attack")

            #TODO: recupero (e,n) in base a chi voglio attaccare

            n = 1189
            e = 9629

            d = factoring(out_lck, n, e)

            #TODO: decifro file con d

        elif main_menu == 5:
            output(out_lck,"\n Start Bruteforce")
            output(out_lck,"\nInsert public mod : ")
            mod = input()
            filename = get_dir_list(out_lck, "received")
            chunks = get_chunks_8bit(out_lck, "received/"+filename, 16)
            n, new_chunks = cipher.bruteforce(out_lck, chunks, mod)
            #creo i file a seconda del formato che ho creato
            if n == 0:
                print("not found valid key")
            elif n == 1:
                fout = open("received/bruteforce/Brute_Force.png", "wb+")
                for chunk in new_chunks:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())
                fout.close()

            elif n == 2:
                fout = open("received/bruteforce/Brute_Force.jpg", "wb+")
                for chunk in new_chunks:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())
                fout.close()

            elif n == 3:
                fout = open("received/bruteforce/Brute_Force.bmp", "wb+")
                for chunk in new_chunks:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())
                fout.close()

            elif n == 4:
                fout = open("received/bruteforce/Brute_Force.GIF", "wb+")
                for chunk in new_chunks:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())
                fout.close()

            elif n == 5:
                fout = open("received/bruteforce/Brute_Force.mp3", "wb+")
                for chunk in new_chunks:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())
                fout.close()