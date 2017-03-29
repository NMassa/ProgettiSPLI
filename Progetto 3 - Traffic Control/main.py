import threading
import sys
from helpers.helpers import output
from helpers.connection import Connection
from helpers import config
from helpers.helpers import loop_menu
import subprocess
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


        main_menu = loop_menu(out_lck, "action", [  "Send messages",
                                                    "Receive messages",
                                                    "Apply tc rules",
                                                    "Reset tc rules",
                                                    "Show tc rules" ])
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
            elif main_menu == 3:
                action = loop_menu(out_lck, "action", [ "Delay",
                                        "Delay Random",
                                        "Lost Packets",
                                        "Duplicate & Corrupt",
                                        "Re-ordering",
                                        "Limit bit-rate for destination host"])

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
                        output(out_lck, "1: Wlan\n2: Eth")
                        dev = input()
                        try:
                            device = int(dev)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            if device == 1:
                                rules.delay(out_lck, "wlp2s0", num)
                            elif device == 2:
                                rules.delay(out_lck, "enp0s3", num)
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
                        output(out_lck, "1: Wlan\n2: Eth")
                        dev = input()
                        try:
                            device = int(dev)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            if device == 1:
                                rules.delay2(out_lck, "wlp2s0",num,num2)
                            elif device == 2:
                                rules.delay2(out_lck, "enp5s8",num,num2)
                            else:
                                output(out_lck, "Option not available")
                    # Lost Packets
                    elif action == 3:
                        output(out_lck, "Please insert the number %: ")
                        option = input()
                        output(out_lck, "Please select Wlan or Eth")
                        output(out_lck, "1: Wlan\n2: Eth")
                        dev = input()
                        try:
                            device = int(dev)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            if device == 1:
                                rules.lost_pck(out_lck, "wlp2s0", option)
                            elif device == 2:
                                rules.lost_pck(out_lck, "enp5s8", option)
                            else:
                                output(out_lck, "Option not available")
                    # Duplicate




                    # Corrupt and Duplicate Packets
                    elif action == 4:
                        output(out_lck, "Please insert % of corruption:")
                        n = input()
                        try:
                            num = str(n)
                        except ValueError:
                            output(out_lck, "A number is required")
                        output(out_lck, "Please insert % of duplicate:")
                        n = input()
                        try:
                            num2 = str(n)
                        except ValueError:
                            output(out_lck, "A number is required")
                        output(out_lck, "Please select Wlan or Eth")
                        output(out_lck, "1: Wlan\n2: Eth")
                        dev = input()
                        try:
                            device = int(dev)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            if device == 1:
                                rules.corrupt(out_lck, "wlp2s0", num, num2)
                            elif device == 2:
                                rules.corrupt(out_lck, "enp5s8", num, num2)
                            else:
                                output(out_lck, "Option not available")

                    elif action == 5:
                        output(out_lck, "Please select Wlan or Eth")
                        output(out_lck, "1: Wlan\n2: Eth")
                        dev = input()

                        output(out_lck, "Please insert gap number")
                        gap = input()

                        output(out_lck, "Please insert delay time (ms)")
                        delay = input()

                        output(out_lck, "Please probability of reordering (%)")
                        probability = input()
                        try:
                            device = int(dev)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            if device == 1:
                                rules.reordering(out_lck, "wlp2s0", probability, gap, delay)
                            elif device == 2:
                                rules.reordering(out_lck, "enp5s8", probability, gap, delay)

                    # Limita bit-rate
                    elif action == 6:
                        output(out_lck, "Please insert destination:")
                        dest = input()
                        output(out_lck, "Insert Max Bandwidth:")
                        band = input()
                        output(out_lck, "Insert Number of the subclass:")
                        subclass = input()
                        output(out_lck, "Insert Mark Number:")
                        mark = input()
                        output(out_lck, "Please select Wlan or Eth")
                        output(out_lck, "1: Wlan\n2: Eth")
                        dev = input()
                        try:
                            device = int(dev)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            if device == 1:
                                rules.limit_bitrate(out_lck, "wlp2s0", config._base + dest, band, mark, subclass)
                            elif device == 2:
                                rules.limit_bitrate(out_lck, "enp5s8", config._base + dest, band, mark, subclass)
                            else:
                                output(out_lck, "Option not available")

            elif main_menu == 4:
                rules.flush_tc(out_lck)
            elif main_menu == 5:
                rules.show_tc(out_lck)