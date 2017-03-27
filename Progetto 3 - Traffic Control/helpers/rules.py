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
    cmd = "tc qdisc add dev " + dev + " root netem delay " + num + "ms " + num2 + "ms"
    failed = os.system(cmd)
    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")
    output(out_lck, "\n")

# Lost packets
def lost_pck(out_lck, dev, n):
    cmd = "tc qdisc add dev " + dev + " root netem loss " + n + "%"
    failed = os.system(cmd)
    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")


# Duplicate
def duplicate(out_lck, dev, n):
    cmd = "tc qdisc add dev " + dev + " root netem duplicate " + n + "%"
    failed = os.system(cmd)
    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")

    output(out_lck, "\n")



# Modifica mark
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
    cmd = "tc qdisc add dev " + dev + " root netem corrupt " + num + "%"
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