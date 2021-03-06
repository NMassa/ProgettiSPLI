import os
from helpers.helpers import output


# Show tables state
def show_tables(out_lck):
    cmd = "iptables -L"
    cmd1 = "iptables -t nat -L"
    cmd2 = "iptables -t mangle -L"

    output(out_lck, "\n----------------------- MAIN TABLE -----------------------\n")
    os.system(cmd)
    output(out_lck, "\n----------------------------------------------------------\n")
    output(out_lck, "\n----------------------- NAT TABLE ------------------------\n")
    os.system(cmd1)
    output(out_lck, "\n----------------------------------------------------------\n")
    output(out_lck, "\n---------------------- MANGLE TABLE ----------------------\n")
    os.system(cmd2)
    output(out_lck, "\n----------------------------------------------------------\n")
    output(out_lck, "\n")


# Flush di tutte le tavole
def flush_tables(out_lck):
    cmd = "iptables -X"
    cmd1 = "iptables -F"
    cmd2 = "iptables -t nat -X"
    cmd3 = "iptables -t nat -F"
    cmd4 = "iptables -t mangle -X"
    cmd5 = "iptables -t mangle -F"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    failed2 = os.system(cmd2)
    failed3 = os.system(cmd3)
    failed4 = os.system(cmd4)
    failed5 = os.system(cmd5)

    if not (failed and failed1 and failed2 and failed3 and failed4 and failed5):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
        output(out_lck, cmd2)
        output(out_lck, cmd3)
        output(out_lck, cmd4)
        output(out_lck, cmd5)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")

# Blocca sorgente IP
def block_IPsorg(out_lck, ip):
    cmd = "iptables -N LOGGING"
    cmd1 = "iptables -A FORWARD -s " + ip + " -j LOGGING"
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

# Blocca protocollo
def block_proto(out_lck, proto):
    cmd = "iptables -N LOGGING"
    cmd1 = "iptables -A FORWARD -p " + proto + " -s 0/0 -d 0/0 -j LOGGING"
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

# Blocca porta
def block_port(out_lck, interface, proto, porta):
    cmd = "iptables -N LOGGING"
    cmd1 = "iptables -A FORWARD -i " + interface + " -p " + proto + " --dport " + porta + " -j LOGGING"
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
    cmd = "iptables -N LOGGING"
    cmd1 = "iptables -A INPUT -p " + protocol + " -d " + dip + " --dport " + dport + " -j LOGGING"
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


# Blocca in uscita
def block_output(out_lck, dip, dport, protocol):
    # cmd = "iptables -A OUTPUT -p " + protocol + " -d " + dip + " --dport " + dport + " -j DROP"
    # failed = os.system(cmd)
    # if not failed:
    #     output(out_lck, "\nApplied rules:")
    #     output(out_lck, cmd)
    # else:
    #     output(out_lck, "Rules not applied")
    #
    # output(out_lck, "\n")
    cmd = "iptables -N LOGGING"
    cmd1 = "iptables -A OUTPUT -p " + protocol + " -d " + dip + " --dport " + dport + " -j LOGGING"
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
    cmd1 = "iptables -A REJECT -j LOG --log-prefix "'[Drop_Packet]'"  --log-level 4"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    if not (failed and failed1):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Port Forwarding
def port_forw(out_lck, proto, ip1, port, port2):
    cmd = "iptables -t nat -A PREROUTING -p " + proto + " -d " + ip1 + " --dport " + str(port) + " -j DNAT --to " + ip1 + ":" + str(port2)

    cmd1 = "iptables -A DNAT -j LOG --log-prefix "'[Redirect_Packet]'"  --log-level 4"
    # in teoria non servono
    #cmd1 = "iptables -A INPUT -i " + interf + " -p " + proto + " --dport " + port + " -m state --state NEW,ESTABLISHED -j ACCEPT"
    #cmd2 = "iptables -A OUTPUT -o " + interf + " -p " + proto + " --sport " + port + " -m state --state ESTABLISHED -j ACCEPT"
    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    #failed1 = os.system(cmd1)
    #failed2 = os.system(cmd2)
    #if not (failed and failed1 and failed2):
    if not (failed and failed1):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
        #output(out_lck, cmd1)
        #output(out_lck, cmd2)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Ridireziona pacchetti ad un altro destinatario
