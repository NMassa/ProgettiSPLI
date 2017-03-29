import os
from helpers.helpers import output


# Show tables state
def show_tc(out_lck):
    cmd = "tc -s qdisc"
    os.system(cmd)
    output(out_lck, "\n")


# Flush di tutte le tavole
def flush_tc(out_lck):
    cmd = "tc qdisc del dev enp5s8 root"
    cmd1 = "tc qdisc del dev wlp2s0 root"
    cmd2 = "iptables -t mangle -F"

    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    failed2 = os.system(cmd2)
    if not (failed and failed1 and failed2):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
        output(out_lck, cmd2)
    else:
        output(out_lck, "Rules not applied")
    output(out_lck, "\n")


# Delay
def delay(out_lck, dev, num):
    cmd = "tc qdisc add dev " + dev + " root netem delay " + num + "ms"
    failed = os.system(cmd)
    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")
    output(out_lck, "\n")

# Delay Random
def delay2(out_lck, dev, num, num2):
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
    cmd = "iptables -t mangle -A POSTROUTING -j MARK --set-mark " + mark
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
def limit_bitrate(out_lck, dev, dest):
    cmd = "tc qdisc add dev " + dev + " handle 1: root htb"
    cmd1 = "tc class add dev " + dev + " parent 1: classid 1:1 htb rate 100Mbps"
    cmd2 = "tc class add dev " + dev + " parent 1:1 classid 1:10 htb rate 10kbps ceil 10kbps prio 1"
    cmd3 = "tc filter add dev "+ dev + " parent 1:0 prio 1 protocol ip handle 10 fw flowid 1:10"
    cmd4 = "iptables -A POSTROUTING -t mangle -d " + dest + " -p tcp -j MARK --set-mark 10"

    failed = os.system(cmd)
    failed1 = os.system(cmd1)
    failed2 = os.system(cmd2)
    failed3 = os.system(cmd3)
    failed4 = os.system(cmd4)
    if not (failed and failed1 and failed2 and failed3 and failed4):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
        output(out_lck, cmd1)
        output(out_lck, cmd2)
        output(out_lck, cmd3)
        output(out_lck, cmd4)
    else:
        output(out_lck, "Rules not applied")
    output(out_lck, "\n")


def reordering(out_lck, dev, probability, gap, delay):
    cmd = "tc qdisc add dev " + dev + " root netem delay " + delay + "ms reorder " + probability + " gap " + gap
    failed = os.system(cmd)

    if not (failed):
        output(out_lck, "\nApplied rules:")
        output(out_lck, cmd)
    else:
        output(out_lck, "Rules not applied")
    output(out_lck, "\n")