echo "1" > /proc/sys/net/ipv4/ip_forward
echo "0" > /proc/sys/net/ipv4/conf/eth0/send_redirects
echo "1" > /proc/sys/net/ipv4/conf/all/rp_filter

Log
iptables -A INPUT -i eth1 -s 10.0.0.0/8 -j LOG --log-prefix "esempio di prefisso: "

Log con limite di tempo
iptables -A INPUT -i eth1 -s 10.0.0.0/8 -j LOG --log-prefix "IP_SPOOF A: "

Log su nuova chain e drop dei pacchetti
iptables -N LOGGING
iptables -A INPUT -j LOGGING
iptables -A LOGGING -m limit --limit 2/min -j LOG --log-prefix "IPTables Packet Dropped: " --log-level 7
iptables -A LOGGING -j DROP

Blocca sorgente IP
iptables -I INPUT -s 202.54.1.2 -j DROP

Blocca protocollo
iptables -t filter -A FORWARD -p udp -s 0/0 -d 0/0 -j DROP[Invio]

Blocca porta
iptables -A INPUT -i eth1 -p tcp --dport 80 -j DROP

Blocca porta solo per indirizzo (o classe)
iptables -A INPUT -i eth1 -p tcp -s 192.168.1.0/24 --dport 80 -j DROP

Blocca in uscita per indirizzo (o classe)
iptables -A OUTPUT -o eth1 -d 192.168.1.0/24 -j DROP

Limita le risposte al ping
iptables -A INPUT  -p icmp -m limit --limit 10/second -j ACCEPT
iptables -A INPUT  -p icmp -j DROP

Restrict the Number of Parallel Connections To a Server Per Client IP
iptables -A INPUT -p tcp --syn --dport 22 -m connlimit --connlimit-above 3 -j REJECT

Port Forwarding
iptables -t nat -A PREROUTING -p tcp -d 192.168.102.37 --dport 422 -j DNAT --to 192.168.102.37:22
iptables -A INPUT -i eth0 -p tcp --dport 422 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 422 -m state --state ESTABLISHED -j A

Ridireziona pacchetti ad un altro destinatario
iptables -A FORWARD -d 172.30.2.1 -i wlp2s0 -p tcp -m tcp --dport 3389 -j ACCEPT   #172.30.2.1 è la destinazione
iptables -t nat -A PREROUTING -d 172.30.2.3 -p tcp -m tcp --dport 3389 -j DNAT --to-destination 172.30.2.1   #172.30.2.3 è l'indirizzo della macchina "locale"
iptables -t nat -A POSTROUTING -o wlp2s0 -j MASQUERADE #serve a sostituire l'indirizzo sorgente con quello di mezzo

Ridireziona pacchetti modificando il contenuto con mangle
iptables -t mangle -A PREROUTING -i eth0 -j TTL --ttl-set 1

Load Balancing
iptables -A PREROUTING -i eth0 -p tcp --dport 443 -m state --state NEW -m nth --counter 0 --every 3 --packet 0 -j DNAT --to-destination 192.168.1.101:443
iptables -A PREROUTING -i eth0 -p tcp --dport 443 -m state --state NEW -m nth --counter 0 --every 3 --packet 1 -j DNAT --to-destination 192.168.1.102:443
iptables -A PREROUTING -i eth0 -p tcp --dport 443 -m state --state NEW -m nth --counter 0 --every 3 --packet 2 -j DNAT --to-destination 192.168.1.103:443

Allow incoming SSH
iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT

Allow incoming HTTP
iptables -A INPUT -i eth0 -p tcp --dport 80 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 80 -m state --state ESTABLISHED -j ACCEPT

Allow outgoing SSH
iptables -A OUTPUT -o eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A INPUT -i eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT

Allow Sendmail or Postfix traffic
iptables -A INPUT -i eth0 -p tcp --dport 25 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 25 -m state --state ESTABLISHED -j ACCEPT

Allow IMAP e IMAPS
iptables -A INPUT -i eth0 -p tcp --dport 143 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 143 -m state --state ESTABLISHED -j ACCEPT

iptables -A INPUT -i eth0 -p tcp --dport 993 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 993 -m state --state ESTABLISHED -j ACCEPT

Allow POP3 e POP3S
iptables -A INPUT -i eth0 -p tcp --dport 110 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 110 -m state --state ESTABLISHED -j ACCEPT

iptables -A INPUT -i eth0 -p tcp --dport 995 -m state --state NEW,ESTABLISHED -j ACCEPT
iptables -A OUTPUT -o eth0 -p tcp --sport 995 -m state --state ESTABLISHED -j ACCEPT

Previene DoS, limita il numero di connessioni al minuto permesse
iptables -A INPUT -p tcp --dport 80 -m limit --limit 25/minute --limit-burst 100 -j ACCEPT

Load balancing CHE FUNZIONA (una volta sola)
iptables -A FORWARD -p udp -m udp --dport 3000 -j ACCEPT

iptables -t nat -A PREROUTING -p udp --dport 3000 -m state --state NEW -m statistic --mode nth --every 2 --packet 0 -j DNAT --to-destination 192.168.1.1:3000
iptables -t nat -A PREROUTING -p udp --dport 3000 -m state --state NEW -m statistic --mode nth --every 2 --packet 1 -j DNAT --to-destination 192.168.1.3:3000
iptables -t nat -A PREROUTING -p udp --dport 3000 -m state --state NEW -m statistic --mode nth --every 3 --packet 2 -j DNAT --to-destination 192.168.1.9:3000

iptables -t nat -A POSTROUTING -j ACCEPT
iptables -t nat -A POSTROUTING -j MASQUERADE