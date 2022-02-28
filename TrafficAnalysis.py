from scapy.all import *
from scapy.layers.http import *
from pandas import Series
from Entropy import fieldEntropy
from CheckEncoding import checkEncoding


protocols = {}
targetLayers = ("Raw","DNS","HTTP Request","HTTP Response")
def ProtocolAnalysis(p):
    layers = p.layers()
    protos = [l.name for l in[p.getlayer(i) for i in range(len(
            layers))]if l.name in targetLayers] 
    for proto in protos:
        if proto in protocols:
            protocols[proto] += 1
        else:
            protocols[proto] = 1
    return protos

def getFieldName(p,f):
    name = ""
    l = 0
    while p.getlayer(l).name != f:
        name += "%s:" % p.getlayer(l).name
        l += 1
    name += "%s" % p.getlayer(l).name
    return name
# we're identify which fields within this particular packet
# could be used to store useful information.
fields = {}
def fieldAnalysis(p,proto):
    x = getFieldName(p,proto)
    for f in p[proto].fields:
        v = p[proto].fields[f]
        e = fieldEntropy(v) # how much opportunity we have to store random looking data.
        if e:
            enc = checkEncoding(v) # some fields automatically have some form of encoding used to obfuscate their contents
            n = "%s:%s" % (x,f)
            if n in fields:
                fields[n]["entropy"].append(e)
                fields[n]["length"].append(len(v))
                fields[n]["encoding"].append(enc)
            else:
                fields[n] = {
                    "entropy":[e],
                    "length":[len(v)],
                    "encoding": [enc]
                }
    for pf in p[proto].packetfields: # packet fields in DNS Response
        name = pf.name
        if p[proto].getfieldval(name):
            for f in p[proto].getfieldval(name).fields:
                v = p[proto].getfieldval(name).getfieldval(f)
                e = fieldEntropy(v)
                if e:
                    enc = checkEncoding(v)
                    n = "%s:%s:%s" % (x,name,f)
                    if n in fields:
                        fields[n]["entropy"].append(e)
                fields[n]["length"].append(len(v))
                fields[n]["encoding"].append(enc)
            else:
                fields[n] = {
                    "entropy":[e],
                    "length":[len(v)],
                    "encoding": [enc]
                }


def analyzeTraffic(p):
    protos = ProtocolAnalysis(p) # looking for different network protocols
    for proto in protos:  # look for potential opportunities to hide in the fields of each protocol.
        fieldAnalysis(p,proto)


# sniff(count=100,prn=analyzeTraffic) # live caputure 100 packets
# use sniff command in offline mode
sniff(offline="traffic.pcap",prn=analyzeTraffic)

for p in protocols:
    print(p,protocols[p])

for f in fields:
    # calculate average entropy
    entropies = fields[f]["entropy"]
    e = sum(entropies)/len(entropies)

    # calculate average length
    lenghts = fields[f]["length"]
    l = sum(lenghts)/len(lenghts)

    # Calculate counts of each encoding
    s = Series(fields[f]["encoding"])
    #print(s)
    counts = s.value_counts().to_dict()
    url = counts["URL"]/len(lenghts) if "URL" in counts else 0.0
    b64 = counts["B64"]/len(lenghts) if "B64" in counts else 0.0
    print("%s\n\tCount: %d\n\tAverage Lenght: %f\n\tAverage Entropy: %f\n\tURL Encoded: %f\n\tBase64 Encoded: %f" % (f,len(lenghts),l,e,url,b64))
    
