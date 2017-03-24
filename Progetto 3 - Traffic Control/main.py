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
    output(out_lck, "Insert your IP: ")
    ip = None
    while ip is None:
        try:
            ip = input()
        except SyntaxError:
            ip = None
        if ip is None:
            output(out_lck, "Please insert your IP number")
        else:
            my_ip = config._base + ip

    output(out_lck, "Source IP: " + my_ip)
    while True:
        # Main Menu
        #output(out_lck, "Insert your IP: ")


        main_menu = loop_menu(out_lck, "action", [  "Send messages ",
                                                    "Receive messages ",
                                                    "Apply tc rules ",
                                                    "Reset tc rules ",
                                                    "Show tc rules",
                                                    "Show logs "])
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

                    c = Connection(host, protocol, port, my_ip, out_lck)
                    try:
                        c.connect()
                        output(out_lck, "Sending %s requests.." % protocol)
                    except Exception as e:
                         output(out_lck, str(e))

                    # per sicurezza teniamo

                    # n = None
                    # output(out_lck, "Insert packet number:")
                    #
                    # while n is None:
                    #     try:
                    #         option = input()
                    #     except SyntaxError:
                    #         option = None
                    #
                    #     if option is None:
                    #         output(out_lck, "Please insert packet number")
                    #     else:
                    #         try:
                    #             int_option = int(option)
                    #         except ValueError:
                    #             output(out_lck, "A number is required")
                    #         else:
                    #             n = int_option
                    #
                    # output(out_lck, "Insert message: ")
                    # msg = input()
                    #
                    # Connection.send_udp(n, msg, host, port)
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

                    c = Connection(None, protocol, port, my_ip, out_lck)
                    try:
                        c.listen()
                        output(out_lck, "Listening on port %s.." % port)
                    except Exception:                               # Daniele: non so che Exception da il multithreading
                        output(out_lck, "Thread not initialized")
            elif main_menu == 3:
                action = loop_menu(out_lck, "action", [ "Delay",
                                                        "Delay Random",
                                                        "Lost Packets",
                                                        "Port Forwarding",
                                                        "Block inbound or outbound traffic",
                                                        "Redirection (destination)",
                                                        "Packet alteration (ttl)",
                                                        "Ping limit",
                                                        "SYN defense"])

                if action is not None:
                    # Delay
                    if action == 1:
                        output(out_lck, "Please insert time of delay:")
                        n_delay = input()
                        try:
                            num = str(n_delay)
                        except ValueError:
                            output(out_lck, "A number is required")
                        output(out_lck, "Please select Wlan or Eth")
                        output(out_lck, "\n1: Wlan\n2: Eth")
                        dev = input()
                        try:
                            device = int(dev)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            if device == 1:
                                rules.delay(out_lck, "wlan0",num)
                            elif device == 2:
                                rules.delay(out_lck, "eth0",num)
                            else:
                                output(out_lck, "Option not available")
                    #Delay Random
                    if action == 2:
                        output(out_lck, "Please insert the range1 time of delay:")
                        n_delay = input()
                        output(out_lck, "Please insert the range2 time of delay:")
                        n_delay2 = input()
                        try:
                            num = str(n_delay)
                            num2 = str(n_delay2)
                        except ValueError:
                            output(out_lck, "A number is required")
                        output(out_lck, "Please select Wlan or Eth")
                        output(out_lck, "\n1: Wlan\n2: Eth")
                        dev = input()
                        try:
                            device = int(dev)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            if device == 1:
                                rules.delay(out_lck, "wlan0",num,num2)
                            elif device == 2:
                                rules.delay(out_lck, "eth0",num,num2)
                            else:
                                output(out_lck, "Option not available")
                    # Lost Packets
                    elif action == 3:
                        output(out_lck, "Please insert the number %: ")
                        option = input()
                        try:
                            n=str(option)
                        except ValueError:
                            output(out_lck, "A number is required")
                            output(out_lck, "Please select Wlan or Eth")
                            output(out_lck, "\n1: Wlan\n2: Eth")
                            dev = input()
                            try:
                                device = int(dev)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                if device == 1:
                                     rules.delay(out_lck, "wlan0", n)
                                elif device == 2:
                                     rules.delay(out_lck, "eth0", n)
                                else:
                                     output(out_lck, "Option not available")
                    # Lost Packets
                    elif action == 4:
                         output(out_lck, "Please insert the number %: ")
                         option = input()
                         try:
                             n = str(option)
                         except ValueError:
                             output(out_lck, "A number is required")
                             output(out_lck, "Please select Wlan or Eth")
                             output(out_lck, "\n1: Wlan\n2: Eth")
                             dev = input()
                             try:
                                device = int(dev)
                             except ValueError:
                                output(out_lck, "A number is required")
                             else:
                                if device == 1:
                                     rules.delay(out_lck, "wlan0", n)
                                elif device == 2:
                                     rules.delay(out_lck, "eth0", n)
                                else:
                                     output(out_lck, "Option not available")
                    # Port Forwarding
                    elif action == 5:
                        output(out_lck, "Please insert the destination host")  # Da controllare
                        temphost = input()
                        try:
                            ip1 = str(temphost)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            output(out_lck, "Please insert destination port number")
                            dport = input()
                            try:
                                dport = int(dport)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                output(out_lck, "Please insert destination port number")
                                dport2 = input()
                                try:
                                    dport2 = int(dport2)
                                except ValueError:
                                    output(out_lck, "A number is required")
                                else:
                                    output(out_lck, "Please select the Protocol")
                                    output(out_lck, "1: TCP\n2: UDP\n3: ICMP")
                                    proto = input()
                                    try:
                                        protocol = int(proto)
                                    except ValueError:
                                        output(out_lck, "A number is required")
                                    else:
                                        if protocol == 1:
                                            rules.port_forw(out_lck, "tcp", ip1, dport, dport2)

                                        elif protocol == 2:
                                            rules.port(out_lck, "udp", ip1, dport, dport2)

                                        elif protocol == 3:
                                            rules.port_forw(out_lck, "icmp", ip1, dport, dport2)
                                        else:
                                            output(out_lck, "Option not available")
                    # Block inbound or outbound traffic
                    elif action == 6:
                        output(out_lck, "Insert destination port:")
                        p = input()
                        try:
                            port = str(p)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            output(out_lck, "Please select a protocol:")
                            output(out_lck, "1: TCP\n2: UDP\n3: ICMP")
                            proto = input()
                            try:
                                protocol = int(proto)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                output(out_lck, "Block input or output?: ")
                                output(out_lck, "1: Input")
                                output(out_lck, "2: Output")

                                option = input()
                                try:
                                    int_option = int(option)
                                except ValueError:
                                    output(out_lck, "A number is required")
                                else:
                                    if int_option == 1:
                                        output(out_lck, "Insert destination:")
                                        dip = input()

                                        if protocol == 1:
                                            rules.block_input(out_lck, dip, port, "tcp")
                                        elif protocol == 2:
                                            rules.block_input(out_lck, dip, port, "udp")
                                        elif protocol == 3:
                                            rules.block_input(out_lck, dip, port, "icmp")
                                        else:
                                            output(out_lck, "Option not available")
                                    elif int_option == 2:

                                        output(out_lck, "Insert destination:")
                                        dip = input()

                                        if protocol == 1:
                                            rules.block_output(out_lck, dip, port, "tcp")
                                        elif protocol == 2:
                                            rules.block_output(out_lck, dip, port, "udp")
                                        elif protocol == 3:
                                            rules.block_output(out_lck, dip, port, "icmp")
                                        else:
                                            output(out_lck, "Option not available")
                                    else:
                                        output(out_lck, "Option not available")
                    # Redirect
                    elif action == 7:
                        output(out_lck, "Please insert the number of local IP")
                        ip1 = input()

                        output(out_lck, "Please insert the number of the receiver")
                        ip2 = input()

                        output(out_lck, "Please insert port number")
                        porta = input()
                        try:
                            port = str(porta)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            output(out_lck, "Please select a protocol")
                            output(out_lck, "1: TCP\n2: UDP\n3: ICMP")
                            proto = input()
                            try:
                                protocol = int(proto)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                if protocol == 1:
                                    rules.redirection(out_lck, "%s%s" % (config._base, ip2),
                                                      "%s%s" % (config._base, ip1), "tcp", port)

                                elif protocol == 2:
                                    rules.redirection(out_lck, "%s%s" % (config._base, ip2),
                                                      "%s%s" % (config._base, ip1), "udp", port)

                                elif protocol == 3:
                                    rules.redirection(out_lck, "%s%s" % (config._base, ip2),
                                                      "%s%s" % (config._base, ip1), "icmp", port)

                                else:
                                    output(out_lck, "Option not available")
                    # Alterazione pacchetto (mangle)
                    elif action == 8:
                        # output(out_lck, "Please insert Network Interface") nella funzione set_ttl non richiede interfaccia
                        # interface = input()  # manca gestione errore

                        output(out_lck, "Please insert the number of TTL")  # Da controllare
                        ttl = input()
                        try:
                            str_ttl = str(ttl)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            rules.set_TTL(out_lck, str_ttl)
                    # Limita ping
                    elif action == 9:
                        rules.lim_risp_ping(out_lck)
                    # SYN
                    elif action == 10:
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
                                output(out_lck, "1: TCP\n2: UDP\n3: ICMP")
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
                                        output(out_lck, "Option not available")
            elif main_menu == 4:
                rules.flush_tc(out_lck)
            elif main_menu == 5:
                rules.show_tc(out_lck)
            elif main_menu == 6:
                # Show logs
                print("logs")
            # elif main_menu == 6:
            #     output(out_lck, "Please insert destination IP")
            #     destinazione = input()
            #     try:
            #         dest = str(destinazione)
            #     except ValueError:
            #         output(out_lck, "A number is required")
            #
            #     output(out_lck, "Please insert port")
            #     porta = input()
            #     try:
            #          port = str(porta)
            #     except ValueError:
            #         output(out_lck, "A number is required")
            #
            #     c = Connection(dest, None, port, out_lck)
            #     c.client_server()
            #     output(out_lck, "Routing finish!\n")


