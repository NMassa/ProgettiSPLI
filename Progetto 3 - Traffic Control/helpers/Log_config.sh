#!/bin/bash
cd /etc/rsyslog.d/
rm my_iptables.conf
touch my_iptables.conf

echo ':msg,contains,"[Drop_Packet]" /var/log/iptables.log' >> my_iptables.conf
echo ':msg,contains,"[Pre_Mangle]" /var/log/iptables.log' >> my_iptables.conf
echo ':msg,contains,"[Post_Mangle]" /var/log/iptables.log' >> my_iptables.conf
echo ':msg,contains,"[Redirect_Packet]" /var/log/iptables.log' >> my_iptables.conf
#echo ':msg,contains,"[]" /var/log/iptables.log' >> my_iptables.conf



service rsyslog restart

