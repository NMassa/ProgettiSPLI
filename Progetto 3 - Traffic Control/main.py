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
        #output(out_lck, "Insert your IP: ")


        main_menu = loop_menu(out_lck, "action", [  "Apply tc rules ",
                                                    "Reset tc rules ",
                                                    "Show tc rules" ])
        if main_menu is not None:
            if main_menu == 1:
                action = loop_menu(out_lck, "action", [ "Delay",
                                        "Delay Random",
                                        "Lost Packets",
                                        "Duplicate",
                                        "Corrupt",
                                        "Packet alteration (Mark)",
                                        "Limit bit-rate"])

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
                                rules.delay(out_lck, "wlp2s0",num)
                            elif device == 2:
                                rules.delay(out_lck, "lo",num)
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
                                rules.delay(out_lck, "wlp2s0",num,num2)
                            elif device == 2:
                                rules.delay(out_lck, "lo",num,num2)
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
                                     rules.lost_pck(out_lck, "wlp2s0", n)
                                elif device == 2:
                                     rules.lost_pck(out_lck, "lo", n)
                                else:
                                     output(out_lck, "Option not available")
                    # Duplicate
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
                                     rules.duplicate(out_lck, "wlp2s0", n)
                                elif device == 2:
                                     rules.duplicate(out_lck, "lo", n)
                                else:
                                     output(out_lck, "Option not available")
                    # Corrupt Packets
                    elif action == 5:
                        output(out_lck, "Please insert % of corruption:")
                        n = input()
                        try:
                            num = str(n)
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
                                rules.corrupt(out_lck, "wlp2s0", num)
                            elif device == 2:
                                rules.corrupt(out_lck, "lo", num)
                            else:
                                output(out_lck, "Option not available")
                    # Alterazione pacchetto (mangle MARK)
                    elif action == 6:
                        # output(out_lck, "Please insert Network Interface") nella funzione set_ttl non richiede interfaccia
                        # interface = input()  # manca gestione errore

                        output(out_lck, "Please insert the number of MARK")
                        mark = input()
                        try:
                            str_mark = str(mark)
                        except ValueError:
                            output(out_lck, "A number is required")
                        else:
                            rules.set_MARK(out_lck, str_mark)
                    # Limita bit-rate
                    elif action == 7:
                            output(out_lck, "Please insert destination:")
                            dest = input()

                            output(out_lck, "Please select Wlan or Eth")
                            output(out_lck, "\n1: Wlan\n2: Eth")
                            dev = input()
                            try:
                                device = int(dev)
                            except ValueError:
                                output(out_lck, "A number is required")
                            output(out_lck, "Please select Kbpss or Mbpss")
                            output(out_lck, "\nk: Kbit\nm: Mbits")
                            bit = input()
                            try:
                                bit1 = str(bit)
                            except ValueError:
                                output(out_lck, "A number is required")
                            else:
                                if device == 1:
                                    rules.limit_bitrate(out_lck, "wlp2s0", config._base + dest)
                                elif device == 2:
                                    rules.limit_bitrate(out_lck, "enp5s8", config._base + dest)
                                else:
                                    output(out_lck, "Option not available")

            elif main_menu == 2:
                rules.flush_tc(out_lck)
            elif main_menu == 3:
                rules.show_tc(out_lck)