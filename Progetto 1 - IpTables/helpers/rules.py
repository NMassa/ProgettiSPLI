import os
from helpers.helpers import output

#Show tables state

def show_tables(out_lck):
    cmd = "iptables -L"
    cmd1 = "iptables -t nat -L"
    os.system(cmd)
    os.system(cmd1)
    output(out_lck, "\nRegola applicata:\n####################################\n" + cmd + "\n####################################\n")
    output(out_lck, "\nRegola applicata:\n####################################\n" + cmd1 + "\n####################################\n")

#Flush di tutte le tavole

def flush_tables(out_lck):
    cmd = "iptables -X"
    cmd1 = "iptables -F"
    cmd2 = "iptables -t nat -X"
    cmd3 = "iptables -t nat -F"
    os.system(cmd)
    os.system(cmd1)
    os.system(cmd2)
    os.system(cmd3)
    output(out_lck,
           "\nRegola applicata:\n####################################\n" + cmd + "\n####################################\n")
    output(out_lck,
           "\nRegola applicata:\n####################################\n" + cmd1 + "\n####################################\n")
    output(out_lck,
           "\nRegola applicata:\n####################################\n" + cmd2 + "\n####################################\n")
    output(out_lck,
           "\nRegola applicata:\n####################################\n" + cmd3 + "\n####################################\n")

# Blocca sorgente IP

def block_IPsorg(out_lck, ip):
    cmd = "iptables -I INPUT -s " + ip + " -j DROP"
    os.system(cmd)
    output(out_lck, "\nRegola applicata:\n####################################\n" + cmd + "\n####################################\n")

# Blocca protocollo

def block_proto(out_lck, proto):
    cmd = "iptables -t filter -A FORWARD -p " + proto + " -s 0/0 -d 0/0 -j DROP"
    os.system(cmd)
    output(out_lck, "\nRegola applicata:\n####################################\n" + cmd + "\n####################################\n")

# Blocca porta

def block_port(out_lck, interface, proto, porta):
    cmd = "iptables -A INPUT -i " + interface + " -p " + proto + " --dport " + porta + " -j DROP"
    os.system(cmd)
    output(out_lck, "\nRegola applicata:\n####################################\n" + cmd + "\n####################################\n")

#Blocca porta solo per indirizzo (o classe)

def block_sel_port(out_lck, interface ,proto, ip,porta):
    cmd = "iptables -A INPUT -i " + interface + " -p " + proto + " -s " + ip + " --dport " + porta + " -j DROP"
    os.system(cmd)
    output(out_lck, "\nRegola applicata:\n####################################\n" + cmd + "\n####################################\n")

# Blocca in uscita per indirizzo (o classe)

def block_out_sel(out_lck, interface, ip):
    cmd = "iptables -A OUTPUT -o " + interface + " -d " + ip + " -j DROP"
    os.system(cmd)
    output(out_lck, "\nRegola applicata:\n####################################\n" + cmd + "\n####################################\n")

# Limita le risposte al ping

def lim_risp_ping(out_lck):
    cmd = "iptables -A INPUT  -p icmp -m limit --limit 10/second -j ACCEPT"
    cmd1 = "iptables -A INPUT  -p icmp -j DROP"
    os.system(cmd)
    os.system(cmd1)
    output(out_lck, "\nRegola 1 applicata:\n####################################\n" + cmd + "\n####################################\n")
    output(out_lck, "\nRegola 2 applicata:\n####################################\n" + cmd1 + "\n####################################\n")

# Restrict the Number of Parallel Connections To a Server Per Client IP

def rest_conn_Ip(out_lck, proto, porta, nconn):
    cmd = "iptables -A INPUT -p " + proto + " --syn --dport " + porta + " -m connlimit --connlimit-above " + nconn + " -j REJECT"
    os.system(cmd)
    output(out_lck, "\nRegola applicata:\n####################################\n" + cmd + "\n####################################\n")

# Port Forwarding
def port_forw(out_lck, interf, proto, ip1, ip2, port):
    cmd = "iptables -t nat -A PREROUTING -p " + proto + " -d " + ip1 + " --dport " + port + " -j DNAT --to" + ip2
    cmd1 = "iptables -A INPUT -i " + interf + " -p " + proto + " --dport " + port + " -m state --state NEW,ESTABLISHED -j ACCEPT"
    cmd2 = "iptables -A OUTPUT -o " + interf + " -p " + proto + " --sport " + port + " -m state --state ESTABLISHED -j ACCEPT"
    os.system(cmd)
    os.system(cmd1)
    os.system(cmd2)
    output(out_lck, "\nRegola 1 applicata:\n####################################\n" + cmd + "\n####################################\n")
    output(out_lck, "\nRegola 2 applicata:\n####################################\n" + cmd1 + "\n####################################\n")
    output(out_lck, "\nRegola 3 applicata:\n####################################\n" + cmd2 + "\n####################################\n")

# Ridireziona pacchetti ad un altro destinatario

def redirection(out_lck, ipdest, iplocal, proto, port):
    cmd = "iptables -A FORWARD -d " + ipdest + " -i wlp2s0 -p tcp -m " + proto + " --dport " + port + " -j ACCEPT"
    cmd1 = "iptables -t nat -A PREROUTING -d " + iplocal + " -p tcp -m " + proto + " --dport " + port + " -j DNAT"
    cmd2 = "iptables -t nat -A POSTROUTING -o wlp2s0 -j MASQUERADE"
    os.system(cmd)
    os.system(cmd1)
    os.system(cmd2)
    output(out_lck, "Regola 1 applicata:\n####################################\n" + cmd + "\n####################################\n")
    output(out_lck, "Regola 2 applicata:\n####################################\n" + cmd1 + "\n####################################\n")
    output(out_lck, "Regola 3 applicata:\n####################################\n" + cmd2 + "\n####################################\n")

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
