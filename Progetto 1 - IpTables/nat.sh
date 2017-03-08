#!/bin/sh

iptables -A FORWARD -d 172.30.2.1 -i wlp2s0 -p tcp -m tcp --dport 3389 -j ACCEPT   #172.30.2.1 è la destinazione

iptables -t nat -A PREROUTING -d 172.30.2.3 -p tcp -m tcp --dport 3389 -j DNAT --to-destination 172.30.2.1   #172.30.2.3 è l'indirizzo della macchina "locale"

iptables -t nat -A POSTROUTING -o wlp2s0 -j MASQUERADE #serve a sostituire l'indirizzo sorgente con quello di mezzo


