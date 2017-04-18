from scapy.all import *
from scapy.layers.inet import TCP

def parse(pkt):
    #pkt.show()
    print(pkt[TCP].payload)

#filename = "received"
#fout = open('received/' + filename, "wb")

a = sniff(filter="tcp and (port 3000)",  prn=parse)

