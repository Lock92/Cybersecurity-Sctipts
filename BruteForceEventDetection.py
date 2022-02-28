import win32evtlog

server = "localhost"
logtype = "Security"
flags = win32evtlog.EVENTLOG_FORWARDS_READ(win32evtlog.
EVENTLOG_SEQENTIAL_READ)


def QueryEventLog(eventID, filename=None):
    logs = []
    if not filename:
        # live access
        h = win32evtlog.OpenEventLog(server,logtype)
    else:
        # access from the file(read a saved one)
        # if we put server=None, it's going to default localhost
        h = win32evtlog.OpenBackupEventLog(server,filename)
    while True:
        events = win32evtlog.ReadEventLog(h, flags, 0)
        if events:
            for event in events:
                if event.EventID == eventID:
                    logs.append(event)
        else:
            break
    return logs



def DetectBruteForce(filename=None):
    failures = {}
    events = QueryEventLog(4625,filename)
    for event in events:
        # String Insert [10] indicate Logon type
        if int(event.StringInerts[10]) in [3,8,10]:
            # String Insert [5] indicate user Name
            account = event.StrinInserts[5]
            if account in failures:
                failures[account] += 1
            else:
                failures[account] = 1
    return failures


filename = "events.evtx"
failures = DetectBruteForce(filename)   
for account in failures:
    print("%s: %s failed logins" % (account,failures[account]))