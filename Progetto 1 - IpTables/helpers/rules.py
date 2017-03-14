import os
from helpers.helpers import output


# Show tables state
def show_tables(out_lck):
    cmd = "iptables -L"
    cmd1 = "iptables -t nat -L"
    os.system(cmd)
    os.system(cmd1)


# Flush di tutte le tavole
def flush_tables(out_lck):
    cmd = "iptables -X"
    cmd1 = "iptables -F"
    cmd2 = "iptables -t nat -X"
    cmd3 = "iptables -t nat -F"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    failed2 = os.system(cmd2)
    failed3 = os.system(cmd3)

    if not (failed and failed1 and failed2 and failed3):
        output(out_lck, "Applied rules: ")
        output(out_lck, cmd)
        output(out_lck, cmd1)
        output(out_lck, cmd2)
        output(out_lck, cmd3)
    else:
        output(out_lck, "Rules not applied")


# Blocca sorgente IP
def block_IPsorg(out_lck, ip):
    cmd = "iptables -I INPUT -s " + ip + " -j DROP"
    failed = os.system(cmd)
    if not failed:
        output(out_lck, "Applied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")


# Blocca protocollo
def block_proto(out_lck, proto):
    cmd = "iptables -t filter -A FORWARD -p " + proto + " -s 0/0 -d 0/0 -j DROP"
    failed = os.system(cmd)
    if not failed:
        output(out_lck, "Applied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")


# Blocca porta
def block_port(out_lck, interface, proto, porta):
    cmd = "iptables -A INPUT -i " + interface + " -p " + proto + " --dport " + porta + " -j DROP"
    failed = os.system(cmd)
    if not failed:
        output(out_lck, "Applied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")


# Blocca porta solo per indirizzo (o classe)
def block_sel_port(out_lck, interface ,proto, ip,porta):
    cmd = "iptables -A INPUT -i " + interface + " -p " + proto + " -s " + ip + " --dport " + porta + " -j DROP"
    failed = os.system(cmd)
    if not failed:
        output(out_lck, "Applied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")


# Blocca in uscita per indirizzo (o classe)
def block_out_sel(out_lck, interface, ip):
    cmd = "iptables -A OUTPUT -o " + interface + " -d " + ip + " -j DROP"
    failed = os.system(cmd)
    if not failed:
        output(out_lck, "Applied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")


# Limita le risposte al ping
def lim_risp_ping(out_lck):
    cmd = "iptables -A INPUT  -p icmp -m limit --limit 10/second -j ACCEPT"
    cmd1 = "iptables -A INPUT  -p icmp -j DROP"
    failed = os.system(cmd)
    failed2 = os.system(cmd1)
    if not (failed and failed2):
        output(out_lck, "Applied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
    else:
        output(out_lck, "Rules not applied")


# Restrict the Number of Parallel Connections To a Server Per Client IP
def rest_conn_Ip(out_lck, proto, porta, nconn):
    cmd = "iptables -A INPUT -p " + proto + " --syn --dport " + porta + " -m connlimit --connlimit-above " + nconn + " -j REJECT"
    failed = os.system(cmd)
    if not failed:
        output(out_lck, "Applied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")


# Port Forwarding
def port_forw(out_lck, interf, proto, ip1, ip2, port):
    cmd = "iptables -t nat -A PREROUTING -p " + proto + " -d " + ip1 + " --dport " + port + " -j DNAT --to " + ip2
    cmd1 = "iptables -A INPUT -i " + interf + " -p " + proto + " --dport " + port + " -m state --state NEW,ESTABLISHED -j ACCEPT"
    cmd2 = "iptables -A OUTPUT -o " + interf + " -p " + proto + " --sport " + port + " -m state --state ESTABLISHED -j ACCEPT"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    failed2 = os.system(cmd2)
    if not (failed and failed1 and failed2):
        output(out_lck, "Applied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
        output(out_lck, cmd2)
    else:
        output(out_lck, "Rules not applied")


# Ridireziona pacchetti ad un altro destinatario
def redirection(out_lck, ipdest, iplocal, proto, port):
    cmd = "iptables -A FORWARD -d " + ipdest + " -p " + proto + " -m " + proto + " --dport " + port + " -j ACCEPT"
    cmd1 = "iptables -t nat -A PREROUTING -d " + iplocal + " -p " + proto + " -m " + proto + " --dport " + port + " -j DNAT"
    #cmd2 = "iptables -t nat -A POSTROUTING -j MASQUERADE"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    #os.system(cmd2)
    if not (failed and failed1):
        output(out_lck, "Applied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
    else:
        output(out_lck, "Rules not applied")


#Allow incoming SSH
#iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
#iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
def inc_ssh(out_lck,interface,proto,porta):
    cmd= "iptables -A INPUT -i "+interface+" -p "+proto+" --dport "+porta+" -m state --state NEW,ESTABLISHED -j ACCEPT"
    cmd1="iptables -A OUTPUT -o "+interface+" -p "+proto+" --sport "+porta+" -m state --state ESTABLISHED -j ACCEPT"
    os.system(cmd)
    os.system(cmd1)
    output(out_lck, "Regola 1 applicata:\n####################################\n" + cmd + "\n####################################\n")
    output(out_lck, "Regola 2 applicata:\n####################################\n" + cmd1 + "\n####################################\n")

#Allow outgoing SSH
#iptables -A OUTPUT -o eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
#iptables -A INPUT -i eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
def out_ssh(out_lck,interface,proto,porta):
    cmd= "iptables -A OUTPUT -o "+interface+" -p "+proto+" --dport "+porta+" -m state --state NEW,ESTABLISHED -j ACCEPT"
    cmd1="iptables -A INPUT -i "+interface+" -p "+proto+" --sport "+porta+" -m state --state ESTABLISHED -j ACCEPT"
    os.system(cmd)
    os.system(cmd1)
    output(out_lck, "Regola 1 applicata:\n####################################\n" + cmd + "\n####################################\n")
    output(out_lck, "Regola 2 applicata:\n####################################\n" + cmd1 + "\n####################################\n")

def set_TTL(out_lck,ttl):
    cmd = "iptables - t mangle - A PREROUTING - i wlp2s0 - j TTL - -ttl - set " +ttl
    os.system(cmd)
    output(out_lck, "Regola 1 applicata:\n####################################\n" + cmd + "\n####################################\n")
