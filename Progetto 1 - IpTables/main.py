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
#import iptc     #Daniele: potrebbe servire in un secondo momento...
from helpers import rules

if __name__ == "__main__":

    out_lck = threading.Lock()

    # Main Menu
    while True:
        output(out_lck, "\nSelect one of the following options ('e' to exit): ")
        output(out_lck, "1: Send messages ")
        output(out_lck, "2: Receive messages ")
        output(out_lck, "3: Apply iptables rules ")
        output(out_lck, "4: Reset iptables rules ")
        output(out_lck, "5: Show iptables ")

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
                    rule = None
                    while rule is None:
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
                                    rule = "TCP"
                                elif int_option == 2:
                                    rule = "UDP"
                                else:
                                    output(out_lck, "Option " + str(int_option) + " not available")
                                    continue

                    output(out_lck, "Selected protocol: %s" % rule)

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
                        c = Connection(host, rule, port, out_lck)
                        try:
                            c.connect()
                            #threading._start_new_thread(c.connect,())
                            output(out_lck, "Sending %s requests.." % rule)
                        except Exception as e:           #Daniele: non so che Exception da il multithreading
                            output(out_lck, str(e))


                elif int_option == 2:
                    rule = None
                    while rule is None:
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
                                    rule = "TCP"
                                elif int_option == 2:
                                    rule = "UDP"
                                else:
                                    output(out_lck, "Option " + str(int_option) + " not available")
                                    continue

                    output(out_lck, "Selected protocol: %s" % rule)

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

                    c = Connection(None, rule, port, out_lck)
                    try:
                        #threading._start_new_thread(c.listen, ())
                        c.listen()
                        output(out_lck, "Listening on port %s.." % port)
                    except Exception:                               # Daniele: non so che Exception da il multithreading
                        output(out_lck, "Thread not initialized")

                elif int_option == 3:
                    action = None
                    while action is None:
                        output(out_lck, "Select an option ('e' to exit): \n" \
                                        "1: Blocca sorgente IP \n" \
                                        "2: Blocca Protocollo \n" \
                                        "3: Blocca Porta \n" \
                                        "4: Blocca Traffico in uscita \n" \
                                        "5: Limita Ping \n" \
                                        "6: SYN \n" \
                                        "7: Port Forwarding \n" \
                                        "8: Ridirezione ad altro destinatario \n")

                        selected = None
                        try:
                            action = input()
                        except SyntaxError:
                            action = None

                        if action is None:
                            output(out_lck, "Please select an option")
                        elif action == 'e':
                            continue
                        else:
                            try:
                                selected = int(action)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                #Blocco IP
                                if selected == 1:
                                    output(out_lck, "Please insert the number of the host")
                                    selected = input()
                                    try:
                                        selected = int(option)
                                    except ValueError:
                                        output(out_lck, "A number is required")
                                    else:
                                        rules.block_IPsorg(out_lck, "%s%i" % (config._base, selected))
                                        output(out_lck, "Rule Applied!\n")
                                #Blocco Protocollo
                                elif selected == 2:
                                    output(out_lck, "Please select the Protocol")
                                    output(out_lck, "\n1: TCP\n2: UDP\n3: ICMP")
                                    proto = input()
                                    try:
                                        protocol = int(proto)
                                    except ValueError:
                                        output(out_lck, "A number is required")
                                    else:
                                        if protocol == 1:
                                            rules.block_proto(out_lck, "tcp")
                                            output(out_lck, "Rule Applied!\n")
                                        elif protocol == 2:
                                            rules.block_proto(out_lck, "udp")
                                            output(out_lck, "Rule Applied!\n")
                                        elif protocol == 3:
                                            rules.block_proto(out_lck, "icmp")
                                            output(out_lck, "Rule Applied!\n")
                                        else:
                                            output(out_lck, "Please insert a number")
                                #Blocco Porta
                                elif selected == 3:
                                    output(out_lck, "Please insert port number")
                                    porta = input()
                                    protocol = None
                                    interface = None
                                    try:
                                        port = int(porta)
                                    except ValueError:
                                        output(out_lck, "A number is required")
                                    else:
                                        output(out_lck, "Please insert Network Interface")

                                        interface = input()             #manca gestione errore

                                        output(out_lck, "Please select the Protocol")
                                        output(out_lck, "\n1: TCP\n2: UDP\n3: ICMP")
                                        proto = input()
                                        try:
                                            protocol = int(proto)
                                        except ValueError:
                                            output(out_lck, "A number is required")
                                        else:
                                            if protocol == 1:
                                                rules.block_port(out_lck, interface, "tcp", porta)
                                                output(out_lck, "Rule Applied!\n")
                                            elif protocol == 2:
                                                rules.block_port(out_lck, interface, "udp", porta)
                                                output(out_lck, "Rule Applied!\n")
                                            elif protocol == 3:
                                                rules.block_port(out_lck, interface, "icmp", porta)
                                                output(out_lck, "Rule Applied!\n")
                                            else:
                                                output(out_lck, "Please insert a number")
                                #Blocco traffico in uscita
                                elif selected == 4:
                                    output(out_lck, "Please insert Network Interface")

                                    interface = input()  # manca gestione errore

                                    output(out_lck, "Please insert the number of the host")
                                    selected = input()
                                    try:
                                        host = int(selected)
                                    except ValueError:
                                        output(out_lck, "A number is required")
                                    else:
                                        rules.block_out_sel(out_lck, interface, "%s%i" % (config._base, host))
                                        output(out_lck, "Rule Applied!\n")
                                #Limita ping
                                elif selected == 5:
                                    rules.lim_risp_ping(out_lck)
                                    output(out_lck, "Rule Applied!\n")
                                #SYN
                                elif selected == 6:
                                    output(out_lck, "Please insert port number")
                                    porta = input()
                                    try:
                                        port = str(porta)
                                    except ValueError:
                                        output(out_lck, "A number is required")
                                    else:
                                        output(out_lck, "Please max number of connections")
                                        connections = input()
                                        try:
                                            conn = str(connections)
                                        except ValueError:
                                            output(out_lck, "A number is required")
                                        else:
                                            output(out_lck, "Please select a protocol")
                                            output(out_lck, "\n1: TCP\n2: UDP\n3: ICMP")
                                            proto = input()
                                            try:
                                                protocol = int(proto)
                                            except ValueError:
                                                output(out_lck, "A number is required")
                                            else:
                                                if protocol == 1:
                                                    rules.rest_conn_Ip(out_lck, "tcp", port, conn)
                                                    output(out_lck, "Rule Applied!\n")
                                                elif protocol == 2:
                                                    rules.rest_conn_Ip(out_lck, "udp", port, conn)
                                                    output(out_lck, "Rule Applied!\n")
                                                elif protocol == 3:
                                                    rules.rest_conn_Ip(out_lck, "icmp", port, conn)
                                                    output(out_lck, "Rule Applied!\n")
                                                else:
                                                    output(out_lck, "Please insert a number")
                                #Port Forwarding
                                elif selected == 7:
                                    output(out_lck, "Please insert Network Interface")

                                    interface = input()  # manca gestione errore

                                    output(out_lck, "Please insert the number of the source  !!!!DA CONTROLLARE!!!!")    #Da controllare
                                    temphost = input()
                                    try:
                                        ip1 = str(temphost)
                                    except ValueError:
                                        output(out_lck, "A number is required")
                                    else:
                                        output(out_lck,
                                               "Please insert the number of the receiver  !!!!DA CONTROLLARE!!!!")  # Da controllare
                                        temphost = input()
                                        try:
                                            ip2 = str(temphost)
                                        except ValueError:
                                            output(out_lck, "A number is required")
                                        else:
                                            output(out_lck, "Please insert port number")
                                            porta = input()
                                            try:
                                                port = str(porta)
                                            except ValueError:
                                                output(out_lck, "A number is required")
                                            else:
                                                output(out_lck, "Please select the Protocol")
                                                output(out_lck, "\n1: TCP\n2: UDP\n3: ICMP")
                                                proto = input()
                                                try:
                                                    protocol = int(proto)
                                                except ValueError:
                                                    output(out_lck, "A number is required")
                                                else:
                                                    if protocol == 1:
                                                        rules.port_forw(out_lck, interface, "tcp", "%s%s" % (config._base, ip1), "%s%s" % (config._base, ip2), port)
                                                        output(out_lck, "Rule Applied!\n")
                                                    elif protocol == 2:
                                                        rules.port_forw(out_lck, interface, "udp",
                                                                        "%s%s" % (config._base, ip1),
                                                                        "%s%s" % (config._base, ip2), port)
                                                        output(out_lck, "Rule Applied!\n")
                                                    elif protocol == 3:
                                                        rules.port_forw(out_lck, interface, "icmp",
                                                                        "%s%s" % (config._base, ip1),
                                                                        "%s%s" % (config._base, ip2), port)
                                                        output(out_lck, "Rule Applied!\n")
                                                    else:
                                                        output(out_lck, "Please insert a number")
                                #Redirezione
                                elif selected == 8:
                                    output(out_lck, "Please insert the number of local IP")  # Da controllare
                                    temphost = input()
                                    try:
                                        ip1 = str(temphost)
                                    except ValueError:
                                        output(out_lck, "A number is required")
                                    else:
                                        output(out_lck,
                                               "Please insert the number of the receiver")  # Da controllare
                                        temphost = input()
                                        try:
                                            ip2 = str(temphost)
                                        except ValueError:
                                            output(out_lck, "A number is required")
                                        else:
                                            output(out_lck, "Please insert port number")
                                            porta = input()
                                            try:
                                                port = str(porta)
                                            except ValueError:
                                                output(out_lck, "A number is required")
                                            else:
                                                output(out_lck, "Please select a protocol")
                                                output(out_lck, "\n1: TCP\n2: UDP\n3: ICMP")
                                                proto = input()
                                                try:
                                                    protocol = int(proto)
                                                except ValueError:
                                                    output(out_lck, "A number is required")
                                                else:
                                                    if protocol == 1:
                                                        rules.redirection(out_lck, "%s%s" %(config._base, ip2), "%s%s" %(config._base, ip1), "tcp", port)
                                                        output(out_lck, "Rule Applied!\n")
                                                    elif protocol == 2:
                                                        rules.redirection(out_lck, "%s%s" % (config._base, ip2),
                                                                          "%s%s" % (config._base, ip1), "udp", port)
                                                        output(out_lck, "Rule Applied!\n")
                                                    elif protocol == 3:
                                                        rules.redirection(out_lck, "%s%s" % (config._base, ip2),
                                                                          "%s%s" % (config._base, ip1), "icmp", port)
                                                        output(out_lck, "Rule Applied!\n")
                                                    else:
                                                        output(out_lck, "Please insert a number")

                elif int_option == 4:
                    rules.flush_tables(out_lck)
                    output(out_lck, "Rule Applied!\n")

                elif int_option == 5:
                    rules.show_tables(out_lck)
                    output(out_lck, "Rule Applied!\n")
                else:
                    output(out_lck, "Option " + str(int_option) + " not available")





