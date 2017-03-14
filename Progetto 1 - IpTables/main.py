import threading
import sys
from helpers.helpers import output
from helpers.connection import Connection
from helpers import config
from helpers.helpers import loop_menu
#import iptc     #Daniele: potrebbe servire in un secondo momento...
from helpers import rules

if __name__ == "__main__":

    out_lck = threading.Lock()
    while True:
        # Main Menu
        main_menu = loop_menu(out_lck, "action", [  "Send messages ",
                                                    "Receive messages ",
                                                    "Apply iptables rules ",
                                                    "Reset iptables rules ",
                                                    "Show iptables ",
                                                    "Server-Client "])
        if main_menu is not None:
            if main_menu == 1:
                protocol = loop_menu(out_lck, "protocol", ["TCP", "UDP"])
                if protocol is not None:
                    if protocol == 1:
                        protocol = "TCP"
                    elif protocol == 2:
                        protocol = "UDP"

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
                                host = config._base + option
                                output(out_lck, "Selected host: %s" % host)

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

                        c = Connection(host, protocol, port, out_lck)
                        try:
                            c.connect()
                            output(out_lck, "Sending %s requests.." % protocol)
                        except Exception as e:
                            output(out_lck, str(e))

            elif main_menu == 2:
                protocol = loop_menu(out_lck, "protocol", ["TCP", "UDP"])
                if protocol is not None:
                    if protocol == 1:
                        protocol = "TCP"
                    elif protocol == 2:
                        protocol = "UDP"

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

                    c = Connection(None, protocol, port, out_lck)
                    try:
                        c.listen()
                        output(out_lck, "Listening on port %s.." % port)
                    except Exception:                               # Daniele: non so che Exception da il multithreading
                        output(out_lck, "Thread not initialized")

            elif main_menu == 3:
                action = loop_menu(out_lck, "action", [ "Blocca sorgente IP",
                                                        "Blocca Protocollo",
                                                        "Blocca Porta",
                                                        "Blocca Traffico in uscita",
                                                        "Limita Ping",
                                                        "SYN",
                                                        "Port Forwarding",
                                                        "Ridirezione ad altro destinatario",
                                                        "Variazione TTL pacchetto"])

                if action is not None:
                    #Blocco IP
                    if action == 1:
                        output(out_lck, "Please insert the number of the host")
                        option = input()
                        host = config._base + selected
                        rules.block_IPsorg(out_lck, "%s" % host)

                    #Blocco Porta
                    elif action == 2:
                        output(out_lck, "Please select the rotocol")
                        output(out_lck, "\n1: TCP\n2: UDP\n3: ICMP")
                        proto = input()
                        try:
                            protocol = int(proto)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            if protocol == 1:
                                rules.block_proto(out_lck, "tcp")

                            elif protocol == 2:
                                rules.block_proto(out_lck, "udp")

                            elif protocol == 3:
                                rules.block_proto(out_lck, "icmp")

                            else:
                                output(out_lck, "Please insert a number")
                    #Blocco Protocollo
                    elif action == 3:
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

                            proto = loop_menu(out_lck, "protocol", ["TCP", "UDP", "ICMP"])
                            if proto is not None:
                                if proto == 1:
                                    rules.block_port(out_lck, interface, "tcp", porta)

                                elif proto == 2:
                                    rules.block_port(out_lck, interface, "udp", porta)

                                elif proto == 3:
                                    rules.block_port(out_lck, interface, "icmp", porta)


                    #Blocco traffico in uscita
                    elif action == 4:
                        output(out_lck, "Please insert Network Interface")

                        interface = input()  # manca gestione errore

                        output(out_lck, "Please insert the number of the host")
                        selected = input()
                        host2 = config._base + selected
                        rules.block_out_sel(out_lck, interface, "%s" % host2)

                    #Limita ping
                    elif action == 5:
                        rules.lim_risp_ping(out_lck)

                    #SYN
                    elif action == 6:
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

                                    elif protocol == 2:
                                        rules.rest_conn_Ip(out_lck, "udp", port, conn)

                                    elif protocol == 3:
                                        rules.rest_conn_Ip(out_lck, "icmp", port, conn)

                                    else:
                                        output(out_lck, "Please insert a number")
                    #Port Forwarding
                    elif action == 7:
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

                                        elif protocol == 2:
                                            rules.port_forw(out_lck, interface, "udp",
                                                            "%s%s" % (config._base, ip1),
                                                            "%s%s" % (config._base, ip2), port)

                                        elif protocol == 3:
                                            rules.port_forw(out_lck, interface, "icmp",
                                                            "%s%s" % (config._base, ip1),
                                                            "%s%s" % (config._base, ip2), port)

                                        else:
                                            output(out_lck, "Please insert a number")
                    #Redirezione
                    elif action == 8:
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

                                        elif protocol == 2:
                                            rules.redirection(out_lck, "%s%s" % (config._base, ip2),
                                                              "%s%s" % (config._base, ip1), "udp", port)

                                        elif protocol == 3:
                                            rules.redirection(out_lck, "%s%s" % (config._base, ip2),
                                                              "%s%s" % (config._base, ip1), "icmp", port)

                                        else:
                                            output(out_lck, "Please insert a number")

                elif action == 9:
                    output(out_lck, "Please insert the number of TTL")  # Da controllare
                    ttl = input()
                    try:
                        str_ttl = str(ttl)
                    except ValueError:
                        output(out_lck, "A number is required")
                    else:
                        rules.set_TTL(out_lck, str_ttl)

            elif main_menu == 4:
                rules.flush_tables(out_lck)
                output(out_lck, "Rule Applied!\n")
            elif main_menu == 4:
                rules.flush_tables(out_lck)

            elif main_menu == 5:
                rules.show_tables(out_lck)
                main_menu = None

            elif main_menu == 6:
                c = Connection(None, 3000, None, out_lck)
                c.client_server(out_lck)
                output(out_lck, "Routing finish!\n")

            elif main_menu == 6:
                output(out_lck, "Please insert destination IP")
                destinazione = input()
                try:
                    dest = str(destinazione)
                except ValueError:
                    output(out_lck, "A number is required")

                output(out_lck, "Please insert port")
                porta = input()
                try:
                     port = str(porta)
                except ValueError:
                    output(out_lck, "A number is required")

                c = Connection(dest, None, port, out_lck)
                c.client_server()
                output(out_lck, "Routing finish!\n")


