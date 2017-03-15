import socket
import sys
import select

if __name__ == "__main__":
    protocol = sys.argv[1]
    port = sys.argv[2]

    if str(protocol) == "tcp":
        sock_lst = []
        try:
            sock_lst.append(socket.socket(socket.AF_INET6, socket.SOCK_STREAM))
            sock_lst[-1].setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            sock_lst[-1].bind(("", int(port)))
            sock_lst[-1].listen(100)
            print("Listening on port " + port)
        except socket.error as message:
            if sock_lst[-1]:
                sock_lst[-1].close()
                sock_lst = sock_lst[:-1]
            sys.exit(1)

        while True:
            inputready, outputready, exceptready = select.select(sock_lst, [], [])

            for s in inputready:
                for item in sock_lst:
                    if s == item:
                        port = s.getsockname()[1]

                        try:
                            conn, addr = item.accept()
                            size = 1024
                            data = conn.recv(size)
                            while len(data) > 0:
                                print("Received: %s" % data)
                                data = conn.recv(size)

                        except Exception as e:
                            print("Server Error: " + e.message)


        # # Ascolto socket TCP
        # _socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        # _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        # try:
        #     _socket.bind(('', int(port)))  # inizializzazione della connessione
        #     _socket.listen(100)
        #     print("Listening on port %s" % (port))
        #     conn, addr = _socket.accept()
        #     size = 1024
        #     data = conn.recv(size)
        #     while len(data) > 0:
        #         print("Received: %s" % data)
        #         data = conn.recv(size)
        # except socket.error as msg:
        #     print(str(msg))

    # Ascolto socket UDP
    elif str(protocol) == "udp":

        _socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        _socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        try:
            _socket.bind(("", int(port)))  # inizializzazione della connessione
            print("Listening on port %s" % (port))
            while True:
                data, address = _socket.recvfrom(1024)
                print("Received: %s" % data)

        except socket.error as msg:
            print(str(msg))
    else:
        # errori
        exit()