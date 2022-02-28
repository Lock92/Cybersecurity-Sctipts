from scapy.all import *
# from scapy.layers.all import *
from scapy.layers.http import *
from base64 import b64decode


b64regex = b"[A-Za-z0=9+/=]+"
def extractData(data):
    data = data.rstrip()  # strip away any trailing whitespace on our data
    matches = re.findall(b64regex,data)
    for match in matches:
        if len(match) == 0:
            continue
        try:
            if not len(match) % 4 == 0:
                padnum = (4-len(match)%4)%4
                match += b"=" *padnum
            decoded = b64decode(match).decode("utf-8")
            if len(decoded) > 5 and decoded.isprintable(): # printable content
                print("DEcode: %s"%decoded)
        except:
            continue
# with Printable content, we ignoring anything that might be
# say, a download piece of malware that's a binary exectable
# which includes a lot of unprintable bytes.


# A brute force search through an HTTP request or Response packet
def extractHTTP(p):
    fields = None
    if p.haslayer(HTTPRequest):
        fields = p[HTTPRequest].fields
    else:
        fields = p[HTTPResponse].fields
    for f in fields:
        data = fields[f]
        if isinstance(data,str):   # string like cookies
            extractData(data)
        elif isinstance(data,dict):
            for d in data:
                extractData(data[d])
        elif isinstance(data,list) or isinstance(data,tuple):
            for d in data:
                extractData(d)
            


def extractRaw(p):
    extractData(p[Raw].load)

# detect http packet or something just carrying a payload of data
def analyzePackets(p):
    if p.haslayer(HTTPRequest) or p.haslayer(HTTPResponse):
        p.show()
        extractHTTP(p)
    elif p.haslayer(Raw): # check if a packet has a raw layer(data/payload of the packet)
        extractRaw(p)

sniff(prn=analyzePackets)