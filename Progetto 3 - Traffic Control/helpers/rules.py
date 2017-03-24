import os
from helpers.helpers import output


# Show tables state
def show_tc(out_lck):
    cmd = "tc -s qdisc"
    os.system(cmd)
    output(out_lck, "\n")


# Flush di tutte le tavole
def flush_tc(out_lck):
    cmd = "tc qdisc del dev lo root"
    cmd1 = "tc qdisc del dev wlp2s0 root"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    if not (failed and failed1):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
    else:
        output(out_lck, "Rules not applied")
    output(out_lck, "\n")


# Delay
def delay(out_lck, dev,num):
    cmd = "tc qdisc add dev " + dev + " root netem delay " + num + "ms"
    failed = os.system(cmd)
    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")
    output(out_lck, "\n")

# Delay Random
def delay(out_lck, dev,num):
    cmd = "tc qdisc change dev " + dev + " root netem delay " + num + "ms " + num2 + "ms"
    failed = os.system(cmd)
    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")
    output(out_lck, "\n")

# Lost packets
def lost_pck(out_lck, dev, n):
    cmd = "tc qdisc change dev " + dev + " root netem loss " + n + "%"
    failed = os.system(cmd)
    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Duplicate
def duplicate(out_lck, dev, n):
    cmd = "tc qdisc change dev " + dev + " root netem duplicate " + n + "%"
    failed = os.system(cmd)
    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")
# Blocca porta solo per indirizzo (o classe)
def block_sel_port(out_lck, interface, proto, ip, porta):
    cmd = "iptables -N LOGGING"
    cmd1 = "iptables -A FORWARD -i " + interface + " -p " + proto + " -s " + ip + " --dport " + porta + " -j LOGGING"
    cmd2 = "iptables -A LOGGING  -j LOG --log-prefix "'[Drop_Packet]'" --log-level 4"
    cmd3 = "iptables -A LOGGING -j DROP"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    failed2 = os.system(cmd2)
    failed3 = os.system(cmd3)
    if not (failed and failed1 and failed2 and failed3):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
        output(out_lck, cmd2)
        output(out_lck, cmd3)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Blocca in input
def block_input(out_lck, dip, dport, protocol):
    cmd = "iptables -A INPUT -p " + protocol + " -d " + dip + " --dport " + dport + " -j DROP"
    failed = os.system(cmd)
    if not failed:
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Blocca in uscita
def block_output(out_lck, dip, dport, protocol):
    cmd = "iptables -A OUTPUT -p " + protocol + " -d " + dip + " --dport " + dport + " -j DROP"
    failed = os.system(cmd)
    if not failed:
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Limita le risposte al ping
def lim_risp_ping(out_lck):
    cmd = "iptables -A INPUT -p icmp --icmp-type echo-request -m limit --limit 4/minute --limit-burst 3 -j ACCEPT"
    #cmd1 = "iptables -A INPUT -p icmp -j DROP"
    failed = os.system(cmd)
    #failed2 = os.system(cmd1)
    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        #output(out_lck, cmd1)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Restrict the Number of Parallel Connections To a Server Per Client IP
def rest_conn_Ip(out_lck, proto, porta, nconn):
    cmd = "iptables -A INPUT -p " + proto + " --syn --dport " + porta + " -m connlimit --connlimit-above " + nconn + " -j REJECT"
    failed = os.system(cmd)
    if not failed:
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Port Forwarding
def port_forw(out_lck, proto, ip1, port, port2):
    cmd = "iptables -t nat -A PREROUTING -p " + proto + " -d " + ip1 + " --dport " + str(port) + " -j DNAT --to " + ip1 + ":" + str(port2)
    # in teoria non servono
    #cmd1 = "iptables -A INPUT -i " + interf + " -p " + proto + " --dport " + port + " -m state --state NEW,ESTABLISHED -j ACCEPT"
    #cmd2 = "iptables -A OUTPUT -o " + interf + " -p " + proto + " --sport " + port + " -m state --state ESTABLISHED -j ACCEPT"
    failed = os.system(cmd)
    #failed1 = os.system(cmd1)
    #failed2 = os.system(cmd2)
    #if not (failed and failed1 and failed2):
    if not failed:
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        #output(out_lck, cmd1)
        #output(out_lck, cmd2)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Ridireziona pacchetti ad un altro destinatario
def redirection(out_lck, ipdest, iplocal, proto, port):
    cmd = "iptables -A FORWARD -d " + ipdest + " -p " + proto + " -m " + proto + " --dport " + port + " -j ACCEPT"
    cmd1 = "iptables -t nat -A PREROUTING -d " + iplocal + " -p " + proto + " -m " + proto + " --dport " + port + " -j DNAT"
    #cmd2 = "iptables -t nat -A POSTROUTING -j MASQUERADE"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    #os.system(cmd2)
    if not (failed and failed1):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Allow incoming SSH
# iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
# iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
def inc_ssh(out_lck, interface):
    cmd = "iptables -A INPUT -i " + interface + " -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT"
    cmd1 = "iptables -A OUTPUT -o " + interface + " -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    if not (failed and failed1):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Allow outgoing SSH
# iptables -A OUTPUT -o eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
# iptables -A INPUT -i eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
def out_ssh(out_lck, interface):
    cmd = "iptables -A OUTPUT -o " + interface + " -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT"
    cmd1 = "iptables -A INPUT -i " + interface + " -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    if not (failed and failed1):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Modifica ttl
def set_MARK(out_lck, mark):
    cmd = "iptables -t mangle -A FORWARD -j MARK --set-mark " + mark
    failed = os.system(cmd)
    if not failed:
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")

# Corrompe pacchetti
def corrupt(out_lck, dev,num):
    cmd = "tc qdisc change dev " + dev + " root netem corrupt " + num + "%"
    failed = os.system(cmd)
    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")
    output(out_lck, "\n")

#Bit-rate limitata       DA CONTROLLARE--- lanciando questi comandi da terminale funzionano, qua mi danno errore
def limit_bitrate(out_lck, dev,num,bit):
    cmd = "tc qdisc add dev " + dev + " handle 1: root htb default 11"
    #cmd1 = "tc class add dev eth0 parent 1: classid 1:1 htb rate 1kbps"
    cmd2 = "tc class add dev " + dev + " parent 1:1 classid 1:11 htb rate " + num + "  " + bit + "bps"
    failed = os.system(cmd)
    failed2 = os.system(cmd2)
    if not (failed and failed2):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck,cmd2)
    else:
        output(out_lck, "Rules not applied")
    output(out_lck, "\n")