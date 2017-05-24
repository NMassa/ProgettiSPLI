import threading

from bitarray import bitarray
from helpers import key_generator
from helpers import mysocket, cipher, utils
from helpers.utils import loop_menu, loop_input, output, loop_int_input, get_dir_list, get_chunks, get_chunks_16bit, \
    write_decrypted_from_chunks, write_encrypted_from_chunks, get_chunks_8bit, factoring, \
    write_decrypted_from_chunks_fermat

_base = "192.168.0."
host = 0


if __name__ == "__main__":

    out_lck = threading.Lock()
    network = 0
    port = 3000
    my_private_key = 0
    my_module = 0
    my_public_key = 0
    len_key = 0
    public_keys_list = []

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
        main_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["Generate Keys",
                                                                                               "View Keys",
                                                                                               "Send file",
                                                                                               "Receive file",
                                                                                               "Fermat",
                                                                                               "Bruteforce"])

        #Zotti: la tua funzione genera chiavi la trovi in utils.generate_keys. Non toccare altro, basta che torna i valori che vedi
        if main_menu == 1:
            if network == 2:
                dest = loop_input(out_lck, "Please insert the destination...")
            else:
                dest = '1'
            my_private_key, pub_key, my_module, my_public_key, len_key = key_generator.keys(out_lck, _base + dest, port,
                                                                         my_private_key, my_module, my_public_key, len_key)
            public_keys_list.append([pub_key[0][0], pub_key[0][1], pub_key[0][2], len_key])

        #Mostra le chiavi presenti nella lista
        elif main_menu == 2:

            output(out_lck, "My keys: \nPublic Key: %d\nModule: %d\nPrivate Key: %d\n" % (int(my_public_key),
                   int(my_module), int(my_private_key)))

            for index in range(0, len(public_keys_list)):
                output(out_lck, "Host: %s\nPublic Key: %d\nModule: %d\nLength: %d bits" % (str(public_keys_list[index][0]).replace("'",
                                                                            ""), public_keys_list[index][1],
                                                                            public_keys_list[index][2], public_keys_list[index][3]))

        #Send
        elif main_menu == 3:

            option_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["RSA",
                                                                                             "Authentication"])
            #Send RSA
            if option_menu == 1:
                sock = mysocket.MySocket()
                if network == 2:
                    host = loop_input(out_lck, "Insert destination IP:")

                # Get filenames
                filename = get_dir_list(out_lck, "files")

                pub_key_to_send, mod_to_send = 0, 0


                bits_keys = loop_menu(out_lck, "Select one of the following length ('e' to exit): ", ["8 bits",
                                                                                                        "128 bits"])

                output(out_lck, "Getting chunks...")
                if bits_keys == 1:
                    # Get Chunks
                    chunks = get_chunks_8bit(out_lck, 'files/' + filename, 1)  # qui va in bytes
                    c = cipher.Cipher(out_lck, chunks, 16)
                    leng = 2
                    sel = 8

                else:
                    # Get Chunks
                    chunks = get_chunks(out_lck, 'files/' + filename, 8)  # qui va in bytes
                    c = cipher.Cipher(out_lck, chunks, 128)
                    leng = 16
                    sel = 128

                output(out_lck, "Done chunks.")

                for index in range(0, len(public_keys_list)):
                    if str(public_keys_list[index][0]).replace("'", "") == _base + host and public_keys_list[index][3] == sel:
                        pub_key_to_send, mod_to_send = public_keys_list[index][1], public_keys_list[index][2]
                        output(out_lck, "Sending file to %s\nEncryption key: %d" % (public_keys_list[index][0],
                                                                                    public_keys_list[index][1]))

                output(out_lck, "Encrypting file with %d key.." % pub_key_to_send)

                encrypted_chunks = c.encrypt_and_decrypt(pub_key_to_send, mod_to_send)
                enc_file = write_encrypted_from_chunks(encrypted_chunks, "RSA", leng)

                #Il file deve essere nella cartella files
                sock.connect(_base + host, port)
                sock.sendfile(out_lck, sock, enc_file)
                output(out_lck, "File sent!\n")
                sock.close()
            #Send Authentication
            if option_menu == 2:
                sock = mysocket.MySocket()
                if network == 2:
                    host = loop_input(out_lck, "Insert destination IP:")

                # Get filenames
                filename = get_dir_list(out_lck, "files")

                bits_keys = loop_menu(out_lck, "Select one of the following length ('e' to exit): ", ["8 bits",
                                                                                                      "128 bits"])
                if bits_keys == 1:
                    # Get Chunks
                    chunks = get_chunks_8bit(out_lck, 'files/' + filename, 1)  # qui va in bytes
                    c = cipher.Cipher(out_lck, chunks, 16)
                    leng = 2

                else:
                    # Get Chunks
                    chunks = get_chunks(out_lck, 'files/' + filename, 8)  # qui va in bytes
                    c = cipher.Cipher(out_lck, chunks, 128)
                    leng = 16

                output(out_lck, "Done chunks.")
                #encrypt with private key
                output(out_lck, "Encrypting file with private %d key.." % my_private_key)
                #crypt chunk private key
                encrypted_chunks = c.encrypt_and_decrypt(my_private_key, my_module)
                enc_file = write_encrypted_from_chunks(encrypted_chunks, "AUTHENTICATION", leng)

                # Il file deve essere nella cartella files
                sock.connect(_base + host, port)
                sock.sendfile(out_lck, sock, enc_file)
                output(out_lck, "File sent!\n")
                sock.close()

        #Receive
        elif main_menu == 4:
            option_menu = loop_menu(out_lck, "Select one of the following actions ('e' to exit): ", ["RSA",
                                                                                                     "Authentication"])
            #Receive RSA
            if option_menu == 1:
                sock = mysocket.MySocket()
                sock.bind('', port)
                sock.listen(5)

                bits_keys = loop_menu(out_lck, "Select one of the following length ('e' to exit): ", ["8 bits",
                                                                                                      "128 bits"])
                enc_filename, address = sock.receivefile(out_lck, sock, "enc")
                received_mod = 0

                if bits_keys == 1:
                    # Get Chunks
                    chunks = get_chunks_16bit(out_lck, enc_filename, 2)  # qui va in bytes
                    c = cipher.Cipher(out_lck, chunks, 16)
                    lenght = 1
                    sel = 8

                elif bits_keys == 2:
                    # Get Chunks
                    chunks = get_chunks(out_lck, enc_filename, 16)  # qui va in bytes
                    c = cipher.Cipher(out_lck, chunks, 128)
                    lenght = 8
                    sel = 128

                for index in range(0, len(public_keys_list)):
                    if str(public_keys_list[index][0]).replace("'", "") == (_base + dest) and str(public_keys_list[index][3]) == str(sel):
                        pub_key_to_send, mod_to_send = public_keys_list[index][1], public_keys_list[index][2]


                #il file verrà salvato nella cartella received con l'estensione indicata
                output(out_lck, "Decrypting with private key %d" % my_private_key)
                decrypted_chunks = c.encrypt_and_decrypt(my_private_key, my_module)

                write_decrypted_from_chunks(decrypted_chunks, lenght)

                output(out_lck, "Done!\n")
                sock.close()
            #Receive Authentication
            elif option_menu == 2:
                sock = mysocket.MySocket()
                sock.bind('', port)
                sock.listen(5)
                pub_key = 0
                received_mod = 0
                bits_keys = loop_menu(out_lck, "Select one of the following length ('e' to exit): ", ["8 bits",
                                                                                                      "128 bits"])
                enc_filename, address = sock.receivefile(out_lck, sock, "enc")

                if bits_keys == 1:
                    # Get Chunks
                    chunks = get_chunks_16bit(out_lck, enc_filename, 2)  # qui va in bytes
                    c = cipher.Cipher(out_lck, chunks, 16)
                    lenght = 1
                    sel = 8

                elif bits_keys == 2:
                    # Get Chunks
                    chunks = get_chunks(out_lck, enc_filename, 16)  # qui va in bytes
                    c = cipher.Cipher(out_lck, chunks, 128)
                    lenght = 8
                    sel = 128

                for index in range(0, len(public_keys_list)):
                    if str(public_keys_list[index][0]).replace("'", "") == (_base + dest) and str(public_keys_list[index][3]) == str(sel):
                        pub_key_to_send, mod_to_send = public_keys_list[index][1], public_keys_list[index][2]


                # il file verrà salvato nella cartella received con l'estensione indicata
                output(out_lck, "Decrypting with pubic key %d" % my_public_key)
                decrypted_chunks = c.encrypt_and_decrypt(pub_key_to_send, mod_to_send)

                write_decrypted_from_chunks(decrypted_chunks, lenght)
                output(out_lck, "Decrypted file coming from %s." % str(address).replace("'", ""))
                output(out_lck, "Done!\n")
                sock.close()

        elif main_menu == 5:
            output(out_lck, "Fermat Factorization Attack")

            d = factoring(out_lck, my_module, my_public_key)

            output(out_lck, "Reading encrypted file ...")
            chunks = get_chunks_16bit(out_lck, "received/enc", 2)  # qui va in bytes
            c = cipher.Cipher(out_lck, chunks, 16)
            output(out_lck, "Decrypting with private key %s" % d)
            decrypted_chunks = c.encrypt_and_decrypt(d, my_module)
            write_decrypted_from_chunks_fermat(decrypted_chunks, 2)
            output(out_lck, "Decrypted!\n")

        elif main_menu == 6:
            output(out_lck, "\n Start Bruteforce\n")
            #output(out_lck, "\nInsert public mod : ")
            #mod = input()
            filename = get_dir_list(out_lck, "received")
            chunks = get_chunks_16bit(out_lck, "received/" + filename, 2)
            n, new_chunks = cipher.bruteforce(out_lck, chunks, my_module, my_private_key)
            #creo i file a seconda del formato che ho creato
            if n == 0:
                output(out_lck, "not found valid key")
            elif n == 1:
                fout = open("received/Brute_Force.png", "wb+")
                for chunk in new_chunks:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())
                fout.close()

            elif n == 2:
                fout = open("received/Brute_Force.jpg", "wb+")
                for chunk in new_chunks:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())
                fout.close()

            elif n == 3:
                fout = open("received/Brute_Force.bmp", "wb+")
                for chunk in new_chunks:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())
                fout.close()

            elif n == 4:
                fout = open("received/Brute_Force.GIF", "wb+")
                for chunk in new_chunks:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())
                fout.close()

            elif n == 5:
                fout = open("received/Brute_Force.mp3", "wb+")
                for chunk in new_chunks:
                    ba = bitarray(chunk)
                    fout.write(ba.tobytes())
                fout.close()