def redirection(out_lck, ipdest, iplocal, proto, port):
    cmd1 = "iptables -t nat -N PRELOG"
    cmd2 = "iptables -t nat -A PREROUTING -d " + iplocal + " -p " + proto + " -m " + proto + " --dport " + port + " -j PRELOG"
    cmd3 = "iptables -t nat -A PRELOG -j LOG --log-prefix "'[Pre_Redirect]'" --log-level 4"
    cmd4 = "iptables -t nat -A PRELOG -j DNAT --to-destination " + ipdest

    cmd5 = "iptables -N POSTLOG"
    cmd6 = "iptables -A FORWARD -d " + ipdest + " -p " + proto + " -m " + proto + " --dport " + port + " -j POSTLOG"
    cmd7 = "iptables -A POSTLOG -j LOG --log-prefix "'[Post_Redirect]'" --log-level 4"
    #cmd8 = "iptables -A POSTLOG -j ACCEPT"

    #cmd5 = "iptables -t nat -A POSTROUTING -j MASQUERADE"

    #failed = os.system(cmd)
    failed1 = os.system(cmd1)
    failed2 = os.system(cmd2)
    failed3 = os.system(cmd3)
    failed4 = os.system(cmd4)
    failed5 = os.system(cmd5)
    failed6 = os.system(cmd6)
    failed7 = os.system(cmd7)
    #failed8 = os.system(cmd8)

    #failed5 = os.system(cmd5)
    #os.system(cmd2)
    if not (failed1 and failed2 and failed3 and failed4 and failed5 and failed6 and failed7 ):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd1)
        output(out_lck, cmd2)
        output(out_lck, cmd3)
        output(out_lck, cmd4)
        output(out_lck, cmd5)
        output(out_lck, cmd6)
        output(out_lck, cmd7)
        #output(out_lck, cmd8)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Modifica ttl
def set_TTL(out_lck, ip_sorg, ip_dest, ttl):
    cmd = "iptables -t mangle -A FORWARD -s " + ip_sorg + " -d " + ip_dest + " -j TTL --ttl-set " + ttl

    cmd1 = "iptables -t nat -N PRELOG"
    cmd2 = "iptables -t nat -A PREROUTING -s " + ip_sorg + " -d " + ip_dest + " -j PRELOG"
    cmd3 = "iptables -t nat -A PRELOG -j LOG --log-prefix "'[Pre_Mangle]'" --log-level 4"
    cmd4 = "iptables -t nat -A PRELOG -j ACCEPT"

    cmd5 = "iptables -t nat -N POSTLOG"
    cmd6 = "iptables -t nat -A POSTROUTING -s " + ip_sorg + " -d " + ip_dest + " -j POSTLOG"
    cmd7 = "iptables -t nat -A POSTLOG -j LOG --log-prefix "'[Post_Mangle]'" --log-level 4"
    cmd8 = "iptables -t nat -A POSTLOG -j ACCEPT"

    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    failed2 = os.system(cmd2)
    failed3 = os.system(cmd3)
    failed4 = os.system(cmd4)
    failed5 = os.system(cmd5)
    failed6 = os.system(cmd6)
    failed7 = os.system(cmd7)
    failed8 = os.system(cmd8)

    if not (failed and failed1 and failed2 and failed3 and failed4 and failed5 and failed6 and failed7 and failed8):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
        output(out_lck, cmd2)
        output(out_lck, cmd3)
        output(out_lck, cmd4)
        output(out_lck, cmd5)
        output(out_lck, cmd6)
        output(out_lck, cmd7)
        output(out_lck, cmd8)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# # Allow incoming SSH
# # iptables -A INPUT -i eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
# # iptables -A OUTPUT -o eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
# def inc_ssh(out_lck, interface):
#     cmd = "iptables -A INPUT -i " + interface + " -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT"
#     cmd1 = "iptables -A OUTPUT -o " + interface + " -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT"
#     failed = os.system(cmd)
#     failed1 = os.system(cmd1)
#     if not (failed and failed1):
#         output(out_lck, "\nApplied rules:")
#         output(out_lck, cmd)
#         output(out_lck, cmd1)
#     else:
#         output(out_lck, "Rules not applied")
#
#     output(out_lck, "\n")
#
#
# # Allow outgoing SSH
# # iptables -A OUTPUT -o eth0 -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT
# # iptables -A INPUT -i eth0 -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT
# def out_ssh(out_lck, interface):
#     cmd = "iptables -A OUTPUT -o " + interface + " -p tcp --dport 22 -m state --state NEW,ESTABLISHED -j ACCEPT"
#     cmd1 = "iptables -A INPUT -i " + interface + " -p tcp --sport 22 -m state --state ESTABLISHED -j ACCEPT"
#     failed = os.system(cmd)
#     failed1 = os.system(cmd1)
#     if not (failed and failed1):
#         output(out_lck, "\nApplied rules:")
#         output(out_lck, cmd)
#         output(out_lck, cmd1)
#     else:
#         output(out_lck, "Rules not applied")
#
#     output(out_lck, "\n")
