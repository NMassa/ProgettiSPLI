from helpers.utils import loop_menu, generate_keys, toBinary16, toBinary128, output
from helpers import mysocket


def keys(out_lck, my_ip, port, my_private_key, my_module, my_public_key, len_key):
    public_keys_list = []
    send_or_receive = loop_menu(out_lck, "Select one of the following actions ('e' to exit):", ["Send Key",
                                                                                                "Receive Key"])
    if send_or_receive == 1:
        # Generate keys
        bits_keys = loop_menu(out_lck, "Select one of the following length ('e' to exit): ", ["8 bits",
                                                                                               "128 bits"])
        # Inizializzo socket
        sock = mysocket.MySocket()

        if bits_keys == 1:
            if my_private_key == 0 and my_module == 0 and my_public_key == 0:
                n, d, e = generate_keys(out_lck, 16)
                my_private_key = d
                my_module = n
            elif len_key == 128:
                n, d, e = generate_keys(out_lck, 16)
                my_private_key = d
                my_module = n
            else:
                n = my_module
                e = my_public_key

            key_to_send = toBinary16(n) + '@' + toBinary16(e) + '@' + toBinary16(8)
            output(out_lck, "Sending key to %s" % my_ip)
            sock.connect(my_ip, port)
            sock.send_key(out_lck, sock, key_to_send, len(key_to_send))
            sock.close()
            # Inizializzo socket        sock.close()

            sock = mysocket.MySocket()
            output(out_lck, "Waiting for public keys..")
            pkey, mod, len_key, address = sock.recv_key(out_lck, sock, port + 1)
            public_keys_list.append([address[0], pkey, mod, len_key])
            sock.close()
            return my_private_key, public_keys_list, my_module, e, len_key

        elif bits_keys == 2:
            if my_private_key == 0 and my_module == 0 and my_public_key == 0:
                n, d, e = generate_keys(out_lck, 128)
                my_private_key = d
                my_module = n
            elif len_key == 8:
                n, d, e = generate_keys(out_lck, 128)
                my_private_key = d
                my_module = n
            else:
                n = my_module
                e = my_public_key

            key_to_send = toBinary128(n) + '@' + toBinary128(e) + '@' + toBinary128(128)

            output(out_lck, "Sending key to %s" % my_ip)
            sock.connect(my_ip, port)
            sock.send_key(out_lck, sock, key_to_send, len(key_to_send))
            sock.close()
            # Inizializzo socket
            sock = mysocket.MySocket()
            output(out_lck, "Waiting for public keys..")
            pkey, mod, len_key, address = sock.recv_key(out_lck, sock, port + 1)
            public_keys_list.append([address[0], pkey, mod, len_key])
            sock.close()
            return my_private_key, public_keys_list, my_module, e, len_key

    elif send_or_receive == 2:
        bits_keys = loop_menu(out_lck, "Select one of the following length ('e' to exit): ", ["8 bits",
                                                                                             "128 bits"])
        #Receive keys
        # Inizializzo socket
        sock = mysocket.MySocket()
        if bits_keys == 1:
            output(out_lck, "Waiting for connection... ")
            pkey, mod, rec_len_key, address = sock.recv_key(out_lck, sock, port)
            sock.close()
            public_keys_list.append([address[0], pkey, mod, rec_len_key])
            if my_private_key == 0 and my_module == 0 and my_public_key == 0:
                n, d, e = generate_keys(out_lck, 16)
                my_private_key = d
                my_module = n
            elif len_key == 128:
                n, d, e = generate_keys(out_lck, 16)
                my_private_key = d
                my_module = n
            else:
                n = my_module
                e = my_public_key

            key_to_send = toBinary16(n) + '@' + toBinary16(e) + '@' + toBinary16(8)

            # Send the key
            # Inizializzo socket
            output(out_lck, "Sending key to %s" % my_ip)
            sock = mysocket.MySocket()
            sock.connect(my_ip, port + 1)
            sock.send_key(out_lck, sock, key_to_send, len(key_to_send))
            sock.close()
            return my_private_key, public_keys_list, my_module, e, rec_len_key

        elif bits_keys == 2:
            output(out_lck, "Waiting for connection... ")
            pkey, mod, rec_len_key, address = sock.recv_key(out_lck, sock, port)
            sock.close()
            public_keys_list.append([address[0], pkey, mod, rec_len_key])
            if my_private_key == 0 and my_module == 0 and my_public_key == 0:
                n, d, e = generate_keys(out_lck, 128)
                my_private_key = d
                my_module = n
            elif len_key == 8:
                n, d, e = generate_keys(out_lck, 128)
                my_private_key = d
                my_module = n
            else:
                n = my_module
                e = my_public_key
            key_to_send = toBinary128(n) + '@' + toBinary128(e) + '@' + toBinary128(128)

            # Send the key
            # Inizializzo socket
            output(out_lck, "Sending key to %s" % my_ip)
            sock = mysocket.MySocket()
            sock.connect(my_ip, port + 1)
            sock.send_key(out_lck, sock, key_to_send, len(key_to_send))
            sock.close()
            return my_private_key, public_keys_list, my_module, e, rec_len_key

