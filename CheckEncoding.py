# We're just going to look for something that's completely URL encoding
import re
from base64 import b64decode


# focus on things that are completely encoded (reserved characters)
def checkURLEncoding(data):
    # we're looking for a percent followed by two hexadecimal digits.
    if re.fullmatch('(%[0-9A-Fa-f]{2})+', str(data)):
        return True
    else:
        return False


def checkB64Encoding(data):
    try:
        plaintext = b64decode(data)
        return True
    except:
        return False


# check encoding
def checkEncoding(data):
    if len(data) == 0:  # 0 means successfully decoded by any scheme, it is confusing
        return False
    if checkURLEncoding(data):
        return "URL"
    elif checkB64Encoding(data):
        return "B64"
    else:
        return ""


from base64 import b64encode
data = [
    b64encode(bytes("Hello world!", "utf-8")),
    "%48%65%6C%6c%6F",
    "FFFFFFFF"]
for d in data:
    encoding = checkEncoding(d)
    if encoding:
        print(d, encoding)
