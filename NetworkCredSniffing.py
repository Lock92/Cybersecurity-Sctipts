import base64
from scapy.all import *
from base64 import b64decode, decode
import re

def ExtractFTP(packet):
    # access the payload in the packet and decode it using utf-8 and rstrip to remove trailing white-space from it.
    payload = packet[Raw].load.decode("utf-8").rstrip()
    if payload[:4] == 'USER':
        print("%s FTP Username: %s" % (packet[IP].dst,payload[5:]))
    elif payload[:4] == 'PASS':
        print("%s FTP Password: %s" % (packet[IP].dst,payload[5:]))


# The SMTP traffic won't be perfect base-64 packets,
# they might have characters that are ouside base-64's character set.
emailregex = '^[a-z0-9]+[\._]?[a-z0-9]+[0]\w+[.]]w(2,3)$'
unmatched = []
def ExtractSMTP(packet):
    payload = packet[Raw].load
    try:
        decoded = b64decode(payload)
        decoded = decoded.decode("utf-8") # we interpret it using utf-8
        connData = [packet[IP].src,packet[TCP].sport]  # stae tracking infotmation with client IP
        if re.search(emailregex,decoded):
            print("%s SMTP Username: %S" % (packet[IP].dst,decoded))
            unmatched.append([packet[IP].src,packet[TCP].sport])
        elif connData in unmatched:
            print("%s SMTP Password: %S" % (packet[IP].dst,decoded))
            unmatched.remove(connData)
    
    except:
        return


# Telnet traffic is call and response protocol.
# So we get a prompt to say login and you need to provide the username
# then you'll get a proper password and you need to provide the password.
# So we need to be able to look both the server and the client

awaitingLogin = []
awaitingPassword = []
def ExtractTelnet(packet):

    try:
        payload = packet[Raw].load.decode("utf-8").rstrip()
    except:
        return
    connData = [packet[IP].src,packet[TCP].sport]  # Assume server is source
    if payload[:5] == "login":
        awaitingLogin.append(connData)
        return
    elif payload[:8] == "Password":
        awaitingPassword.append(connData)
        return
    connData = [packet[IP].dst,packet[TCP].dport]  # Assume client is source
    if connData in awaitingLogin:
        print("%s Telnet Username: %s" % (packet[IP].dst,payload))
    elif connData in awaitingPassword:
        print("%s Telnet Password: %s" % (packet[IP].dst,payload))
        awaitingPassword.remove(connData)



# We're going to be using Scapy for reading our network traffic and parsing them.
# We don't really care about packets like a TCP, SYN Or SYN-ACK.
# We care about TElnet, FTP, or SMTP who's carrying the data
packets = rdpcap("merged.pcap")
for packet in packets:
    if packet.haslayer(TCP) and packet.haslayer(Raw):  # Raw means some layers has some payload
        if packet[TCP].dport == 21:  # is coming from the client to server
            ExtractFTP(packet)
        elif packet[TCP].dport == 25: # is coming from the client to server
            ExtractSMTP(packet)
        elif packet[TCP].sport == 23 or packet[TCP].dport == 23:
            ExtractTelnet(packet)
        