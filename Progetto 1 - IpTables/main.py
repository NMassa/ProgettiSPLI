import threading
import sys
import os
from helpers.helpers import output
from helpers.connection import Connection
from helpers import config
from helpers.helpers import loop_menu
#import iptc     #Daniele: potrebbe servire in un secondo momento...
from helpers import rules
from helpers import server
import subprocess
import os

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
                                                    "Apply iptables rules ",
                                                    "Reset iptables rules ",
                                                    "Show iptables",
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
                        protocol = "tcp"
                    elif protocol == 2:
                        protocol = "udp"

                    output(out_lck, "Selected protocol: %s" % protocol)

                    port = None
                    output(out_lck, "Insert port number:")

                    while port is None:
                        try:
                            option = input()
                        except SyntaxError:
                            option = None

                        if option is None:
                            output(out_lck, "Please insert port number")
                        else:
                            try:
                                int_option = int(option)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                port = int_option

                    output(out_lck, "Selected port: %i" % port)

                    subprocess.Popen(["xterm", "-e", "python3 ./helpers/server.py " + protocol + " " + str(port)])

                    # proc = subprocess.Popen(args=["gnome-terminal", "--disable-factory", " --command=python ./helpers/server.py.bak"],
                    #                         stdin=subprocess.PIPE, stdout=subprocess.PIPE, preexec_fn=os.setpgrp)
                    # c = Connection(None, protocol, port, my_ip, out_lck)
                    # try:
                    #     c.listen()
                    #     output(out_lck, "Listening on port %s.." % port)
                    # except Exception:                               # Daniele: non so che Exception da il multithreading
                    #     output(out_lck, "Thread not initialized")
            elif main_menu == 3:
                action = loop_menu(out_lck, "action", [ "Block Protocol",
                                                        "Block IP source",
                                                        "Block Port",
                                                        "Port Forwarding",
                                                        "Block inbound or outbound traffic",
                                                        "Redirection (destination)",
                                                        "Packet alteration (ttl)"])

                if action is not None:
                    # Blocco Protocollo
                    if action == 1:
                        output(out_lck, "Please select the protocol")
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
                                output(out_lck, "Option not available")
                    # Blocco IP
                    elif action == 2:
                        output(out_lck, "Please insert the number of the host (or class)")
                        option = input()
                        host = config._base + option
                        rules.block_IPsorg(out_lck, "%s" % host)
                    # Blocco Porta
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
                    # Port Forwarding
                    elif action == 4:
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
                                            rules.port_forw(out_lck, "tcp", config._base + ip1, dport, dport2)

                                        elif protocol == 2:
                                            rules.port_forw(out_lck, "udp", config._base + ip1, dport, dport2)

                                        elif protocol == 3:
                                            rules.port_forw(out_lck, "icmp", config._base + ip1, dport, dport2)
                                        else:
                                            output(out_lck, "Option not available")
                    # Block inbound or outbound traffic
                    elif action == 5:
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
                                            rules.block_input(out_lck, config._base + dip, port, "tcp")
                                        elif protocol == 2:
                                            rules.block_input(out_lck, config._base + dip, port, "udp")
                                        elif protocol == 3:
                                            rules.block_input(out_lck, config._base + dip, port, "icmp")
                                        else:
                                            output(out_lck, "Option not available")
                                    elif int_option == 2:

                                        output(out_lck, "Insert destination:")
                                        dip = input()

                                        if protocol == 1:
                                            rules.block_output(out_lck, config._base + dip, port, "tcp")
                                        elif protocol == 2:
                                            rules.block_output(out_lck, config._base + dip, port, "udp")
                                        elif protocol == 3:
                                            rules.block_output(out_lck, config._base + dip, port, "icmp")
                                        else:
                                            output(out_lck, "Option not available")
                                    else:
                                        output(out_lck, "Option not available")


                    # Redirect
                    elif action == 6:
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
                    elif action == 7:
                        # output(out_lck, "Please insert Network Interface") nella funzione set_ttl non richiede interfaccia
                        # interface = input()  # manca gestione errore
                        ip_sorg = None
                        ip_dest = None
                        output(out_lck, "Please insert the number of TTL")  # Da controllare
                        ttl = input()
                        try:
                            str_ttl = str(ttl)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            output(out_lck, "Please source IP: ")
                            ip = input()
                            try:
                                ip_sorg = config._base + str(ttl)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                output(out_lck, "Please destination IP: ")
                                ip = input()
                                try:
                                    ip_dest = config._base + str(ttl)
                                except ValueError:
                                    output(out_lck, "A number is required")
                                rules.set_TTL(out_lck, ip_sorg, ip_dest, str_ttl)

                    # Limita ping
                    elif action == 8:
                        rules.lim_risp_ping(out_lck)
                    # SYN
                    elif action == 9:
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
                rules.flush_tables(out_lck)
            elif main_menu == 5:
                rules.show_tables(out_lck)
            elif main_menu == 6:
                # Show logs
                output(out_lck, "\nShow LOG, select prefix: ")
                prefix = loop_menu(out_lck, "protocol", ["[Drop_Packet]",
                                                         "[Pre_Mangle]",
                                                         "[Post_Mangle]",
                                                         "[Redirect_Packet]"])
                if prefix == 1:
                    prefix = "[Drop_Packet]"
                elif prefix == 2:
                    prefix = "[Pre_Mangle]"
                elif prefix == 3:
                    prefix = "[Post_Mangle]"
                elif prefix == 4:
                    prefix = "[Redirect_Packet]"
                cmd = "grep -in " + prefix + " /var/log/iptables.log | tail -10"
                output(out_lck, "\ncommand: %s" % cmd)
                failed = os.system(cmd)
                if not failed:
                    output(out_lck, "\nApplied rules:")
                    output(out_lck, cmd)


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


