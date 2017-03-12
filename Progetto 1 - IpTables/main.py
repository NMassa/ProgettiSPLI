import threading
import sys
#from pathl1ib import Path # if you haven't already done so          #Daniele: pathlib mi crea un errore. Senza funziona tutto lo stesso (o almeno sembra)
#root = str(Path(__file__).resolve().parents[1])
# Or
# from os.path import dirname, abspath
# root = dirname(dirname(abspath(__file__)))
# sys.path.append(root)

from helpers.helpers import output
from helpers.connection import Connection
from helpers import config

if __name__ == "__main__":

    out_lck = threading.Lock()

    # Main Menu
    while True:
        output(out_lck, "\nSelect one of the following options ('e' to exit): ")
        output(out_lck, "1: Send messages ")
        output(out_lck, "2: Receive messages ")
        output(out_lck, "3: Apply iptables rules ")
        output(out_lck, "4: Reset iptables rules ")

        int_option = None
        try:
            option = input()
        except SyntaxError:
            option = None

        if option is None:
            output(out_lck, "Please select an option")
        elif option == 'e':
            output(out_lck, "Bye bye")
            sys.exit()
        else:
            try:
                int_option = int(option)
            except ValueError:
                output(out_lck, "A number is required")
            else:
                if int_option == 1:
                    protocol = None
                    while protocol is None:
                        output(out_lck, "\nSelect protocol ('e' to exit): ")
                        output(out_lck, "1: TCP ")
                        output(out_lck, "2: UDP ")

                        int_option = None
                        try:
                            option = input()
                        except SyntaxError:
                            option = None

                        if option is None:
                            output(out_lck, "Please select an option")
                        elif option == 'e':
                            continue
                        else:
                            try:
                                int_option = int(option)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                if int_option == 1:
                                    protocol = "TCP"
                                elif int_option == 2:
                                    protocol = "UDP"
                                else:
                                    output(out_lck, "Option " + str(int_option) + " not available")
                                    continue

                    output(out_lck, "Selected protocol: %s" % protocol)

                    host = None
                    output(out_lck, "Insert destination host number:")

                    while host is None:
                        try:
                            option = input()
                        except SyntaxError:
                            option = None

                        if option is None:
                            output(out_lck, "Please insert destination host number")
                        else:
                            try:
                                int_option = int(option)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                host = int_option
                                output(out_lck, "Selected host: %s%i" % (config._base,host))

                    port = None
                    output(out_lck, "Insert destination port number:")

                    while port is None:
                        try:
                            option = input()
                        except SyntaxError:
                            option = None

                        if option is None:
                            output(out_lck, "Please insert destination port number")
                        else:
                            try:
                                int_option = int(option)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                port = int_option
                                output(out_lck, "Selected port: %i" % port)

                        # TODO: creare thread
                        c = Connection(host, protocol, port, out_lck)
                        try:
                            c.connect()
                            #threading._start_new_thread(c.connect,())
                            output(out_lck, "Sending %s requests.." % protocol)
                        except Exception as e:           #Daniele: non so che Exception da il multithreading
                            output(out_lck, str(e))


                elif int_option == 2:
                    protocol = None
                    while protocol is None:
                        output(out_lck, "\nSelect protocol ('e' to exit): ")
                        output(out_lck, "1: TCP ")
                        output(out_lck, "2: UDP ")

                        int_option = None
                        try:
                            option = input()
                        except SyntaxError:
                            option = None

                        if option is None:
                            output(out_lck, "Please select an option")
                        elif option == 'e':
                            continue
                        else:
                            try:
                                int_option = int(option)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                if int_option == 1:
                                    protocol = "TCP"
                                elif int_option == 2:
                                    protocol = "UDP"
                                else:
                                    output(out_lck, "Option " + str(int_option) + " not available")
                                    continue

                    output(out_lck, "Selected protocol: %s" % protocol)

                    port = None
                    output(out_lck, "Insert destination port number:")

                    while port is None:
                        try:
                            option = input()
                        except SyntaxError:
                            option = None

                        if option is None:
                            output(out_lck, "Please insert destination port number")
                        else:
                            try:
                                int_option = int(option)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                port = int_option

                    output(out_lck, "Selected port: %i" % port)

                    # TODO: creare thread

                    c = Connection(None, protocol, port, out_lck)
                    try:
                        #threading._start_new_thread(c.listen, ())
                        c.listen()
                        output(out_lck, "Listening on port %s.." % port)
                    except Exception:                               # Daniele: non so che Exception da il multithreading
                        output(out_lck, "Thread not initialized")



                elif int_option == 3:
                    print("menu regole")
                elif int_option == 4:
                    print("reset regole")
                else:
                    output(out_lck, "Option " + str(int_option) + " not available")





