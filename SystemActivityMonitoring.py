# Detect brute force account through windows event voewer
# detect abnormalies events
from sqlalchemy import PrimaryKeyConstraint
import win32evtlog

server = "localhost"
logtype = "Security"
flags = win32evlog.EVENTLOG_FORWARDS_READ|win32evtlog.EVENTLOG_SEQUENTIAL_READ

failures = {}

def checkEvents():
    h = win32evtlog.OpenEventLog(server,logtype)
    while True:
        events = win32evtlog.ReadEventLog(h,flags,0)
        if events:
            for event in events:
                if event.EventID == 4625:
                    if event.StringInserts[0].startswith("s-1-5-21"):
                        account = event.StringInserts[1]
                        if account in failures:
                            failures[account]
                        else:
                            failures[account] = 1
        else:
            break
checkEvents()

for account in failures:
    print("%s: %s failed logins" % (account,failures[account]))


