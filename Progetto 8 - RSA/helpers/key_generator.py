from helpers.utils import loop_menu, generate_keys, toBinary16, toBinary128, output
from helpers import mysocket, utils


def keys(out_lck, _base, host, port, my_private_key, my_module, my_public_key):
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
            else:
                n = my_module
                e = my_public_key

            key_to_send = toBinary16(n) + '@' + toBinary16(e)
            output(out_lck, "Sending key to %s" % str(_base + host))
            sock.connect(_base + host, port)
            sock.send_key(out_lck, sock, key_to_send, len(key_to_send))
            sock.close()
            # Inizializzo socket
            sock = mysocket.MySocket()
            output(out_lck, "Waiting for public keys..")
            pkey, mod, address = sock.recv_key(out_lck, sock, port + 1)
            public_keys_list.append([address[0], pkey, mod])

        elif bits_keys == 2:
            if my_private_key == 0 and my_module == 0 and my_public_key == 0:
                n, d, e = generate_keys(out_lck, 128)
                my_private_key = d
                my_module = n
            else:
                n = my_module
                e = my_public_key

            key_to_send = toBinary128(n) + '@' + toBinary128(e)

            output(out_lck, "Sending key to %s" % str(_base + host))
            sock.connect(_base + host, port)
            sock.send_key(out_lck, sock, key_to_send, len(key_to_send))
            sock.close()
            # Inizializzo socket
            sock = mysocket.MySocket()
            output(out_lck, "Waiting for public keys..")
            pkey, mod, address = sock.recv_key(out_lck, sock, port + 1)
            public_keys_list.append([address[0], pkey, mod])

        sock.close()

    elif send_or_receive == 2:
        bits_keys = loop_menu(out_lck, "Select one of the following length ('e' to exit): ", ["8 bits",
                                                                                             "128 bits"])
        #Receive keys
        # Inizializzo socket
        sock = mysocket.MySocket()
        if bits_keys == 1:
            output(out_lck, "Waiting for connection... ")
            pkey, mod, address = sock.recv_key(out_lck, sock, port)
            sock.close()
            public_keys_list.append([address[0], pkey, mod])
            if my_private_key == 0 and my_module == 0 and my_public_key == 0:
                n, d, e = generate_keys(out_lck, 16)
                my_private_key = d
                my_module = n
            else:
                n = my_module
                e = my_public_key

            key_to_send = toBinary16(n) + '@' + toBinary16(e)

            # Send the key
            # Inizializzo socket
            output(out_lck, "Sending key to %s" % str(_base + host))
            sock = mysocket.MySocket()
            sock.connect(_base + host, port + 1)
            sock.send_key(out_lck, sock, key_to_send, len(key_to_send))

        elif bits_keys == 2:
            output(out_lck, "Waiting for connection... ")
            pkey, mod, address = sock.recv_key(out_lck, sock, port)
            sock.close()
            public_keys_list.append([address[0], pkey, mod])
            if my_private_key == 0 and my_module == 0 and my_public_key == 0:
                n, d, e = generate_keys(out_lck, 128)
                my_private_key = d
                my_module = n
            else:
                n = my_module
                e = my_public_key
            key_to_send = toBinary128(n) + '@' + toBinary128(e)

            # Send the key
            # Inizializzo socket
            output(out_lck, "Sending key to %s" % str(_base + host))
            sock = mysocket.MySocket()
            sock.connect(_base + host, port + 1)
            sock.send_key(out_lck, sock, key_to_send, len(key_to_send))
        sock.close()
    return my_private_key, public_keys_list, my_module, e